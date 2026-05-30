import asyncio
import html

from fastapi import APIRouter, Depends, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.state import call_caller_info, call_config, call_phone_map, pending_first, pending_rest
from app.services.business_service import get_business
from app.services.call_service import end_call, generate_and_save_summary, start_call
from app.services.conversation_service import _is_business_hours, clear_session
from app.services.customer_service import get_caller_context

router = APIRouter(prefix="/call", tags=["call"])


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
    db: AsyncSession = Depends(get_db),
):
    print(f"[CALL] Incoming call: {CallSid} from {From}", flush=True)
    call_phone_map[CallSid] = From

    ctx = await get_caller_context(db, From)
    call_caller_info[CallSid] = ctx
    config = await get_business(db)
    call_config[CallSid] = config

    await start_call(db, CallSid, From)

    biz_name = config.get("name", "Apex Home Services")
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
        await generate_and_save_summary(db, CallSid)
        clear_session(CallSid)
    elif CallStatus in ("failed", "busy", "no-answer"):
        await end_call(db, CallSid)
        clear_session(CallSid)
    call_phone_map.pop(CallSid, None)
    call_caller_info.pop(CallSid, None)
    call_config.pop(CallSid, None)
    return Response(status_code=204)
