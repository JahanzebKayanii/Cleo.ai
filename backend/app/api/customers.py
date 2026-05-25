from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.customer_service import get_customer, get_or_create_customer

router = APIRouter(prefix="/customers", tags=["customers"])


class CustomerRequest(BaseModel):
    phone: str
    name: str | None = None


@router.post("/")
async def create_customer(body: CustomerRequest, db: AsyncSession = Depends(get_db)):
    customer, created = await get_or_create_customer(db, body.phone, body.name)
    return {
        "id": customer.id,
        "phone": customer.phone,
        "name": customer.name,
        "created": created,
    }


@router.get("/{customer_id}")
async def get(customer_id: int, db: AsyncSession = Depends(get_db)):
    customer = await get_customer(customer_id, db)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
