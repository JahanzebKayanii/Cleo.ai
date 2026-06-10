from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.call import Call
from app.models.customer import Customer


async def get_or_create_customer(
    db: AsyncSession, phone: str, business_id: int = 1, name: str | None = None
) -> tuple[Customer, bool]:
    result = await db.execute(
        select(Customer).where(Customer.phone == phone, Customer.business_id == business_id)
    )
    customer = result.scalar_one_or_none()
    if customer:
        return customer, False

    customer = Customer(phone=phone, business_id=business_id, name=name)
    db.add(customer)
    await db.flush()
    return customer, True


async def get_customer(customer_id: int, db: AsyncSession) -> Customer | None:
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    return result.scalar_one_or_none()


async def get_caller_context(db: AsyncSession, phone: str, business_id: int = 1) -> dict:
    """Return name and recent call summaries for a phone number scoped to a tenant.
    Empty dict for first-time callers to this specific tenant.
    """
    result = await db.execute(
        select(Customer).where(Customer.phone == phone, Customer.business_id == business_id)
    )
    customer = result.scalar_one_or_none()
    if not customer or not customer.name:
        return {}

    calls_result = await db.execute(
        select(Call)
        .where(
            Call.customer_id == customer.id,
            Call.business_id == business_id,
            Call.summary.isnot(None),
        )
        .order_by(Call.started_at.desc())
        .limit(3)
    )
    summaries = [c.summary for c in calls_result.scalars().all()]
    return {"name": customer.name, "summaries": summaries}


async def update_customer_name(db: AsyncSession, phone: str, name: str, business_id: int = 1) -> None:
    result = await db.execute(
        select(Customer).where(Customer.phone == phone, Customer.business_id == business_id)
    )
    customer = result.scalar_one_or_none()
    if customer and not customer.name:
        customer.name = name
