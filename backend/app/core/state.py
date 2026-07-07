import time

# Shared in-memory state between stream and call handlers
pending_responses: dict[str, str | None] = {}  # legacy, kept for safety

# Streaming TTS state: set incrementally as Claude streams
pending_first: dict[str, str | None] = {}  # first sentence, None = not yet ready
pending_rest: dict[str, str | None] = {}   # remainder, None = still generating
pending_audio: dict[str, str | None] = {}  # ElevenLabs filename, None = generating, "" = failed

# Phone number lookup so the call handler can pass it to booking tools
call_phone_map: dict[str, str] = {}  # call_sid -> caller E.164 phone number

# Returning caller info: name + recent call summaries, populated on /incoming
call_caller_info: dict[str, dict] = {}  # call_sid -> {name, summaries}

# Business config cached per call so stream.py doesn't need DB access
call_config: dict[str, dict] = {}  # call_sid -> business config dict

# Set to transfer phone number when Claude requests a live transfer
call_transfer_map: dict[str, str] = {}  # call_sid -> transfer phone number

# Set when Claude signals the conversation is complete and Cleo should hang up
call_hangup_set: set[str] = set()  # call_sids pending hangup

# Track when each call was started so we can purge stale entries
# if Twilio never sends a final /call/status event (network failure, crash).
call_started_at: dict[str, float] = {}  # call_sid -> unix timestamp

_MAX_CALL_AGE = 60 * 60  # 1 hour — generous upper bound for a real call


def purge_stale_calls() -> None:
    now = time.time()
    stale = [sid for sid, ts in call_started_at.items() if now - ts > _MAX_CALL_AGE]
    for sid in stale:
        for d in (call_phone_map, call_caller_info, call_config, call_transfer_map,
                  pending_first, pending_rest, pending_audio, call_started_at):
            d.pop(sid, None)
        call_hangup_set.discard(sid)
