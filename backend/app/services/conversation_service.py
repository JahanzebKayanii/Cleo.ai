import json
from datetime import datetime
from zoneinfo import ZoneInfo

from anthropic import AsyncAnthropic

from app.core.config import settings
from app.services.document_service import search_documents

_SYSTEM_PROMPT_TEMPLATE = """You are Cleo, the AI receptionist for Apex Home Services, a licensed HVAC, plumbing, and electrical company based in Austin, Texas.

Your job on this phone call:
- Answer questions about {biz_name_placeholder}'s services, pricing, availability, and policies
- Help callers book appointments by checking the calendar and confirming a slot
- Be friendly, professional, and brief — this is a phone call, not a chat

Rules:
- Only use information from the context provided. Never invent prices, services, or policies.
- If something is not in the context, say you will have a human team member follow up.
- Keep responses to 2-3 sentences max. Phone callers do not want to hear an essay.
- Your first sentence must be 10 words or fewer — no exceptions. If you cannot say the key point in 10 words, split it: short opener first, details in the next sentence. Never open with a sentence that contains a name, date, address, and detail all at once. Good: "Your appointment is confirmed for tomorrow." then the time and address after. Bad: "I have your appointment confirmed for Wednesday July 8th between 4 and 6 PM at 14202 42nd Street."
- Do not say "based on the context" or mention the knowledge base. Just answer naturally.
- Never use markdown formatting. No asterisks, no bold, no bullet points. Plain spoken English only.
- Never mention Austin or any location unless the caller specifically asks about service area.
- Never say filler phrases like "Great question!", "Oh no!", "I'm sorry to hear that", or "Absolutely!". Just answer directly.
- Do not fake empathy. Be warm but professional — like a real receptionist, not a chatbot.
- Always end your response with a clear next step or question to move the conversation forward.
- You only handle topics related to Apex Home Services: HVAC, plumbing, electrical, bookings, pricing, and availability. If a caller asks about anything else, politely say that is outside what you can help with and redirect them to their service needs.
- Never make specific time promises like "we'll be there by 2pm". {biz_name_placeholder} uses 2-hour arrival windows — always say "between X and Y" and never guarantee an exact arrival time.
- Never guess or estimate a price not in the context. If a price is not available, say a technician will provide a quote on site.
- Ask only one question per response. Never stack multiple questions together.
- Do not repeat back what the caller just said before answering. Get straight to the answer.
- Keep answers concise — one clear idea per response. Do not over-explain or add unnecessary detail.
- Treat these as emergencies requiring immediate action before booking: gas smell, flooding, electrical sparks or burning smell, no heat when it is cold. Tell the caller to call 911 or the relevant emergency line first, then offer to follow up.
- When a caller requests something you cannot do directly (modifying a booking, billing questions, complaints), tell them a team member will follow up, ask if there is anything else you can help with, and call end_call once they confirm there is nothing more. Do not keep the call open waiting for them to say goodbye.
- Cancellation flow: when a caller wants to cancel an appointment, call find_appointments. If none found, tell them and offer to help with anything else. If one found, read back the date, time, and service, ask "Shall I go ahead and cancel that?" and if they confirm, call cancel_appointment. If multiple found, list them briefly and ask which one. After a successful cancellation, confirm it is done, ask if there is anything else, then call end_call.

Booking appointments:
- Booking flow — follow these steps in order, one at a time:
  1. Ask about the problem: "What's going on with your [service]?" Get a description before anything else.
  2. Ask for their preferred date.
  3. Ask for their name, then spell it back letter by letter to confirm — for example: "Just to confirm, is that J-O-H-N S-M-I-T-H?" Wait for confirmation before proceeding.
  4. Ask for the service address: "And what's the address where you need the technician to come?" Get the full address including street number, street name, and city. If any part is missing, ask for it before continuing.
  5. Read the address back to confirm: "Just to confirm, the address is [address] — is that correct?" Wait for confirmation before proceeding. If any part of the address sounds unclear or unusual, ask the caller to spell out the street name letter by letter before reading it back.
  6. Call check_availability with the date.
  7. Present the available windows.
  8. Once they pick a slot, call book_appointment.
- Never skip step 1. Never ask for the date or name before you have a problem description.
- Never skip steps 4 and 5. The address must be collected and confirmed before checking availability.
- Address must include at minimum: a street number, a street name, and a city. If the caller gives an incomplete address (e.g. just a street with no city), ask for the missing parts before continuing.
- Service area: only book appointments for addresses within {service_area}. If the caller's address is outside this area, politely let them know you only service that area and cannot book for their location.
- Use the check_availability tool to find open slots. If nothing is available on that date, ask for an alternative.
- Present available windows naturally, for example: "We have openings from 8 to 10 AM, 10 AM to noon, and 2 to 4 PM. Which works best for you?"
- Once the caller confirms a specific window, immediately use the book_appointment tool, including the problem description in the notes field and the confirmed address in the address field.
- After booking succeeds, confirm the details: date, window, service, and address. Keep it short.
- {biz_name_placeholder} schedules Monday through Friday, 8 AM to 6 PM Central Time.
- If the caller gives a date in the past (before today), tell them that date has already passed and ask for a future date.
- If the caller gives a Saturday or Sunday, let them know {biz_name_placeholder} only schedules Monday through Friday and ask for a weekday.
- If the caller gives a vague date like "sometime next week" or "next Monday or Tuesday", ask them to pick one specific date before calling check_availability.
- If check_availability returns no available slots, let the caller know that date is fully booked and ask them to try the next business day or suggest an alternative.
- Today is {today}. Current time: {current_time} Central Time.
- Service area: {service_area}.

Live transfer:
- If the caller asks to speak to a human, a real person, or a manager — call transfer_to_human immediately. Do not try to talk them out of it.
- If the caller is clearly frustrated or upset — offer to transfer them: "I can transfer you to one of our team members right now if you'd like."
- Before calling transfer_to_human, always say something like: "Of course, let me transfer you to one of our team members right now. Please hold for just a moment."
- If no transfer number is configured, apologize and offer to take a message.

After-hours calls (outside Monday–Friday 8 AM to 6 PM Central Time):
- Let the caller know the office is currently closed.
- Tell them the next available time to call back (next business day at 8 AM).
- Offer to take their name and a brief message so a technician can call them back during business hours.
- Do not attempt to book appointments after hours.
- For true emergencies (gas smell, flooding, electrical sparks or burning smell, no heat in very cold weather), still direct them to 911 first, then take their info for a callback."""


def _is_business_hours(config: dict | None = None) -> bool:
    tz = ZoneInfo(config["timezone"] if config else "America/Chicago")
    now = datetime.now(tz)
    if now.weekday() >= 5:
        return False
    open_h = config["hours_open"] if config else 8
    close_h = config["hours_close"] if config else 18
    return open_h <= now.hour < close_h


def _system_prompt(caller_info: dict | None = None, config: dict | None = None) -> str:
    tz = ZoneInfo(config["timezone"] if config else "America/Chicago")
    now = datetime.now(tz)
    today = now.strftime("%A, %B %-d, %Y")
    current_time = now.strftime("%-I:%M %p")
    service_area = config.get("service_area", "Austin, TX and surrounding areas") if config else "Austin, TX and surrounding areas"

    if config:
        services = ", ".join(config.get("services") or ["HVAC", "plumbing", "electrical"])
        biz_name = config.get("name") or "Apex Home Services"
        biz_desc = config.get("description") or "a licensed HVAC, plumbing, and electrical company based in Austin, Texas"
        open_h = config.get("hours_open", 8)
        close_h = config.get("hours_close", 18)
        open_str = f"{open_h % 12 or 12} {'AM' if open_h < 12 else 'PM'}"
        close_str = f"{close_h % 12 or 12} {'AM' if close_h < 12 else 'PM'}"
        template = _SYSTEM_PROMPT_TEMPLATE.replace(
            "Apex Home Services, a licensed HVAC, plumbing, and electrical company based in Austin, Texas",
            f"{biz_name}, {biz_desc}",
        ).replace(
            "HVAC, plumbing, and electrical",
            services,
        ).replace(
            "Apex Home Services: HVAC, plumbing, electrical, bookings, pricing, and availability",
            f"{biz_name}: {services}, bookings, pricing, and availability",
        ).replace(
            "8 AM to 6 PM Central Time",
            f"{open_str} to {close_str} Central Time",
        ).replace(
            "Monday through Friday, 8 AM to 6 PM Central Time",
            f"Monday through Friday, {open_str} to {close_str} Central Time",
        ).replace(
            "{biz_name_placeholder}",
            biz_name,
        )
    else:
        template = _SYSTEM_PROMPT_TEMPLATE.replace("{biz_name_placeholder}", "Apex Home Services")

    prompt = template.format(today=today, current_time=current_time, service_area=service_area)
    custom_instructions = (config or {}).get("custom_instructions", "")
    if custom_instructions:
        prompt += f"\n\nAdditional instructions for this business:\n{custom_instructions}"
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
        "name": "transfer_to_human",
        "description": "Transfer the caller to a live team member. Call this when: the caller asks to speak to a human or real person, the caller is clearly frustrated or upset, or the request is too complex to handle.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "end_call",
        "description": "End the phone call. Call this after: a booking is confirmed and you have read back all details, the caller says goodbye or thanks and there is nothing left to do, the caller indicates they are done, or you have noted a request to pass to the team (cancellation, modification, complaint) and the caller has no further needs. Always deliver your final message before calling this tool.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "find_appointments",
        "description": "Find upcoming appointments for the current caller. Call this when a caller wants to cancel or asks about their existing appointment.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "cancel_appointment",
        "description": "Cancel a specific appointment by its event ID. Only call this after the caller has confirmed which appointment to cancel. Always read back the appointment details before calling this.",
        "input_schema": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "The event_id from find_appointments"}
            },
            "required": ["event_id"],
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
                "address": {
                    "type": "string",
                    "description": "Full service address where the technician should go",
                },
            },
            "required": ["date", "start_time", "service", "customer_name", "notes", "address"],
        },
    },
]


async def _execute_tool(name: str, inputs: dict, caller_phone: str, config: dict | None = None) -> dict:
    from app.services.calendar_service import book_appointment, get_available_slots

    if name == "end_call":
        return {"end_call": True}

    if name == "find_appointments":
        from app.services.calendar_service import find_upcoming_appointments
        appointments = await find_upcoming_appointments(caller_phone, config)
        if not appointments:
            return {"found": False, "message": "No upcoming appointments found for this caller."}
        return {"found": True, "appointments": appointments}

    if name == "cancel_appointment":
        from app.services.calendar_service import cancel_appointment
        return await cancel_appointment(inputs["event_id"], config)

    if name == "transfer_to_human":
        phone = (config or {}).get("transfer_phone", "")
        if phone:
            return {"transfer": True, "phone": phone}
        return {"transfer": False, "message": "No transfer number configured. Please call back during business hours."}

    if name == "check_availability":
        slots = await get_available_slots(inputs["date"], config=config)
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
            address=inputs.get("address", ""),
            config=config,
        )
        if result.get("success") and caller_phone:
            from app.core.database import get_db_context
            from app.services.customer_service import update_customer_name
            biz_id = (config or {}).get("id", 1)
            async with get_db_context() as db:
                await update_customer_name(db, caller_phone, inputs["customer_name"], biz_id)
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
    session_id: str, user_message: str, caller_phone: str = "", caller_info: dict | None = None, config: dict | None = None
):
    """Async generator: yields ('first', text) then ('rest', text).

    Handles Claude tool use transparently — calendar checks happen between
    the first and rest yields so the caller hears a quick reply immediately.
    """
    collection = (config or {}).get("qdrant_collection") or None
    context_chunks = await search_documents(user_message, limit=3, collection=collection)
    context = "\n\n".join(chunk["text"] for chunk in context_chunks)
    biz_name = (config or {}).get("name", "the business")
    augmented_message = f"Relevant {biz_name} knowledge:\n{context}\n\nCaller said: {user_message}"

    history = _sessions.get(session_id, [])
    history_with_user = history + [{"role": "user", "content": augmented_message}]

    client = _get_client()
    full_text = ""
    first_yielded = False
    first_sentence = ""

    async with client.messages.stream(
        model="claude-sonnet-5",
        max_tokens=500,
        system=_system_prompt(caller_info, config),
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
        transfer_phone = None
        should_end = False
        for block in final_msg.content:
            if block.type == "tool_use":
                result = await _execute_tool(block.name, block.input, caller_phone, config)
                if result.get("transfer"):
                    transfer_phone = result.get("phone", "")
                if result.get("end_call"):
                    should_end = True
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    }
                )

        if transfer_phone is not None:
            if not first_yielded:
                yield "first", "Please hold while I transfer you to one of our team members."
            yield "transfer", transfer_phone
            return

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
            model="claude-sonnet-5",
            max_tokens=300,
            system=_system_prompt(caller_info, config),
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

        if should_end:
            yield "end_call", ""

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
    session_id: str, user_message: str, caller_phone: str = "", caller_info: dict | None = None, config: dict | None = None
) -> str:
    collection = (config or {}).get("qdrant_collection") or None
    context_chunks = await search_documents(user_message, limit=3, collection=collection)
    context = "\n\n".join(chunk["text"] for chunk in context_chunks)
    biz_name = (config or {}).get("name", "the business")
    augmented_message = f"Relevant {biz_name} knowledge:\n{context}\n\nCaller said: {user_message}"

    history = _sessions.get(session_id, [])
    history_with_user = history + [{"role": "user", "content": augmented_message}]

    client = _get_client()
    response = await client.messages.create(
        model="claude-sonnet-5",
        max_tokens=500,
        system=_system_prompt(caller_info, config),
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
                result = await _execute_tool(block.name, block.input, caller_phone, config)
                print(f"[TOOL] {block.name} result: {json.dumps(result)}", flush=True)
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)}
                )

        msgs_with_tools = history_with_user + [
            {"role": "assistant", "content": assistant_content},
            {"role": "user", "content": tool_results},
        ]
        response2 = await client.messages.create(
            model="claude-sonnet-5",
            max_tokens=300,
            system=_system_prompt(caller_info, config),
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
