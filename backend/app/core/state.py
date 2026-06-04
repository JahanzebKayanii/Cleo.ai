# Shared in-memory state between stream and call handlers
pending_responses: dict[str, str | None] = {}  # legacy, kept for safety

# Streaming TTS state: set incrementally as Claude streams
pending_first: dict[str, str | None] = {}  # first sentence, None = not yet ready
pending_rest: dict[str, str | None] = {}   # remainder, None = still generating

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
