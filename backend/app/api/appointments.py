from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.appointment_service import (
    create_appointment,
    get_appointment,
    get_available_slots,
)

router = APIRouter(prefix="/appointments", tags=["appointments"])


class CreateAppointmentRequest(BaseModel):
    customer_id: int
    date: date
    slot_hour: int
    service_type: str
    notes: str | None = None
    call_id: int | None = None


@router.get("/slots")
async def available_slots(date: date, db: AsyncSession = Depends(get_db)):
    slots = await get_available_slots(date, db)
    return {"date": str(date), "available_slots": slots}


@router.post("/create")
async def book_appointment(
    body: CreateAppointmentRequest, db: AsyncSession = Depends(get_db)
):
    try:
        appointment = await create_appointment(
            db=db,
            customer_id=body.customer_id,
            day=body.date,
            slot_hour=body.slot_hour,
            service_type=body.service_type,
            notes=body.notes,
            call_id=body.call_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return {
        "id": appointment.id,
        "customer_id": appointment.customer_id,
        "scheduled_at": appointment.scheduled_at.isoformat(),
        "service_type": appointment.service_type,
        "status": appointment.status,
    }


@router.get("/{appointment_id}")
async def get(appointment_id: int, db: AsyncSession = Depends(get_db)):
    appointment = await get_appointment(appointment_id, db)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
