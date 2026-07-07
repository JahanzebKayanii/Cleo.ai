import asyncio
import base64
import html
import json
import time

from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from twilio.rest import Client as TwilioClient

from app.core.config import settings
from app.core.database import get_db_context
from app.core.state import call_caller_info, call_config, call_hangup_set, call_phone_map, call_transfer_map, pending_audio, pending_first, pending_rest
from app.services.call_service import append_transcript
from app.services.conversation_service import stream_response_parts

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


async def _pregenerate_audio(call_sid: str, text: str) -> None:
    try:
        from app.services.tts_service import text_to_speech
        filename = await text_to_speech(text)
        pending_audio[call_sid] = filename
        print(f"[TTS] Pre-generated audio for {call_sid}", flush=True)
    except Exception as e:
        pending_audio[call_sid] = ""  # empty = failed, call.py falls back to <Say>
        print(f"[TTS] Pre-generation failed for {call_sid}: {e}", flush=True)


async def _generate_and_store(call_sid: str, transcript: str) -> None:
    full_reply = ""
    phone = call_phone_map.get(call_sid, "")
    caller_info = call_caller_info.get(call_sid, {})
    config = call_config.get(call_sid)
    async for part, text in stream_response_parts(call_sid, transcript, phone, caller_info, config):
        if part == "transfer":
            call_transfer_map[call_sid] = text
            pending_rest[call_sid] = ""  # unblock /call/continue
            print(f"[TRANSFER] Transferring {call_sid} to {text}", flush=True)
            break
        elif part == "end_call":
            call_hangup_set.add(call_sid)
            pending_rest[call_sid] = ""  # unblock /call/continue so final message plays
            print(f"[HANGUP] Scheduled hangup for {call_sid}", flush=True)
            break
        elif part == "first":
            pending_first[call_sid] = text
            full_reply = text
            # Pre-generate ElevenLabs audio in parallel while Claude finishes the rest
            asyncio.create_task(_pregenerate_audio(call_sid, text))
            print(f"[LLM] First sentence for {call_sid}: {text}", flush=True)
        elif part == "rest":
            pending_rest[call_sid] = text
            if text:
                full_reply = full_reply + " " + text
            print(f"[LLM] Complete for {call_sid}: {full_reply[:80]}", flush=True)

    async with get_db_context() as db:
        await append_transcript(db, call_sid, transcript, full_reply)


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
        endpointing=300,
        interim_results=True,
        smart_format=True,
        numerals=True,
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
                    t0 = time.time()
                    transcript = final_transcript[0]
                    transcript_event.clear()
                    print(f"[STT] Transcript: {transcript}", flush=True)

                    await dg.finish()

                    # Mark slots as pending and kick off Claude streaming in background
                    pending_first[call_sid] = None
                    pending_rest[call_sid] = None
                    asyncio.create_task(_generate_and_store(call_sid, transcript))

                    # Redirect Twilio to poll for first sentence (no "one moment please")
                    redirect_url = settings.base_url + "/call/response"
                    hold_twiml = (
                        '<?xml version="1.0" encoding="UTF-8"?>'
                        "<Response>"
                        f"<Redirect>{redirect_url}</Redirect>"
                        "</Response>"
                    )
                    await _update_twilio_call(call_sid, hold_twiml)
                    print(f"[STREAM] Redirect sent in {time.time()-t0:.2f}s", flush=True)
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
