from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.call import Call

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview")
async def overview(business_id: int = 1, db: AsyncSession = Depends(get_db)):
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    days_14_start = today_start - timedelta(days=13)

    def _filter(q):
        return q.where(Call.business_id == business_id)

    total_res = await db.execute(_filter(select(func.count()).select_from(Call)))
    total_calls = total_res.scalar() or 0

    completed_res = await db.execute(
        _filter(select(func.count()).select_from(Call)).where(Call.status == "completed")
    )
    completed_calls = completed_res.scalar() or 0

    active_res = await db.execute(
        _filter(select(func.count()).select_from(Call)).where(Call.status == "in_progress")
    )
    active_calls = active_res.scalar() or 0

    today_res = await db.execute(
        _filter(select(func.count()).select_from(Call)).where(Call.started_at >= today_start)
    )
    calls_today = today_res.scalar() or 0

    week_res = await db.execute(
        _filter(select(func.count()).select_from(Call)).where(Call.started_at >= week_start)
    )
    calls_this_week = week_res.scalar() or 0

    # Calls by day (last 14 days)
    daily_res = await db.execute(
        _filter(
            select(
                func.date(Call.started_at).label("day"),
                func.count().label("count"),
            ).where(Call.started_at >= days_14_start)
        )
        .group_by(func.date(Call.started_at))
        .order_by(func.date(Call.started_at))
    )
    daily_rows = daily_res.all()
    day_map = {str(r.day): r.count for r in daily_rows}
    calls_by_day = []
    for i in range(14):
        d = (days_14_start + timedelta(days=i)).strftime("%Y-%m-%d")
        calls_by_day.append({"date": d, "count": day_map.get(d, 0)})

    # Calls by hour
    hourly_res = await db.execute(
        _filter(
            select(
                func.extract("hour", Call.started_at).label("hour"),
                func.count().label("count"),
            ).where(Call.status == "completed")
        )
        .group_by(func.extract("hour", Call.started_at))
        .order_by(func.extract("hour", Call.started_at))
    )
    hourly_rows = hourly_res.all()
    hour_map = {int(r.hour): r.count for r in hourly_rows}
    calls_by_hour = [{"hour": h, "count": hour_map.get(h, 0)} for h in range(8, 19)]

    # Service breakdown from call intent field
    all_intents_res = await db.execute(
        _filter(select(Call.intent).where(Call.intent.isnot(None)))
    )
    service_counts: dict[str, int] = {}
    for (intent,) in all_intents_res.all():
        key = (intent or "other").title()
        service_counts[key] = service_counts.get(key, 0) + 1
    if not service_counts:
        service_counts = {"No data": 0}

    # Unique callers
    unique_res = await db.execute(
        _filter(select(func.count(func.distinct(Call.customer_id))).select_from(Call))
    )
    unique_callers = unique_res.scalar() or 0

    return {
        "total_calls": total_calls,
        "completed_calls": completed_calls,
        "active_calls": active_calls,
        "calls_today": calls_today,
        "calls_this_week": calls_this_week,
        "unique_callers": unique_callers,
        "calls_by_day": calls_by_day,
        "calls_by_hour": calls_by_hour,
        "service_breakdown": service_counts,
    }
