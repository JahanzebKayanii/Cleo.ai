import asyncio
import html

from fastapi import APIRouter, Depends, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession
from twilio.rest import Client as TwilioClient

from app.core.config import settings
from app.core.database import get_db
from app.core.state import call_caller_info, call_config, call_hangup_set, call_phone_map, call_transfer_map, pending_first, pending_rest
from app.services.business_service import get_business, get_business_by_phone
from app.services.call_service import end_call, start_call
from app.services.conversation_service import _is_business_hours, clear_session
from app.services.customer_service import get_caller_context

router = APIRouter(prefix="/call", tags=["call"])


async def _start_recording(call_sid: str) -> None:
    try:
        client = TwilioClient(settings.twilio_account_sid, settings.twilio_auth_token)
        await asyncio.to_thread(lambda: client.calls(call_sid).recordings.create())
        print(f"[RECORD] Started for {call_sid}", flush=True)
    except Exception as e:
        print(f"[RECORD] Failed to start recording: {e}", flush=True)


async def _finalize_call(twilio_sid: str) -> None:
    """Runs after a short delay to avoid racing with the final transcript commit."""
    await asyncio.sleep(4)
    from app.core.database import get_db_context
    from app.services.business_service import get_business_raw
    from app.services.call_service import generate_and_save_summary, get_call_for_integrations
    from app.services.integration_service import push_to_integrations
    async with get_db_context() as db:
        await generate_and_save_summary(db, twilio_sid)
        call_info = await get_call_for_integrations(db, twilio_sid)
        if call_info:
            config = await get_business_raw(db)
            await push_to_integrations(
                customer_name=call_info.get("customer_name"),
                customer_phone=call_info.get("customer_phone", ""),
                transcript=call_info.get("transcript", ""),
                summary=call_info.get("summary", ""),
                config=config,
            )


def _stream_url() -> str:
    return settings.base_url.replace("https://", "wss://") + "/call/stream"


def twiml_greet_stream(say_text: str) -> Response:
    safe = html.escape(say_text)
    stream_url = _stream_url()
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<Response>"
        f'<Say voice="alice">{safe}</Say>'
        f'<Connect><Stream url="{stream_url}"/></Connect>'
        "</Response>"
    )
    return Response(content=body, media_type="application/xml")


@router.post("/incoming")
async def incoming_call(
    CallSid: str = Form(...),
    From: str = Form(...),
    To: str = Form(default=""),
    db: AsyncSession = Depends(get_db),
):
    print(f"[CALL] Incoming call: {CallSid} from {From} to {To}", flush=True)
    call_phone_map[CallSid] = From

    # Route to the right tenant by the Twilio number that was dialled
    config = await get_business_by_phone(db, To) if To else None
    if config is None:
        config = await get_business(db, 1)  # fallback to default tenant
    call_config[CallSid] = config

    ctx = await get_caller_context(db, From)
    call_caller_info[CallSid] = ctx

    business_id = config.get("id", 1)
    await start_call(db, CallSid, From, business_id)
    asyncio.create_task(_start_recording(CallSid))

    biz_name = config.get("name", "us")
    if not _is_business_hours(config):
        greeting = f"Thank you for calling {biz_name}. Our office is currently closed, but I can take a message and have someone call you back next business day. What's your name and what do you need help with?"
    elif ctx.get("name"):
        first_name = ctx["name"].split()[0]
        greeting = f"{biz_name}, this is Cleo. Welcome back, {first_name}! How can I help you today?"
    else:
        greeting = f"{biz_name}, this is Cleo, your virtual receptionist. How can I help you?"

    return twiml_greet_stream(greeting)


@router.post("/response")
async def pending_response(CallSid: str = Form(...)):
    stream_url = _stream_url()
    continue_url = settings.base_url + "/call/continue"

    # Poll until first sentence is ready (max 8 seconds)
    for _ in range(80):
        first = pending_first.get(CallSid)
        if first is not None:
            rest = pending_rest.get(CallSid)
            if rest is not None:
                # Full response already done — say everything and reconnect stream
                pending_first.pop(CallSid, None)
                pending_rest.pop(CallSid, None)
                full = (first + " " + rest).strip() if rest else first
                safe = html.escape(full)
                body = (
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    "<Response>"
                    f'<Say voice="alice">{safe}</Say>'
                    f'<Connect><Stream url="{stream_url}"/></Connect>'
                    "</Response>"
                )
            else:
                # Rest still generating — say first sentence, then redirect to continue
                safe = html.escape(first)
                body = (
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    "<Response>"
                    f'<Say voice="alice">{safe}</Say>'
                    f"<Redirect>{continue_url}</Redirect>"
                    "</Response>"
                )
            return Response(content=body, media_type="application/xml")
        await asyncio.sleep(0.1)

    # Timeout fallback
    pending_first.pop(CallSid, None)
    pending_rest.pop(CallSid, None)
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<Response>"
        '<Say voice="alice">Sorry, I had trouble with that. Could you repeat?</Say>'
        f'<Connect><Stream url="{stream_url}"/></Connect>'
        "</Response>"
    )
    return Response(content=body, media_type="application/xml")


@router.post("/continue")
async def continue_response(CallSid: str = Form(...)):
    stream_url = _stream_url()

    # Check for hangup first
    if CallSid in call_hangup_set:
        call_hangup_set.discard(CallSid)
        pending_first.pop(CallSid, None)
        pending_rest.pop(CallSid, None)
        body = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            "<Response>"
            "<Hangup/>"
            "</Response>"
        )
        print(f"[HANGUP] Hanging up {CallSid}", flush=True)
        return Response(content=body, media_type="application/xml")

    # Check for live transfer
    if CallSid in call_transfer_map:
        transfer_phone = call_transfer_map.pop(CallSid)
        pending_first.pop(CallSid, None)
        pending_rest.pop(CallSid, None)
        body = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            "<Response>"
            f"<Dial>{transfer_phone}</Dial>"
            "</Response>"
        )
        print(f"[TRANSFER] Dialing {transfer_phone} for {CallSid}", flush=True)
        return Response(content=body, media_type="application/xml")

    # Poll until rest of response is ready (max 6 seconds — should already be done)
    for _ in range(60):
        rest = pending_rest.get(CallSid)
        if rest is not None:
            pending_first.pop(CallSid, None)
            pending_rest.pop(CallSid, None)
            if rest:
                safe = html.escape(rest)
                body = (
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    "<Response>"
                    f'<Say voice="alice">{safe}</Say>'
                    f'<Connect><Stream url="{stream_url}"/></Connect>'
                    "</Response>"
                )
            else:
                # No rest — just reconnect stream
                body = (
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    "<Response>"
                    f'<Connect><Stream url="{stream_url}"/></Connect>'
                    "</Response>"
                )
            return Response(content=body, media_type="application/xml")
        await asyncio.sleep(0.1)

    # Timeout fallback
    pending_first.pop(CallSid, None)
    pending_rest.pop(CallSid, None)
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<Response>"
        f'<Connect><Stream url="{stream_url}"/></Connect>'
        "</Response>"
    )
    return Response(content=body, media_type="application/xml")


@router.post("/status")
async def call_status(
    CallSid: str = Form(...),
    CallStatus: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    if CallStatus == "completed":
        await end_call(db, CallSid)
        asyncio.create_task(_finalize_call(CallSid))
        clear_session(CallSid)
    elif CallStatus in ("failed", "busy", "no-answer"):
        await end_call(db, CallSid)
        clear_session(CallSid)
    call_phone_map.pop(CallSid, None)
    call_caller_info.pop(CallSid, None)
    call_config.pop(CallSid, None)
    call_transfer_map.pop(CallSid, None)
    return Response(status_code=204)
