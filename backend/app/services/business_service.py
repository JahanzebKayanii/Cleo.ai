import json
import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.business import Business

_cache: dict[int, dict] = {}   # business_id -> masked dict
_cache_ts: dict[int, float] = {}
_phone_to_id: dict[str, int] = {}  # twilio_phone_number -> business_id
_CACHE_TTL = 60


def _to_dict(b: Business, mask_keys: bool = True) -> dict:
    def _mask(v): return "saved" if v else ""
    return {
        "id": b.id,
        "name": b.name,
        "description": b.description,
        "timezone": b.timezone,
        "services": json.loads(b.services) if b.services else [],
        "hours_open": b.hours_open,
        "hours_close": b.hours_close,
        "service_area": b.service_area or "Austin, TX and surrounding areas within 30 miles",
        "owner_email": b.owner_email or "",
        "transfer_phone": b.transfer_phone or "",
        "twilio_phone_number": b.twilio_phone_number or "",
        "slug": b.slug or "",
        "industry": b.industry or "hvac",
        "qdrant_collection": b.qdrant_collection or f"tenant_{b.id}",
        "google_calendar_id": b.google_calendar_id or settings.google_calendar_id,
        "google_service_account_b64": "" if mask_keys else (b.google_service_account_b64 or settings.google_service_account_b64),
        "is_active": b.is_active,
        "stripe_customer_id": b.stripe_customer_id or "",
        "stripe_subscription_id": b.stripe_subscription_id or "",
        "jobber_api_key": _mask(b.jobber_api_key) if mask_keys else (b.jobber_api_key or ""),
        "jobber_refresh_token": "" if mask_keys else (b.jobber_refresh_token or ""),
        "hubspot_token": _mask(b.hubspot_token) if mask_keys else (b.hubspot_token or ""),
        "housecall_pro_api_key": _mask(b.housecall_pro_api_key) if mask_keys else (b.housecall_pro_api_key or ""),
        "quickbooks_token": _mask(b.quickbooks_token) if mask_keys else (b.quickbooks_token or ""),
        "servicetitan_token": _mask(b.servicetitan_token) if mask_keys else (b.servicetitan_token or ""),
    }


async def get_business(db: AsyncSession, business_id: int = 1) -> dict:
    global _cache, _cache_ts
    if business_id in _cache and time.time() - _cache_ts.get(business_id, 0) < _CACHE_TTL:
        return _cache[business_id]

    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()

    if not business:
        business = Business(
            id=1,
            name="Apex Home Services",
            description="a licensed HVAC, plumbing, and electrical company based in Austin, Texas",
            timezone="America/Chicago",
            services='["HVAC", "plumbing", "electrical"]',
            hours_open=8,
            hours_close=18,
        )
        db.add(business)
        await db.flush()

    _cache[business_id] = _to_dict(business)
    _cache_ts[business_id] = time.time()
    if business.twilio_phone_number:
        _phone_to_id[business.twilio_phone_number] = business.id
    return _cache[business_id]


async def get_business_raw(db: AsyncSession, business_id: int = 1) -> dict:
    """Returns real API keys — for internal use only, never expose to frontend."""
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if not business:
        return {}
    return _to_dict(business, mask_keys=False)


async def get_business_by_phone(db: AsyncSession, phone: str) -> dict | None:
    """Look up a tenant by the Twilio number the caller dialled. Returns masked config."""
    if phone in _phone_to_id:
        bid = _phone_to_id[phone]
        if bid in _cache and time.time() - _cache_ts.get(bid, 0) < _CACHE_TTL:
            return _cache[bid]

    result = await db.execute(select(Business).where(Business.twilio_phone_number == phone))
    business = result.scalar_one_or_none()
    if not business:
        return None

    config = _to_dict(business)
    _cache[business.id] = config
    _cache_ts[business.id] = time.time()
    _phone_to_id[phone] = business.id
    return config


async def get_business_raw_by_phone(db: AsyncSession, phone: str) -> dict | None:
    result = await db.execute(select(Business).where(Business.twilio_phone_number == phone))
    business = result.scalar_one_or_none()
    if not business:
        return None
    return _to_dict(business, mask_keys=False)


async def list_businesses(db: AsyncSession) -> list[dict]:
    result = await db.execute(select(Business).order_by(Business.id))
    businesses = result.scalars().all()
    return [_to_dict(b) for b in businesses]


async def create_business(db: AsyncSession, data: dict) -> dict:
    business = Business(
        name=data.get("name", "New Business"),
        description=data.get("description"),
        timezone=data.get("timezone", "America/Chicago"),
        services=json.dumps(data.get("services", ["HVAC", "plumbing", "electrical"])),
        hours_open=int(data.get("hours_open", 8)),
        hours_close=int(data.get("hours_close", 18)),
        service_area=data.get("service_area"),
        owner_email=data.get("owner_email"),
        transfer_phone=data.get("transfer_phone"),
        twilio_phone_number=data.get("twilio_phone_number") or None,
        slug=data.get("slug") or None,
        dashboard_password=data.get("dashboard_password") or None,
        industry=data.get("industry", "hvac"),
        google_calendar_id=data.get("google_calendar_id") or None,
        is_active=True,
    )
    db.add(business)
    await db.flush()
    # Each tenant gets their own Qdrant collection name
    business.qdrant_collection = f"tenant_{business.id}"
    return _to_dict(business)


async def update_business(db: AsyncSession, data: dict, business_id: int = 1) -> dict:
    global _cache, _cache_ts
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()

    if not business:
        business = Business(id=1)
        db.add(business)

    str_fields = ["name", "description", "timezone", "service_area", "owner_email",
                  "transfer_phone", "twilio_phone_number", "slug", "dashboard_password",
                  "industry", "google_calendar_id"]
    for field in str_fields:
        if field in data:
            setattr(business, field, data[field] or None if field not in ("name", "timezone") else data[field])

    if "services" in data:
        business.services = json.dumps(data["services"])
    if "hours_open" in data:
        business.hours_open = int(data["hours_open"])
    if "hours_close" in data:
        business.hours_close = int(data["hours_close"])
    if "is_active" in data:
        business.is_active = bool(data["is_active"])

    # Only update integration keys if a non-empty value is provided
    secret_fields = ["jobber_api_key", "hubspot_token", "housecall_pro_api_key",
                     "quickbooks_token", "servicetitan_token", "google_service_account_b64"]
    for field in secret_fields:
        if data.get(field) and data[field] not in ("saved", "__clear__"):
            setattr(business, field, data[field])

    # Explicit clear
    for field in secret_fields + ["jobber_refresh_token"]:
        if data.get(field) == "__clear__":
            setattr(business, field, None)
    if data.get("jobber_api_key") == "__clear__":
        business.jobber_refresh_token = None

    # Stripe fields (set by billing webhook only)
    for field in ["stripe_customer_id", "stripe_subscription_id"]:
        if field in data:
            setattr(business, field, data[field] or None)

    # Invalidate cache
    _cache.pop(business_id, None)
    _cache_ts.pop(business_id, None)
    if business.twilio_phone_number:
        _phone_to_id[business.twilio_phone_number] = business.id

    return _to_dict(business)


def invalidate_cache(business_id: int | None = None) -> None:
    if business_id is None:
        _cache.clear()
        _cache_ts.clear()
        _phone_to_id.clear()
    else:
        _cache.pop(business_id, None)
        _cache_ts.pop(business_id, None)
