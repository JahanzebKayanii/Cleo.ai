from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.business_service import get_business, update_business

router = APIRouter(prefix="/business", tags=["business"])


@router.get("/config")
async def get_config(db: AsyncSession = Depends(get_db)):
    return await get_business(db)


@router.put("/config")
async def put_config(data: dict, db: AsyncSession = Depends(get_db)):
    return await update_business(db, data)
