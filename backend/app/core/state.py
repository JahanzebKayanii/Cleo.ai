# Shared in-memory state between stream and call handlers
pending_responses: dict[str, str | None] = {}  # legacy, kept for safety

# Streaming TTS state: set incrementally as Claude streams
pending_first: dict[str, str | None] = {}  # first sentence, None = not yet ready
pending_rest: dict[str, str | None] = {}   # remainder, None = still generating

# Phone number lookup so the call handler can pass it to booking tools
call_phone_map: dict[str, str] = {}  # call_sid -> caller E.164 phone number

# Returning caller info: name + recent call summaries, populated on /incoming
call_caller_info: dict[str, dict] = {}  # call_sid -> {name, summaries}
