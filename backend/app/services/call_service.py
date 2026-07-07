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


def _classify_intent(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["hvac", "ac", "air condition", "heat", "furnace", "thermostat", "duct", "cool", "warm"]):
        return "hvac"
    if any(w in t for w in ["plumb", "pipe", "leak", "drain", "toilet", "faucet", "water heater", "sewer"]):
        return "plumbing"
    if any(w in t for w in ["electric", "outlet", "breaker", "wiring", "panel", "light", "switch", "power"]):
        return "electrical"
    return "other"


async def start_call(
    db: AsyncSession, twilio_sid: str, from_phone: str, business_id: int = 1
) -> tuple[Call, int]:
    customer, _ = await get_or_create_customer(db, from_phone, business_id)
    call = Call(
        customer_id=customer.id,
        business_id=business_id,
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
        "business_id": call.business_id or 1,
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
    from app.services.business_service import get_business
    config = await get_business(db, call.business_id or 1)
    biz_name = config.get("name", "the business")
    client = _get_anthropic()
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Summarise this {biz_name} call in 2-3 sentences.{name_hint} "
                    "Cover: what the customer wanted, what was resolved, and any follow-up needed.\n\n"
                    f"{call.transcript}"
                ),
            }
        ],
    )
    call.summary = response.content[0].text.strip()
    call.intent = _classify_intent(call.transcript)

    # Send email summary to business owner
    from app.services.email_service import send_call_summary
    if config.get("owner_email"):
        asyncio.create_task(send_call_summary(
            to_email=config["owner_email"],
            business_name=config.get("name", "the business"),
            customer_name=call.customer.name if call.customer else None,
            customer_phone=call.customer.phone if call.customer else "",
            summary=call.summary,
            transcript=call.transcript,
        ))
