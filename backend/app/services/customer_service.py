from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer


async def get_or_create_customer(
    db: AsyncSession, phone: str, name: str | None = None
) -> tuple[Customer, bool]:
    result = await db.execute(select(Customer).where(Customer.phone == phone))
    customer = result.scalar_one_or_none()
    if customer:
        return customer, False

    customer = Customer(phone=phone, name=name)
    db.add(customer)
    await db.flush()
    return customer, True


async def get_customer(customer_id: int, db: AsyncSession) -> Customer | None:
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    return result.scalar_one_or_none()
