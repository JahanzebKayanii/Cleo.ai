import json
from datetime import datetime
from zoneinfo import ZoneInfo

from anthropic import AsyncAnthropic

from app.core.config import settings
from app.services.document_service import search_documents

_SYSTEM_PROMPT_TEMPLATE = """You are Cleo, the AI receptionist for Apex Home Services, a licensed HVAC, plumbing, and electrical company based in Austin, Texas.

Your job on this phone call:
- Answer questions about Apex's services, pricing, availability, and policies
- Help callers book appointments by checking the calendar and confirming a slot
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
- Treat these as emergencies requiring immediate action before booking: gas smell, flooding, electrical sparks or burning smell, no heat when it is cold. Tell the caller to call 911 or the relevant emergency line first, then offer to follow up.

Booking appointments:
- Booking flow — follow these steps in order, one at a time:
  1. Ask about the problem: "What's going on with your [service]?" Get a description before anything else.
  2. Ask for their preferred date.
  3. Ask for their name, then spell it back letter by letter to confirm — for example: "Just to confirm, is that J-O-H-N S-M-I-T-H?" Wait for confirmation before proceeding.
  4. Call check_availability with the date.
  5. Present the available windows.
  6. Once they pick a slot, call book_appointment.
- Never skip step 1. Never ask for the date or name before you have a problem description.
- Use the check_availability tool to find open slots. If nothing is available on that date, ask for an alternative.
- Present available windows naturally, for example: "We have openings from 8 to 10 AM, 10 AM to noon, and 2 to 4 PM. Which works best for you?"
- Once the caller confirms a specific window, immediately use the book_appointment tool, including the problem description in the notes field.
- After booking succeeds, confirm the details: date, window, and service. Keep it short.
- Apex schedules Monday through Friday, 8 AM to 6 PM Central Time.
- If the caller gives a date in the past (before today), tell them that date has already passed and ask for a future date.
- If the caller gives a Saturday or Sunday, let them know Apex only schedules Monday through Friday and ask for a weekday.
- If the caller gives a vague date like "sometime next week" or "next Monday or Tuesday", ask them to pick one specific date before calling check_availability.
- If check_availability returns no available slots, let the caller know that date is fully booked and ask them to try the next business day or suggest an alternative.
- Today is {today}. Current time: {current_time} Central Time.

After-hours calls (outside Monday–Friday 8 AM to 6 PM Central Time):
- Let the caller know the office is currently closed.
- Tell them the next available time to call back (next business day at 8 AM).
- Offer to take their name and a brief message so a technician can call them back during business hours.
- Do not attempt to book appointments after hours.
- For true emergencies (gas smell, flooding, electrical sparks or burning smell, no heat in very cold weather), still direct them to 911 first, then take their info for a callback."""


def _is_business_hours() -> bool:
    now = datetime.now(ZoneInfo("America/Chicago"))
    if now.weekday() >= 5:
        return False
    return 8 <= now.hour < 18


def _system_prompt(caller_info: dict | None = None) -> str:
    now = datetime.now(ZoneInfo("America/Chicago"))
    today = now.strftime("%A, %B %-d, %Y")
    current_time = now.strftime("%-I:%M %p")
    prompt = _SYSTEM_PROMPT_TEMPLATE.format(today=today, current_time=current_time)
    if caller_info and caller_info.get("name"):
        name = caller_info["name"]
        summaries = caller_info.get("summaries", [])
        context_lines = [f"Returning caller context: You already know this caller's name is {name}. Do not ask for their name again — you already have it."]
        if summaries:
            context_lines.append("Their recent call history:")
            for s in summaries:
                context_lines.append(f"- {s}")
        prompt += "\n\n" + "\n".join(context_lines)
    return prompt


TOOLS = [
    {
        "name": "check_availability",
        "description": "Check available 2-hour appointment slots for a given date. Use this when the caller wants to book and has provided a date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format (Austin TX timezone)",
                }
            },
            "required": ["date"],
        },
    },
    {
        "name": "book_appointment",
        "description": "Book a confirmed appointment on the calendar. Only call this after the caller has agreed to a specific time window.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format",
                },
                "start_time": {
                    "type": "string",
                    "description": "Slot start time in HH:MM 24-hour format, e.g. '08:00' or '14:00'",
                },
                "service": {
                    "type": "string",
                    "description": "Service type: HVAC, plumbing, or electrical",
                },
                "customer_name": {
                    "type": "string",
                    "description": "Customer full name",
                },
                "notes": {
                    "type": "string",
                    "description": "Brief description of the problem the customer described",
                },
            },
            "required": ["date", "start_time", "service", "customer_name", "notes"],
        },
    },
]


async def _execute_tool(name: str, inputs: dict, caller_phone: str) -> dict:
    from app.services.calendar_service import book_appointment, get_available_slots

    if name == "check_availability":
        slots = await get_available_slots(inputs["date"])
        if not slots:
            return {"available": False, "message": "No slots available on that date."}
        return {"available": True, "slots": slots}

    if name == "book_appointment":
        result = await book_appointment(
            date_str=inputs["date"],
            start_time_24h=inputs["start_time"],
            service=inputs["service"],
            customer_name=inputs["customer_name"],
            customer_phone=caller_phone,
            notes=inputs.get("notes", ""),
        )
        if result.get("success") and caller_phone:
            from app.core.database import get_db_context
            from app.services.customer_service import update_customer_name
            async with get_db_context() as db:
                await update_customer_name(db, caller_phone, inputs["customer_name"])
        return result

    return {"error": f"Unknown tool: {name}"}


_sessions: dict[str, list[dict]] = {}

_client: AsyncAnthropic | None = None


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


async def stream_response_parts(
    session_id: str, user_message: str, caller_phone: str = "", caller_info: dict | None = None
):
    """Async generator: yields ('first', text) then ('rest', text).

    Handles Claude tool use transparently — calendar checks happen between
    the first and rest yields so the caller hears a quick reply immediately.
    """
    context_chunks = await search_documents(user_message, limit=3)
    context = "\n\n".join(chunk["text"] for chunk in context_chunks)
    augmented_message = f"Relevant Apex knowledge:\n{context}\n\nCaller said: {user_message}"

    history = _sessions.get(session_id, [])
    history_with_user = history + [{"role": "user", "content": augmented_message}]

    client = _get_client()
    full_text = ""
    first_yielded = False
    first_sentence = ""

    async with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=_system_prompt(caller_info),
        messages=history_with_user,
        tools=TOOLS,
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

        final_msg = await stream.get_final_message()

    if final_msg.stop_reason == "tool_use":
        # Execute all tools Claude requested
        tool_results = []
        for block in final_msg.content:
            if block.type == "tool_use":
                result = await _execute_tool(block.name, block.input, caller_phone)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    }
                )

        # Build assistant message with all content blocks as dicts
        assistant_content = []
        for block in final_msg.content:
            if block.type == "text":
                assistant_content.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                assistant_content.append(
                    {
                        "type": "tool_use",
                        "id": block.id,
                        "name": block.name,
                        "input": block.input,
                    }
                )

        msgs_with_tools = history_with_user + [
            {"role": "assistant", "content": assistant_content},
            {"role": "user", "content": tool_results},
        ]

        # Second streaming call — Claude sees the tool results and responds
        second_text = ""
        async with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=300,
            system=_system_prompt(caller_info),
            messages=msgs_with_tools,
        ) as stream2:
            async for text in stream2.text_stream:
                second_text += text
                if not first_yielded:
                    for marker in [". ", "? ", "! "]:
                        idx = second_text.find(marker)
                        if idx != -1:
                            first_sentence = second_text[: idx + 1].strip()
                            first_yielded = True
                            yield "first", first_sentence
                            break

        if not first_yielded:
            yield "first", second_text.strip()
            yield "rest", ""
        else:
            # Determine where the rest begins
            if first_sentence and first_sentence in second_text:
                rest = second_text[len(first_sentence) :].strip()
            else:
                # first_sentence came from pre-tool text; rest = all of second_text
                rest = second_text.strip()
            yield "rest", rest

        reply = (full_text.strip() + " " + second_text.strip()).strip()
        _sessions[session_id] = msgs_with_tools + [
            {"role": "assistant", "content": second_text.strip()}
        ]

    else:
        # No tool use — normal path
        reply = full_text.strip()
        if not first_yielded:
            yield "first", reply
            yield "rest", ""
        else:
            rest = reply[len(first_sentence) :].strip()
            yield "rest", rest
        _sessions[session_id] = history_with_user + [
            {"role": "assistant", "content": reply}
        ]


async def get_response(
    session_id: str, user_message: str, caller_phone: str = "", caller_info: dict | None = None
) -> str:
    context_chunks = await search_documents(user_message, limit=3)
    context = "\n\n".join(chunk["text"] for chunk in context_chunks)
    augmented_message = f"Relevant Apex knowledge:\n{context}\n\nCaller said: {user_message}"

    history = _sessions.get(session_id, [])
    history_with_user = history + [{"role": "user", "content": augmented_message}]

    client = _get_client()
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=_system_prompt(caller_info),
        messages=history_with_user,
        tools=TOOLS,
    )

    if response.stop_reason == "tool_use":
        tool_results = []
        assistant_content = []
        for block in response.content:
            if block.type == "text":
                assistant_content.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                print(f"[TOOL] {block.name} called with {json.dumps(block.input)}", flush=True)
                assistant_content.append(
                    {"type": "tool_use", "id": block.id, "name": block.name, "input": block.input}
                )
                result = await _execute_tool(block.name, block.input, caller_phone)
                print(f"[TOOL] {block.name} result: {json.dumps(result)}", flush=True)
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)}
                )

        msgs_with_tools = history_with_user + [
            {"role": "assistant", "content": assistant_content},
            {"role": "user", "content": tool_results},
        ]
        response2 = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            system=_system_prompt(caller_info),
            messages=msgs_with_tools,
        )
        reply = response2.content[0].text
        _sessions[session_id] = msgs_with_tools + [{"role": "assistant", "content": reply}]
    else:
        reply = response.content[0].text
        _sessions[session_id] = history_with_user + [{"role": "assistant", "content": reply}]

    return reply


def clear_session(session_id: str) -> None:
    _sessions.pop(session_id, None)
