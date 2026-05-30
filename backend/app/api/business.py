from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.business_service import get_business, update_business
from app.services.integration_service import push_to_integrations

router = APIRouter(prefix="/business", tags=["business"])


@router.get("/config")
async def get_config(db: AsyncSession = Depends(get_db)):
    return await get_business(db)


@router.put("/config")
async def put_config(data: dict, db: AsyncSession = Depends(get_db)):
    return await update_business(db, data)


class TestIntegrationRequest(BaseModel):
    customer_name: str = "Test User"
    customer_phone: str = "+10000000000"
    service_type: str = "HVAC"
    issue: str = "AC not cooling"
    booked: bool = True
    appointment_date: str = "2026-06-06"
    appointment_time: str = "10 AM to noon"


@router.post("/test-integrations")
async def test_integrations(body: TestIntegrationRequest, db: AsyncSession = Depends(get_db)):
    config = await get_business(db)
    transcript = f"Caller: I need help with my {body.service_type}. {body.issue}\nCleo: I can help with that."
    summary = f"Caller reported {body.issue}. {'Appointment booked for ' + body.appointment_date + ' ' + body.appointment_time + '.' if body.booked else 'No appointment booked.'}"
    await push_to_integrations(
        customer_name=body.customer_name,
        customer_phone=body.customer_phone,
        transcript=transcript,
        summary=summary,
        config=config,
    )
    return {"status": "done", "integrations_triggered": [
        k for k in ["hubspot_token", "jobber_api_key", "housecall_pro_api_key", "quickbooks_token", "servicetitan_token"]
        if config.get(k)
    ]}
