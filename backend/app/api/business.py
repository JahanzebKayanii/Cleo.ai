from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.business_service import get_business, get_business_raw, update_business
from app.services.integration_service import push_to_integrations

router = APIRouter(prefix="/business", tags=["business"])


@router.get("/config")
async def get_config(business_id: int = 1, db: AsyncSession = Depends(get_db)):
    return await get_business(db, business_id)


@router.put("/config")
async def put_config(data: dict, business_id: int = 1, db: AsyncSession = Depends(get_db)):
    return await update_business(db, data, business_id)


class TestIntegrationRequest(BaseModel):
    customer_name: str = "Test User"
    customer_phone: str = "+10000000000"
    service_type: str = "HVAC"
    issue: str = "AC not cooling"
    booked: bool = True
    appointment_date: str = "2026-06-06"
    appointment_time: str = "10 AM to noon"
    address: str = "123 Main St, Austin TX 78701"


@router.post("/test-integrations")
async def test_integrations(
    body: TestIntegrationRequest,
    business_id: int = 1,
    db: AsyncSession = Depends(get_db),
):
    config = await get_business_raw(db, business_id)
    transcript = f"Caller: I need help with my {body.service_type}. {body.issue}\nCleo: I can help with that."
    summary = f"Caller reported {body.issue}. {'Appointment booked for ' + body.appointment_date + ' ' + body.appointment_time + '.' if body.booked else 'No appointment booked.'}"
    await push_to_integrations(
        customer_name=body.customer_name,
        customer_phone=body.customer_phone,
        transcript=transcript,
        summary=summary,
        config=config,
    )

    if config.get("owner_email"):
        from app.services.email_service import send_call_summary
        await send_call_summary(
            to_email=config["owner_email"],
            business_name=config.get("name", "the business"),
            customer_name=body.customer_name,
            customer_phone=body.customer_phone,
            summary=summary,
            transcript=transcript,
            booked=body.booked,
            appointment_date=body.appointment_date,
            appointment_time=body.appointment_time,
        )

    triggered = [k for k in ["hubspot_token", "jobber_api_key", "housecall_pro_api_key"] if config.get(k)]
    if config.get("owner_email"):
        triggered.append("email")
    return {"status": "done", "integrations_triggered": triggered}
