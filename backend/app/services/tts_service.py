import asyncio
import hashlib
from pathlib import Path

import httpx

from app.core.config import settings

AUDIO_DIR = Path("/tmp/cleo_audio")
AUDIO_DIR.mkdir(exist_ok=True)


async def text_to_speech(text: str) -> str:
    filename = hashlib.md5(text.encode()).hexdigest() + ".mp3"
    filepath = AUDIO_DIR / filename

    if filepath.exists():
        return filename

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{settings.elevenlabs_voice_id}"
    headers = {
        "xi-api-key": settings.elevenlabs_api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        filepath.write_bytes(response.content)

    return filename
