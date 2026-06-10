from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import require_admin
from app.core.database import get_db
from app.models.business import Business
from app.services.business_service import create_business, list_businesses, update_business, invalidate_cache

router = APIRouter(prefix="/admin", tags=["admin"])


def _require_admin(request: Request) -> None:
    require_admin(request)


@router.get("/tenants")
async def get_tenants(request: Request, db: AsyncSession = Depends(get_db)):
    _require_admin(request)
    return await list_businesses(db)


@router.post("/tenants")
async def create_tenant(request: Request, data: dict, db: AsyncSession = Depends(get_db)):
    _require_admin(request)
    tenant = await create_business(db, data)
    return tenant


@router.put("/tenants/{business_id}")
async def update_tenant(
    business_id: int, request: Request, data: dict, db: AsyncSession = Depends(get_db)
):
    _require_admin(request)
    result = await db.execute(select(Business).where(Business.id == business_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Tenant not found")
    return await update_business(db, data, business_id)


@router.delete("/tenants/{business_id}")
async def delete_tenant(business_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    _require_admin(request)
    if business_id == 1:
        raise HTTPException(status_code=400, detail="Cannot delete the default tenant")
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Tenant not found")
    await db.delete(business)
    invalidate_cache(business_id)
    return {"ok": True}


@router.post("/tenants/{business_id}/activate")
async def activate_tenant(business_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    _require_admin(request)
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Tenant not found")
    business.is_active = True
    invalidate_cache(business_id)
    return {"ok": True}


@router.post("/tenants/{business_id}/deactivate")
async def deactivate_tenant(business_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    _require_admin(request)
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Tenant not found")
    business.is_active = False
    invalidate_cache(business_id)
    return {"ok": True}
