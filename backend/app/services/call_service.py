from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.call import Call
from app.services.customer_service import get_or_create_customer


async def start_call(
    db: AsyncSession, twilio_sid: str, from_phone: str
) -> tuple[Call, int]:
    customer, _ = await get_or_create_customer(db, from_phone)
    call = Call(
        customer_id=customer.id,
        twilio_call_sid=twilio_sid,
        status="in_progress",
    )
    db.add(call)
    await db.flush()
    return call, customer.id


async def append_transcript(
    db: AsyncSession, twilio_sid: str, caller_text: str, cleo_text: str
) -> None:
    result = await db.execute(
        select(Call).where(Call.twilio_call_sid == twilio_sid)
    )
    call = result.scalar_one_or_none()
    if not call:
        return
    existing = call.transcript or ""
    call.transcript = existing + f"Caller: {caller_text}\nCleo: {cleo_text}\n\n"


async def end_call(db: AsyncSession, twilio_sid: str) -> None:
    result = await db.execute(
        select(Call).where(Call.twilio_call_sid == twilio_sid)
    )
    call = result.scalar_one_or_none()
    if not call:
        return
    call.status = "completed"
    call.ended_at = datetime.now(timezone.utc)
