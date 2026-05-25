from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.appointment import Appointment

TIMEZONE = ZoneInfo("America/Chicago")  # Austin, TX

# Apex's 2-hour arrival windows (start hours in 24h)
SLOT_HOURS = [8, 10, 12, 14, 16]


def _slot_start(day: date, hour: int) -> datetime:
    return datetime(day.year, day.month, day.day, hour, 0, 0, tzinfo=TIMEZONE)


async def get_available_slots(day: date, db: AsyncSession) -> list[str]:
    day_start = _slot_start(day, 0)
    day_end = _slot_start(day, 23)

    result = await db.execute(
        select(Appointment.scheduled_at).where(
            and_(
                Appointment.scheduled_at >= day_start,
                Appointment.scheduled_at <= day_end,
                Appointment.status != "cancelled",
            )
        )
    )
    booked_hours = {row.scheduled_at.astimezone(TIMEZONE).hour for row in result}

    now = datetime.now(TIMEZONE)
    available = []
    for hour in SLOT_HOURS:
        slot = _slot_start(day, hour)
        if hour not in booked_hours and slot > now:
            end_hour = hour + 2
            available.append(f"{hour}:00 - {end_hour}:00")

    return available


async def create_appointment(
    db: AsyncSession,
    customer_id: int,
    day: date,
    slot_hour: int,
    service_type: str,
    notes: str | None = None,
    call_id: int | None = None,
) -> Appointment:
    if slot_hour not in SLOT_HOURS:
        raise ValueError(f"Invalid slot. Choose from: {SLOT_HOURS}")

    scheduled_at = _slot_start(day, slot_hour)

    conflict = await db.execute(
        select(Appointment).where(
            and_(
                Appointment.scheduled_at == scheduled_at,
                Appointment.status != "cancelled",
            )
        )
    )
    if conflict.scalar_one_or_none():
        raise ValueError(f"Slot {slot_hour}:00 on {day} is already booked")

    appointment = Appointment(
        customer_id=customer_id,
        call_id=call_id,
        scheduled_at=scheduled_at,
        service_type=service_type,
        notes=notes,
        status="confirmed",
    )
    db.add(appointment)
    await db.flush()
    return appointment


async def get_appointment(appointment_id: int, db: AsyncSession) -> Appointment | None:
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    return result.scalar_one_or_none()
