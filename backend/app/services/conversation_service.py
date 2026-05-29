from anthropic import AsyncAnthropic

from app.core.config import settings
from app.services.document_service import search_documents

SYSTEM_PROMPT = """You are Cleo, the AI receptionist for Apex Home Services, a licensed HVAC, plumbing, and electrical company based in Austin, Texas.

Your job on this phone call:
- Answer questions about Apex's services, pricing, availability, and policies
- Help callers book appointments
- Be friendly, professional, and brief — this is a phone call, not a chat

Rules:
- Only use information from the context provided. Never invent prices, services, or policies.
- If something is not in the context, say you will have a human team member follow up.
- Keep responses to 2-3 sentences max. Phone callers do not want to hear an essay.
- Do not say "based on the context" or mention the knowledge base. Just answer naturally.
- Never use markdown formatting. No asterisks, no bold, no bullet points. Plain spoken English only."""

_sessions: dict[str, list[dict]] = {}

_client: AsyncAnthropic | None = None


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


async def get_response(session_id: str, user_message: str) -> str:
    context_chunks = await search_documents(user_message, limit=3)
    context = "\n\n".join(chunk["text"] for chunk in context_chunks)

    augmented_message = f"Relevant Apex knowledge:\n{context}\n\nCaller said: {user_message}"

    history = _sessions.get(session_id, [])
    history = history + [{"role": "user", "content": augmented_message}]

    client = _get_client()
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=history,
    )

    reply = response.content[0].text

    _sessions[session_id] = history + [{"role": "assistant", "content": reply}]

    return reply


def clear_session(session_id: str) -> None:
    _sessions.pop(session_id, None)
