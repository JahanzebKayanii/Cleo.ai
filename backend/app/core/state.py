# Shared in-memory state between stream and call handlers
pending_responses: dict[str, str | None] = {}
