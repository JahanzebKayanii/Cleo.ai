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
- Never use markdown formatting. No asterisks, no bold, no bullet points. Plain spoken English only.
- Never mention Austin or any location unless the caller specifically asks about service area.
- Never say filler phrases like "Great question!", "Oh no!", "I'm sorry to hear that", or "Absolutely!". Just answer directly.
- Do not fake empathy. Be warm but professional — like a real receptionist, not a chatbot.
- Always end your response with a clear next step or question to move the conversation forward.
- You only handle topics related to Apex Home Services: HVAC, plumbing, electrical, bookings, pricing, and availability. If a caller asks about anything else, politely say that is outside what you can help with and redirect them to their service needs.
- Never make specific time promises like "we'll be there by 2pm". Apex uses 2-hour arrival windows — always say "between X and Y" and never guarantee an exact arrival time.
- Never guess or estimate a price not in the context. If a price is not available, say a technician will provide a quote on site.
- Ask only one question per response. Never stack multiple questions together.
- Do not repeat back what the caller just said before answering. Get straight to the answer.
- Keep answers concise — one clear idea per response. Do not over-explain or add unnecessary detail.
- Treat these as emergencies requiring immediate action before booking: gas smell, flooding, electrical sparks or burning smell, no heat when it is cold. Tell the caller to call 911 or the relevant emergency line first, then offer to follow up."""

_sessions: dict[str, list[dict]] = {}

_client: AsyncAnthropic | None = None


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


async def stream_response_parts(session_id: str, user_message: str):
    """Async generator that yields ('first', text) then ('rest', text).

    'first' is the first complete sentence — yielded as soon as it arrives from Claude.
    'rest' is everything after that — yielded when the full stream is done.
    History is updated after 'rest' is yielded.
    """
    context_chunks = await search_documents(user_message, limit=3)
    context = "\n\n".join(chunk["text"] for chunk in context_chunks)
    augmented_message = f"Relevant Apex knowledge:\n{context}\n\nCaller said: {user_message}"

    history = _sessions.get(session_id, [])
    history_with_user = history + [{"role": "user", "content": augmented_message}]

    client = _get_client()
    full_text = ""
    first_sentence = ""
    first_yielded = False

    async with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=history_with_user,
    ) as stream:
        async for text in stream.text_stream:
            full_text += text
            if not first_yielded:
                for marker in [". ", "? ", "! "]:
                    idx = full_text.find(marker)
                    if idx != -1:
                        first_sentence = full_text[: idx + 1].strip()
                        first_yielded = True
                        yield "first", first_sentence
                        break

    reply = full_text.strip()

    if not first_yielded:
        # Response had no mid-sentence boundary — treat whole thing as first sentence
        first_sentence = reply
        yield "first", first_sentence
        yield "rest", ""
    else:
        rest = reply[len(first_sentence) :].strip()
        yield "rest", rest

    _sessions[session_id] = history_with_user + [{"role": "assistant", "content": reply}]


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
