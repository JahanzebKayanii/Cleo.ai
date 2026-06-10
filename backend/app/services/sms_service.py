import asyncio

from twilio.rest import Client as TwilioClient

from app.core.config import settings

_twilio_client: TwilioClient | None = None


def _get_client() -> TwilioClient:
    global _twilio_client
    if _twilio_client is None:
        _twilio_client = TwilioClient(settings.twilio_account_sid, settings.twilio_auth_token)
    return _twilio_client


async def send_sms(to: str, body: str) -> bool:
    if not to or not settings.twilio_phone_number:
        return False
    try:
        client = _get_client()
        await asyncio.to_thread(
            client.messages.create,
            body=body,
            from_=settings.twilio_phone_number,
            to=to,
        )
        print(f"[SMS] Sent to {to}: {body[:60]}", flush=True)
        return True
    except Exception as e:
        print(f"[SMS] Failed to send to {to}: {e}", flush=True)
        return False


async def send_confirmation_sms(
    phone: str,
    customer_name: str,
    date_display: str,
    window: str,
    service: str,
    business_name: str = "the business",
) -> None:
    first_name = customer_name.split()[0] if customer_name else "there"
    body = (
        f"Hi {first_name}, your {service} appointment with {business_name} "
        f"is confirmed for {date_display} from {window}. "
        "Questions? Call us back. Reply STOP to opt out."
    )
    await send_sms(phone, body)


async def send_morning_reminders() -> None:
    from app.core.database import get_db_context
    from app.services.business_service import list_businesses
    from app.services.calendar_service import get_todays_appointments

    async with get_db_context() as db:
        tenants = await list_businesses(db)

    for tenant in tenants:
        if not tenant.get("is_active"):
            continue
        if not tenant.get("google_calendar_id") and not tenant.get("id") == 1:
            continue  # skip tenants with no calendar configured

        appointments = await get_todays_appointments(config=tenant)
        print(f"[SMS] Tenant {tenant['id']} ({tenant['name']}): {len(appointments)} appointment(s) today", flush=True)

        for appt in appointments:
            phone = appt.get("phone", "")
            if not phone:
                continue
            first_name = (appt.get("customer_name") or "there").split()[0]
            window = appt.get("window", "")
            service = appt.get("service", "")
            biz_name = tenant.get("name", "us")
            body = (
                f"Hi {first_name}, just a reminder that your {service} appointment "
                f"with {biz_name} is today from {window}. See you soon! "
                "Reply STOP to opt out."
            )
            await send_sms(phone, body)
