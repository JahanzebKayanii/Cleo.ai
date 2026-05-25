import html

from fastapi import APIRouter, Depends, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.call_service import append_transcript, end_call, start_call
from app.services.conversation_service import clear_session, get_response
from app.services.stt_service import transcribe_twilio_recording

router = APIRouter(prefix="/call", tags=["call"])

RECORD_ATTRS = (
    'action="/call/transcribe" '
    'method="POST" '
    'maxLength="30" '
    'playBeep="false" '
    'timeout="3"'
)


def twiml_record(say_text: str) -> Response:
    safe = html.escape(say_text)
    body = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">{safe}</Say>
    <Record {RECORD_ATTRS}/>
</Response>"""
    return Response(content=body, media_type="application/xml")


def twiml_say_record(text: str) -> Response:
    safe = html.escape(text)
    body = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">{safe}</Say>
    <Record {RECORD_ATTRS}/>
</Response>"""
    return Response(content=body, media_type="application/xml")


async def speak_and_record(text: str) -> Response:
    return twiml_say_record(text)


@router.post("/incoming")
async def incoming_call(
    CallSid: str = Form(...),
    From: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    await start_call(db, CallSid, From)
    return twiml_record(
        "Thank you for calling Apex Home Services. "
        "This is Cleo, your AI receptionist. How can I help you today?"
    )


@router.post("/transcribe")
async def transcribe(
    CallSid: str = Form(...),
    From: str = Form(...),
    RecordingUrl: str = Form(...),
    RecordingDuration: str = Form(default="0"),
    db: AsyncSession = Depends(get_db),
):
    if int(RecordingDuration) < 1:
        return await speak_and_record("I didn't catch that. Could you please repeat?")

    try:
        transcript = await transcribe_twilio_recording(RecordingUrl)
        print(f"[STT] Deepgram transcript: {transcript}", flush=True)
    except Exception as e:
        print(f"[STT] Deepgram failed: {e}", flush=True)
        return await speak_and_record("Sorry, I had trouble hearing you. Could you repeat that?")

    if not transcript:
        return await speak_and_record("I didn't catch that. Could you please repeat?")

    reply = await get_response(CallSid, transcript)
    await append_transcript(db, CallSid, transcript, reply)
    return await speak_and_record(reply)


@router.post("/status")
async def call_status(
    CallSid: str = Form(...),
    CallStatus: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    if CallStatus in ("completed", "failed", "busy", "no-answer"):
        await end_call(db, CallSid)
        clear_session(CallSid)
    return Response(status_code=204)
