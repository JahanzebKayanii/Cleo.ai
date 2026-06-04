import asyncio

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from twilio.rest import Client as TwilioClient

from app.core.config import settings
from app.core.database import get_db
from app.models.call import Call

router = APIRouter(prefix="/calls", tags=["calls"])

_twilio: TwilioClient | None = None


def _get_twilio() -> TwilioClient:
    global _twilio
    if _twilio is None:
        _twilio = TwilioClient(settings.twilio_account_sid, settings.twilio_auth_token)
    return _twilio


@router.get("/")
async def list_calls(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Call).order_by(desc(Call.started_at)).limit(100))
    calls = result.scalars().all()
    return [
        {
            "id": c.id,
            "customer_name": c.customer.name if c.customer else None,
            "customer_phone": c.customer.phone if c.customer else None,
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


@router.get("/{call_id}/recording")
async def get_recording(call_id: int, db: AsyncSession = Depends(get_db)):
    call = await db.get(Call, call_id)
    if not call or not call.twilio_call_sid:
        raise HTTPException(status_code=404, detail="No recording")

    client = _get_twilio()
    recordings = await asyncio.to_thread(
        lambda: client.recordings.list(call_sid=call.twilio_call_sid, limit=1)
    )
    if not recordings:
        raise HTTPException(status_code=404, detail="No recording found")

    rec = recordings[0]
    audio_url = (
        f"https://api.twilio.com/2010-04-01/Accounts/"
        f"{settings.twilio_account_sid}/Recordings/{rec.sid}.mp3"
    )
    async with httpx.AsyncClient() as http_client:
        resp = await http_client.get(
            audio_url,
            auth=(settings.twilio_account_sid, settings.twilio_auth_token),
            follow_redirects=True,
            timeout=30.0,
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Recording not available")
    return Response(content=resp.content, media_type="audio/mpeg")
