import asyncio

import httpx
from deepgram import DeepgramClient, PrerecordedOptions

from app.core.config import settings

_client: DeepgramClient | None = None


def _get_deepgram() -> DeepgramClient:
    global _client
    if _client is None:
        _client = DeepgramClient(settings.deepgram_api_key)
    return _client


async def transcribe_twilio_recording(recording_url: str) -> str:
    audio_url = recording_url + ".wav"

    async with httpx.AsyncClient(timeout=30) as http:
        response = await http.get(
            audio_url,
            auth=(settings.twilio_account_sid, settings.twilio_auth_token),
        )
        response.raise_for_status()
        audio_bytes = response.content

    deepgram = _get_deepgram()
    options = PrerecordedOptions(model="nova-2", language="en", smart_format=True)

    result = await asyncio.to_thread(
        deepgram.listen.rest.v("1").transcribe_file,
        {"buffer": audio_bytes},
        options,
    )

    transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
    return transcript.strip()
