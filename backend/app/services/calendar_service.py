import asyncio
import base64
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.core.config import settings

TIMEZONE = ZoneInfo("America/Chicago")
BUSINESS_START = 8
BUSINESS_END = 18
SLOT_HOURS = 2

_SCOPES = ["https://www.googleapis.com/auth/calendar"]


def _get_service():
    json_str = base64.b64decode(settings.google_service_account_b64).decode()
    info = json.loads(json_str)
    creds = service_account.Credentials.from_service_account_info(info, scopes=_SCOPES)
    return build("calendar", "v3", credentials=creds)


def _fmt_time(dt: datetime) -> str:
    h = dt.hour % 12 or 12
    m = f":{dt.strftime('%M')}" if dt.minute else ""
    ampm = "AM" if dt.hour < 12 else "PM"
    return f"{h}{m} {ampm}"


def _slot_display(start: datetime, end: datetime) -> str:
    return f"{_fmt_time(start)} to {_fmt_time(end)}"


async def get_todays_appointments() -> list[dict]:
    today = datetime.now(TIMEZONE)
    time_min = today.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    time_max = today.replace(hour=23, minute=59, second=59, microsecond=0).isoformat()

    def _list():
        svc = _get_service()
        return (
            svc.events()
            .list(
                calendarId=settings.google_calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

    result = await asyncio.to_thread(_list)
    appointments = []
    for event in result.get("items", []):
        desc = event.get("description", "")
        phone = ""
        service = ""
        for line in desc.split("\n"):
            if line.startswith("Phone:"):
                phone = line.replace("Phone:", "").strip()
            elif line.startswith("Service:"):
                service = line.replace("Service:", "").strip()

        summary = event.get("summary", "")
        customer_name = summary.split("–", 1)[1].strip() if "–" in summary else ""

        start_str = event.get("start", {}).get("dateTime", "")
        end_str = event.get("end", {}).get("dateTime", "")
        window = ""
        if start_str and end_str:
            s = datetime.fromisoformat(start_str).astimezone(TIMEZONE)
            e = datetime.fromisoformat(end_str).astimezone(TIMEZONE)
            window = _slot_display(s, e)

        appointments.append(
            {"phone": phone, "customer_name": customer_name, "service": service, "window": window}
        )
    return appointments


async def get_available_slots(date_str: str) -> list[dict]:
    date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=TIMEZONE)

    all_slots = []
    t = date.replace(hour=BUSINESS_START, minute=0, second=0, microsecond=0)
    while t.hour + SLOT_HOURS <= BUSINESS_END:
        end = t + timedelta(hours=SLOT_HOURS)
        all_slots.append((t, end))
        t = end

    time_min = date.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    time_max = date.replace(hour=23, minute=59, second=59, microsecond=0).isoformat()

    def _query():
        svc = _get_service()
        body = {
            "timeMin": time_min,
            "timeMax": time_max,
            "items": [{"id": settings.google_calendar_id}],
            "timeZone": "America/Chicago",
        }
        return svc.freebusy().query(body=body).execute()

    result = await asyncio.to_thread(_query)
    busy = (
        result.get("calendars", {})
        .get(settings.google_calendar_id, {})
        .get("busy", [])
    )

    available = []
    for slot_start, slot_end in all_slots:
        overlap = any(
            slot_start < datetime.fromisoformat(b["end"]).astimezone(TIMEZONE)
            and slot_end > datetime.fromisoformat(b["start"]).astimezone(TIMEZONE)
            for b in busy
        )
        if not overlap:
            available.append(
                {
                    "display": _slot_display(slot_start, slot_end),
                    "start_24h": slot_start.strftime("%H:%M"),
                }
            )

    return available


async def book_appointment(
    date_str: str,
    start_time_24h: str,
    service: str,
    customer_name: str,
    customer_phone: str,
    notes: str = "",
) -> dict:
    date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=TIMEZONE)
    h, m = map(int, start_time_24h.split(":"))
    start = date.replace(hour=h, minute=m, second=0, microsecond=0)
    end = start + timedelta(hours=SLOT_HOURS)

    def _create():
        svc = _get_service()
        event = {
            "summary": f"{service} – {customer_name}",
            "description": f"Phone: {customer_phone}\nService: {service}" + (f"\nIssue: {notes}" if notes else ""),
            "start": {"dateTime": start.isoformat(), "timeZone": "America/Chicago"},
            "end": {"dateTime": end.isoformat(), "timeZone": "America/Chicago"},
        }
        return svc.events().insert(
            calendarId=settings.google_calendar_id, body=event
        ).execute()

    await asyncio.to_thread(_create)

    date_display = date.strftime("%A, %B %-d")
    window = _slot_display(start, end)

    if customer_phone:
        from app.services.sms_service import send_confirmation_sms
        await send_confirmation_sms(customer_phone, customer_name, date_display, window, service)

    return {
        "success": True,
        "date": date_display,
        "window": window,
        "service": service,
        "customer_name": customer_name,
    }
