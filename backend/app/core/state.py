# Shared in-memory state between stream and call handlers
pending_responses: dict[str, str | None] = {}  # legacy, kept for safety

# Streaming TTS state: set incrementally as Claude streams
pending_first: dict[str, str | None] = {}  # first sentence, None = not yet ready
pending_rest: dict[str, str | None] = {}   # remainder, None = still generating
