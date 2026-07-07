import hashlib
import re
from pathlib import Path

import httpx

from app.core.config import settings

AUDIO_DIR = Path("/tmp/cleo_audio")
AUDIO_DIR.mkdir(exist_ok=True)

_ORDINAL_MAP: dict[int, str] = {
    1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth",
    6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth",
    11: "eleventh", 12: "twelfth", 13: "thirteenth", 14: "fourteenth",
    15: "fifteenth", 16: "sixteenth", 17: "seventeenth", 18: "eighteenth",
    19: "nineteenth", 20: "twentieth", 21: "twenty-first", 22: "twenty-second",
    23: "twenty-third", 24: "twenty-fourth", 25: "twenty-fifth", 26: "twenty-sixth",
    27: "twenty-seventh", 28: "twenty-eighth", 29: "twenty-ninth", 30: "thirtieth",
    31: "thirty-first", 32: "thirty-second", 33: "thirty-third", 34: "thirty-fourth",
    40: "fortieth", 41: "forty-first", 42: "forty-second", 43: "forty-third",
    50: "fiftieth", 51: "fifty-first", 52: "fifty-second", 53: "fifty-third",
    60: "sixtieth", 70: "seventieth", 80: "eightieth", 90: "ninetieth",
    100: "one hundredth",
}

_DIGIT_WORDS = {"0": "oh", "1": "one", "2": "two", "3": "three", "4": "four",
                "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}


def _normalize_for_tts(text: str) -> str:
    # Ordinals: 42nd → forty-second, 1st → first, etc.
    def _expand_ordinal(m: re.Match) -> str:
        n = int(m.group(1))
        return _ORDINAL_MAP.get(n, m.group(0))

    text = re.sub(r"\b(\d{1,3})(?:st|nd|rd|th)\b", _expand_ordinal, text, flags=re.IGNORECASE)

    # 4-5 digit numbers (street numbers): 14202 → "one four two oh two"
    def _expand_street_number(m: re.Match) -> str:
        return " ".join(_DIGIT_WORDS[c] for c in m.group(0))

    text = re.sub(r"\b\d{4,5}\b", _expand_street_number, text)

    return text


async def text_to_speech(text: str) -> str:
    """Generate speech via ElevenLabs. Returns cached MP3 filename."""
    text = _normalize_for_tts(text)
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
        "model_id": "eleven_flash_v2_5",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.80,
            "style": 0.0,
            "use_speaker_boost": True,
        },
        "output_format": "mp3_22050_32",
    }

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        filepath.write_bytes(response.content)

    return filename
