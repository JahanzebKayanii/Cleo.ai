from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.call import Call
from app.models.customer import Customer

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview")
async def overview(db: AsyncSession = Depends(get_db)):
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    days_14_start = today_start - timedelta(days=13)

    # Totals
    total_res = await db.execute(select(func.count()).select_from(Call))
    total_calls = total_res.scalar() or 0

    completed_res = await db.execute(
        select(func.count()).select_from(Call).where(Call.status == "completed")
    )
    completed_calls = completed_res.scalar() or 0

    active_res = await db.execute(
        select(func.count()).select_from(Call).where(Call.status == "in_progress")
    )
    active_calls = active_res.scalar() or 0

    today_res = await db.execute(
        select(func.count()).select_from(Call).where(Call.started_at >= today_start)
    )
    calls_today = today_res.scalar() or 0

    week_res = await db.execute(
        select(func.count()).select_from(Call).where(Call.started_at >= week_start)
    )
    calls_this_week = week_res.scalar() or 0

    # Calls by day (last 14 days)
    daily_res = await db.execute(
        select(
            func.date(Call.started_at).label("day"),
            func.count().label("count"),
        )
        .where(Call.started_at >= days_14_start)
        .group_by(func.date(Call.started_at))
        .order_by(func.date(Call.started_at))
    )
    daily_rows = daily_res.all()

    # Fill in zeros for missing days
    day_map = {str(r.day): r.count for r in daily_rows}
    calls_by_day = []
    for i in range(14):
        d = (days_14_start + timedelta(days=i)).strftime("%Y-%m-%d")
        calls_by_day.append({"date": d, "count": day_map.get(d, 0)})

    # Calls by hour (all time)
    hourly_res = await db.execute(
        select(
            func.extract("hour", Call.started_at).label("hour"),
            func.count().label("count"),
        )
        .where(Call.status == "completed")
        .group_by(func.extract("hour", Call.started_at))
        .order_by(func.extract("hour", Call.started_at))
    )
    hourly_rows = hourly_res.all()
    hour_map = {int(r.hour): r.count for r in hourly_rows}
    calls_by_hour = [{"hour": h, "count": hour_map.get(h, 0)} for h in range(8, 19)]

    # Service breakdown from summaries
    all_summaries_res = await db.execute(
        select(Call.summary).where(Call.summary.isnot(None))
    )
    summaries = [r[0].lower() for r in all_summaries_res.all()]
    service_counts = {"HVAC": 0, "Plumbing": 0, "Electrical": 0, "Other": 0}
    for s in summaries:
        if "hvac" in s or "ac " in s or "heat" in s or "air condition" in s or "furnace" in s:
            service_counts["HVAC"] += 1
        elif "plumb" in s or "pipe" in s or "leak" in s or "drain" in s or "water heater" in s:
            service_counts["Plumbing"] += 1
        elif "electric" in s or "outlet" in s or "breaker" in s or "wiring" in s:
            service_counts["Electrical"] += 1
        else:
            service_counts["Other"] += 1

    # Unique callers
    unique_res = await db.execute(
        select(func.count(func.distinct(Call.customer_id))).select_from(Call)
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
