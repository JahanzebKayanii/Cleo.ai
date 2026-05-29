import asyncio
import base64
import html
import json

from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from twilio.rest import Client as TwilioClient

from app.core.config import settings
from app.core.database import get_db_context
from app.services.call_service import append_transcript
from app.services.conversation_service import get_response

router = APIRouter(tags=["stream"])


def _stream_url() -> str:
    return settings.base_url.replace("https://", "wss://") + "/call/stream"


def _twiml_say_stream(text: str) -> str:
    safe = html.escape(text)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<Response>"
        f'<Say voice="alice">{safe}</Say>'
        f'<Connect><Stream url="{_stream_url()}"/></Connect>'
        "</Response>"
    )


async def _update_twilio_call(call_sid: str, twiml: str) -> None:
    client = TwilioClient(settings.twilio_account_sid, settings.twilio_auth_token)
    await asyncio.to_thread(client.calls(call_sid).update, twiml=twiml)


@router.websocket("/call/stream")
async def media_stream(websocket: WebSocket):
    print("[STREAM] WebSocket connection received", flush=True)
    await websocket.accept()
    print("[STREAM] WebSocket accepted", flush=True)

    call_sid: str | None = None
    transcript_event = asyncio.Event()
    final_transcript: list[str] = [""]

    deepgram = DeepgramClient(settings.deepgram_api_key)
    dg = deepgram.listen.asynclive.v("1")

    async def on_transcript(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if result.is_final and sentence.strip():
            final_transcript[0] = sentence.strip()
            transcript_event.set()

    dg.on(LiveTranscriptionEvents.Transcript, on_transcript)

    options = LiveOptions(
        model="nova-2",
        encoding="mulaw",
        sample_rate=8000,
        channels=1,
        endpointing=500,
        interim_results=True,
    )

    try:
        started = await dg.start(options)
        print(f"[STREAM] Deepgram live session started: {started}", flush=True)
    except Exception as e:
        print(f"[STREAM] ERROR starting Deepgram: {e}", flush=True)
        await websocket.close()
        return

    try:
        async for raw in websocket.iter_text():
            data = json.loads(raw)
            event = data.get("event")

            if event == "start":
                call_sid = data["start"]["callSid"]
                print(f"[STREAM] Call started: {call_sid}", flush=True)

            elif event == "media":
                audio = base64.b64decode(data["media"]["payload"])
                await dg.send(audio)

                if transcript_event.is_set():
                    transcript = final_transcript[0]
                    transcript_event.clear()
                    print(f"[STT] Live: {transcript}", flush=True)

                    await dg.finish()

                    reply = await get_response(call_sid, transcript)
                    print(f"[LLM] Cleo: {reply}", flush=True)

                    async with get_db_context() as db:
                        await append_transcript(db, call_sid, transcript, reply)

                    await _update_twilio_call(call_sid, _twiml_say_stream(reply))
                    break

            elif event == "stop":
                print(f"[STREAM] Call stream stopped: {call_sid}", flush=True)
                break

    except WebSocketDisconnect:
        print("[STREAM] WebSocket disconnected", flush=True)
    except Exception as e:
        print(f"[STREAM] ERROR in stream loop: {e}", flush=True)
    finally:
        await dg.finish()
        print("[STREAM] Deepgram session closed", flush=True)
