import asyncio
import json

from anthropic import AsyncAnthropic

from app.core.config import settings
from app.services.integrations.base import CallData

_client: AsyncAnthropic | None = None


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


async def extract_call_data(customer_name: str | None, customer_phone: str, transcript: str, summary: str) -> CallData:
    prompt = f"""Extract structured data from this call transcript and return ONLY valid JSON.

Transcript:
{transcript}

Summary:
{summary}

Return JSON with exactly these fields:
{{
  "customer_name": "full name or empty string",
  "service_type": "HVAC or plumbing or electrical or other",
  "issue_description": "brief description of the problem",
  "booked": true or false,
  "appointment_date": "YYYY-MM-DD or null",
  "appointment_time": "time window string or null",
  "address": "full service address or empty string"
}}"""

    response = await _get_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    try:
        text = response.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        d = json.loads(text.strip())
    except Exception:
        d = {}

    return CallData(
        customer_name=customer_name or d.get("customer_name", ""),
        customer_phone=customer_phone,
        service_type=d.get("service_type", "other"),
        issue_description=d.get("issue_description", ""),
        booked=d.get("booked", False),
        appointment_date=d.get("appointment_date"),
        appointment_time=d.get("appointment_time"),
        call_summary=summary,
        address=d.get("address", ""),
    )


async def push_to_integrations(
    customer_name: str | None,
    customer_phone: str,
    transcript: str,
    summary: str,
    config: dict,
) -> None:
    if not transcript or not summary:
        return

    call_data = await extract_call_data(customer_name, customer_phone, transcript, summary)

    tasks = []

    if config.get("hubspot_token"):
        from app.services.integrations import hubspot
        tasks.append(_safe_push("HubSpot", hubspot.push(call_data, config["hubspot_token"])))

    if config.get("jobber_api_key"):
        from app.services.integrations import jobber
        tasks.append(_safe_push("Jobber", jobber.push(call_data, config)))

    if config.get("housecall_pro_api_key"):
        from app.services.integrations import housecall_pro
        tasks.append(_safe_push("HousecallPro", housecall_pro.push(call_data, config["housecall_pro_api_key"])))

    if tasks:
        await asyncio.gather(*tasks)
        print(f"[Integrations] {len(tasks)} integration(s) pushed for {customer_phone}", flush=True)


async def _safe_push(name: str, coro) -> None:
    try:
        await coro
    except Exception as e:
        print(f"[Integrations] {name} failed: {e}", flush=True)
