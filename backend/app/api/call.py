import html

from fastapi import APIRouter, Depends, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.services.call_service import end_call, generate_and_save_summary, start_call
from app.services.conversation_service import clear_session

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
    await start_call(db, CallSid, From)
    return twiml_greet_stream(
        "Thank you for calling Apex Home Services. "
        "This is Cleo, your AI receptionist. How can I help you today?"
    )


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
    return Response(status_code=204)
