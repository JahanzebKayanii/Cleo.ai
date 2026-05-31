import json
import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business

_cache: dict | None = None
_cache_ts: float = 0
_CACHE_TTL = 60  # seconds


def _to_dict(b: Business) -> dict:
    return {
        "id": b.id,
        "name": b.name,
        "description": b.description,
        "timezone": b.timezone,
        "services": json.loads(b.services) if b.services else [],
        "hours_open": b.hours_open,
        "hours_close": b.hours_close,
        "service_area": b.service_area or "Austin, TX and surrounding areas within 30 miles",
        "jobber_api_key": b.jobber_api_key or "",
        "hubspot_token": b.hubspot_token or "",
        "housecall_pro_api_key": b.housecall_pro_api_key or "",
        "quickbooks_token": b.quickbooks_token or "",
        "servicetitan_token": b.servicetitan_token or "",
    }


async def get_business(db: AsyncSession) -> dict:
    global _cache, _cache_ts
    if _cache and time.time() - _cache_ts < _CACHE_TTL:
        return _cache

    result = await db.execute(select(Business).where(Business.id == 1))
    business = result.scalar_one_or_none()

    if not business:
        business = Business(
            id=1,
            name="Apex Home Services",
            description="a licensed HVAC, plumbing, and electrical company based in Austin, Texas",
            timezone="America/Chicago",
            services='["HVAC", "plumbing", "electrical"]',
            hours_open=8,
            hours_close=18,
        )
        db.add(business)
        await db.flush()

    _cache = _to_dict(business)
    _cache_ts = time.time()
    return _cache


async def update_business(db: AsyncSession, data: dict) -> dict:
    global _cache, _cache_ts
    result = await db.execute(select(Business).where(Business.id == 1))
    business = result.scalar_one_or_none()

    if not business:
        business = Business(id=1)
        db.add(business)

    if "name" in data:
        business.name = data["name"]
    if "description" in data:
        business.description = data["description"]
    if "timezone" in data:
        business.timezone = data["timezone"]
    if "services" in data:
        business.services = json.dumps(data["services"])
    if "hours_open" in data:
        business.hours_open = int(data["hours_open"])
    if "hours_close" in data:
        business.hours_close = int(data["hours_close"])
    if "service_area" in data:
        business.service_area = data["service_area"] or None
    if "jobber_api_key" in data:
        business.jobber_api_key = data["jobber_api_key"] or None
    if "hubspot_token" in data:
        business.hubspot_token = data["hubspot_token"] or None
    if "housecall_pro_api_key" in data:
        business.housecall_pro_api_key = data["housecall_pro_api_key"] or None
    if "quickbooks_token" in data:
        business.quickbooks_token = data["quickbooks_token"] or None
    if "servicetitan_token" in data:
        business.servicetitan_token = data["servicetitan_token"] or None

    _cache = None  # invalidate cache
    _cache_ts = 0
    return _to_dict(business)
