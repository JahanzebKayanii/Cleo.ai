from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import require_admin, require_tenant_access
from app.core.database import get_db
from app.services.customer_service import get_customer, get_or_create_customer

router = APIRouter(prefix="/customers", tags=["customers"])


class CustomerRequest(BaseModel):
    phone: str
    name: str | None = None
    business_id: int = 1


@router.post("/")
async def create_customer(body: CustomerRequest, request: Request, db: AsyncSession = Depends(get_db)):
    require_tenant_access(request, body.business_id)
    customer, created = await get_or_create_customer(db, body.phone, body.business_id, body.name)
    return {
        "id": customer.id,
        "phone": customer.phone,
        "name": customer.name,
        "business_id": customer.business_id,
        "created": created,
    }


@router.get("/{customer_id}")
async def get(customer_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    customer = await get_customer(customer_id, db)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    require_tenant_access(request, customer.business_id or 1)
    return customer
