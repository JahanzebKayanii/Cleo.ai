import json

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_session
from app.core.config import settings
from app.core.database import get_db
from app.models.business import Business
from app.services.business_service import invalidate_cache

router = APIRouter(prefix="/billing", tags=["billing"])


def _stripe():
    try:
        import stripe
        stripe.api_key = settings.stripe_secret_key
        return stripe
    except ImportError:
        raise HTTPException(status_code=500, detail="Stripe not installed. Run: pip install stripe")


@router.post("/checkout")
async def create_checkout(request: Request, db: AsyncSession = Depends(get_db)):
    """Create a Stripe Checkout session for a given tenant."""
    token = request.cookies.get("cleo_session")
    s = get_session(token)
    if not s or s.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    body = await request.json()
    business_id = body.get("business_id", 1)

    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Tenant not found")

    if not settings.stripe_price_id:
        raise HTTPException(status_code=500, detail="STRIPE_PRICE_ID not configured")

    stripe = _stripe()

    # Create or reuse Stripe customer
    if not business.stripe_customer_id:
        customer = stripe.Customer.create(
            email=business.owner_email or "",
            name=business.name,
            metadata={"business_id": str(business_id)},
        )
        business.stripe_customer_id = customer["id"]
        await db.commit()
        invalidate_cache(business_id)

    session = stripe.checkout.Session.create(
        customer=business.stripe_customer_id,
        payment_method_types=["card"],
        line_items=[{"price": settings.stripe_price_id, "quantity": 1}],
        mode="subscription",
        success_url=f"{settings.base_url}/dashboard/admin.html?billing=success&bid={business_id}",
        cancel_url=f"{settings.base_url}/dashboard/admin.html?billing=cancelled&bid={business_id}",
        metadata={"business_id": str(business_id)},
    )

    return {"checkout_url": session["url"]}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    if not settings.stripe_webhook_secret:
        raise HTTPException(status_code=500, detail="STRIPE_WEBHOOK_SECRET not configured")

    stripe = _stripe()
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.stripe_webhook_secret)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {e}")

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type in ("checkout.session.completed", "invoice.payment_succeeded"):
        sub_id = data.get("subscription")
        customer_id = data.get("customer")
        business_id = int((data.get("metadata") or {}).get("business_id", 0))

        if business_id:
            result = await db.execute(select(Business).where(Business.id == business_id))
            business = result.scalar_one_or_none()
            if business:
                if sub_id:
                    business.stripe_subscription_id = sub_id
                business.is_active = True
                invalidate_cache(business_id)

    elif event_type in ("customer.subscription.deleted", "invoice.payment_failed"):
        sub_id = data.get("id") or data.get("subscription")
        if sub_id:
            result = await db.execute(
                select(Business).where(Business.stripe_subscription_id == sub_id)
            )
            business = result.scalar_one_or_none()
            if business:
                business.is_active = False
                invalidate_cache(business.id)

    return Response(status_code=200)


@router.get("/portal")
async def billing_portal(request: Request, business_id: int = 1, db: AsyncSession = Depends(get_db)):
    """Redirect to Stripe Customer Portal for subscription management."""
    token = request.cookies.get("cleo_session")
    s = get_session(token)
    if not s or s.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if not business or not business.stripe_customer_id:
        raise HTTPException(status_code=404, detail="No Stripe customer found for this tenant")

    stripe = _stripe()
    session = stripe.billing_portal.Session.create(
        customer=business.stripe_customer_id,
        return_url=f"{settings.base_url}/dashboard/admin.html",
    )
    return {"portal_url": session["url"]}
