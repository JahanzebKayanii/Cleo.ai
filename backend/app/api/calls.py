from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.call import Call

router = APIRouter(prefix="/calls", tags=["calls"])


@router.get("/")
async def list_calls(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Call).order_by(desc(Call.started_at)).limit(100))
    calls = result.scalars().all()
    return [
        {
            "id": c.id,
            "phone": c.customer.phone if c.customer else None,
            "status": c.status,
            "summary": c.summary,
            "started_at": c.started_at,
            "ended_at": c.ended_at,
        }
        for c in calls
    ]


@router.get("/{call_id}")
async def get_call(call_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Call).where(Call.id == call_id))
    call = result.scalar_one_or_none()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return {
        "id": call.id,
        "phone": call.customer.phone if call.customer else None,
        "status": call.status,
        "summary": call.summary,
        "transcript": call.transcript,
        "started_at": call.started_at,
        "ended_at": call.ended_at,
    }
