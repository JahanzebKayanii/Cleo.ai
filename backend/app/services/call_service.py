import asyncio
from datetime import datetime, timezone

from anthropic import AsyncAnthropic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.call import Call
from app.services.customer_service import get_or_create_customer

_anthropic: AsyncAnthropic | None = None


def _get_anthropic() -> AsyncAnthropic:
    global _anthropic
    if _anthropic is None:
        _anthropic = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _anthropic


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


async def get_call_for_integrations(db: AsyncSession, twilio_sid: str) -> dict | None:
    result = await db.execute(select(Call).where(Call.twilio_call_sid == twilio_sid))
    call = result.scalar_one_or_none()
    if not call or not call.transcript:
        return None
    return {
        "customer_name": call.customer.name if call.customer else None,
        "customer_phone": call.customer.phone if call.customer else "",
        "transcript": call.transcript or "",
        "summary": call.summary or "",
    }


async def generate_and_save_summary(db: AsyncSession, twilio_sid: str) -> None:
    result = await db.execute(
        select(Call).where(Call.twilio_call_sid == twilio_sid)
    )
    call = result.scalar_one_or_none()
    if not call or not call.transcript:
        return

    name_hint = f" The customer's name is {call.customer.name}." if call.customer and call.customer.name else ""
    client = _get_anthropic()
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Summarise this Apex Home Services call in 2-3 sentences.{name_hint} "
                    "Cover: what the customer wanted, what was resolved, and any follow-up needed.\n\n"
                    f"{call.transcript}"
                ),
            }
        ],
    )
    call.summary = response.content[0].text.strip()

    # Send email summary to business owner
    from app.services.business_service import get_business
    from app.services.email_service import send_call_summary
    config = await get_business(db)
    if config.get("owner_email"):
        asyncio.create_task(send_call_summary(
            to_email=config["owner_email"],
            business_name=config.get("name", "Apex Home Services"),
            customer_name=call.customer.name if call.customer else None,
            customer_phone=call.customer.phone if call.customer else "",
            summary=call.summary,
            transcript=call.transcript,
        ))
