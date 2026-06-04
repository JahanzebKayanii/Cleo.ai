import asyncio

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from twilio.rest import Client as TwilioClient

from app.core.config import settings
from app.core.database import get_db
from app.models.call import Call

router = APIRouter(prefix="/calls", tags=["calls"])


class TestPushPayload(BaseModel):
    customer_name: str = "John Smith"
    customer_phone: str = "+15551234567"
    service_type: str = "HVAC"
    issue_description: str = "AC not cooling, making loud noise"
    address: str = "123 Main St, Austin TX 78701"
    booked: bool = True
    appointment_date: str | None = "2026-06-10"
    appointment_time: str | None = "10am - 12pm"
    summary: str = "Customer called about AC unit not cooling and making a loud noise. Appointment booked for June 10th between 10am and 12pm at 123 Main St."


@router.post("/test-push")
async def test_push(payload: TestPushPayload, db: AsyncSession = Depends(get_db)):
    """Simulate a completed call and push to all configured integrations. Use for testing without a real call."""
    from app.services.business_service import get_business_raw
    from app.services.integration_service import push_to_integrations

    transcript = (
        f"Caller: Hi, I need help with my AC, it's not cooling and making a loud noise.\n"
        f"Cleo: I can help with that. Can I get your name?\n"
        f"Caller: {payload.customer_name}.\n"
        f"Cleo: And your address?\n"
        f"Caller: {payload.address}.\n"
        f"Cleo: Got it. We can send a technician on {payload.appointment_date} between {payload.appointment_time}. Does that work?\n"
        f"Caller: Yes that works great.\n"
        f"Cleo: Perfect, you're booked. Is there anything else?\n"
        f"Caller: No that's all, thanks.\n"
        f"Cleo: Have a great day!\n"
    ) if payload.booked else (
        f"Caller: Hi, I need help with my {payload.service_type.lower()}, {payload.issue_description}.\n"
        f"Cleo: I can help with that. Can I get your name?\n"
        f"Caller: {payload.customer_name}.\n"
        f"Cleo: And your address?\n"
        f"Caller: {payload.address}.\n"
        f"Cleo: Let me check availability and have someone call you back.\n"
        f"Caller: Ok thanks.\n"
    )

    config = await get_business_raw(db)
    await push_to_integrations(
        customer_name=payload.customer_name,
        customer_phone=payload.customer_phone,
        transcript=transcript,
        summary=payload.summary,
        config=config,
    )
    return {"ok": True, "pushed_to": [k for k in ["hubspot_token", "jobber_api_key", "housecall_pro_api_key", "quickbooks_token"] if config.get(k)]}

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


@router.post("/{call_id}/push-integrations")
async def push_integrations(call_id: int, db: AsyncSession = Depends(get_db)):
    call = await db.get(Call, call_id)
    if not call or not call.twilio_call_sid:
        raise HTTPException(status_code=404, detail="Call not found")
    from app.services.business_service import get_business_raw
    from app.services.call_service import generate_and_save_summary, get_call_for_integrations
    from app.services.integration_service import push_to_integrations
    await generate_and_save_summary(db, call.twilio_call_sid)
    call_info = await get_call_for_integrations(db, call.twilio_call_sid)
    if not call_info:
        raise HTTPException(status_code=400, detail="No transcript found for this call")
    config = await get_business_raw(db)
    await push_to_integrations(
        customer_name=call_info.get("customer_name"),
        customer_phone=call_info.get("customer_phone", ""),
        transcript=call_info.get("transcript", ""),
        summary=call_info.get("summary", ""),
        config=config,
    )
    return {"ok": True}


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
