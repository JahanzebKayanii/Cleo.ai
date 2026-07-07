import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.analytics import router as analytics_router
from app.api.auth import is_valid_session, router as auth_router
from app.api.admin import router as admin_router
from app.api.billing import router as billing_router
from app.api.business import router as business_router
from app.api.call import router as call_router
from app.api.calls import router as calls_router
from app.api.stream import router as stream_router
from app.api.customers import router as customers_router
from app.api.documents import router as documents_router
from app.api.health import router as health_router
from app.core.database import create_tables
from app.core.qdrant import ensure_collection

_scheduler = AsyncIOScheduler(timezone="America/Chicago")


async def _run_morning_reminders() -> None:
    from app.services.sms_service import send_morning_reminders
    await send_morning_reminders()


async def _run_state_cleanup() -> None:
    from app.api.auth import _cleanup_expired_sessions
    from app.core.state import purge_stale_calls
    purge_stale_calls()
    _cleanup_expired_sessions()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await ensure_collection()
    _scheduler.add_job(
        _run_morning_reminders,
        CronTrigger(hour=8, minute=0, timezone="America/Chicago"),
        id="morning_reminders",
        replace_existing=True,
    )
    _scheduler.add_job(
        _run_state_cleanup,
        CronTrigger(minute=0),  # every hour on the hour
        id="state_cleanup",
        replace_existing=True,
    )
    _scheduler.start()
    yield
    _scheduler.shutdown(wait=False)


app = FastAPI(
    title="Cleo Voice AI",
    description="AI Voice Receptionist & Knowledge Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def dashboard_auth(request: Request, call_next):
    path = request.url.path
    if path.startswith("/dashboard/") and path != "/dashboard/login.html":
        token = request.cookies.get("cleo_session")
        if not is_valid_session(token):
            return RedirectResponse("/dashboard/login.html")
    response = await call_next(request)
    # Prevent the browser from caching HTML so deployed UI updates are picked up immediately
    if path.startswith("/dashboard/") and (path.endswith(".html") or path.endswith("/")):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


app.include_router(health_router, tags=["health"])
app.include_router(auth_router)
app.include_router(analytics_router)
app.include_router(business_router)
app.include_router(documents_router)
app.include_router(customers_router)
app.include_router(call_router)
app.include_router(calls_router)
app.include_router(stream_router)
app.include_router(admin_router)
app.include_router(billing_router)

_static_dir = os.path.join(os.path.dirname(__file__), "..", "static")

@app.get("/favicon.svg", include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join(_static_dir, "favicon.svg"), media_type="image/svg+xml")


@app.get("/audio/{filename}", include_in_schema=False)
async def serve_audio(filename: str):
    import re
    from fastapi import HTTPException
    from pathlib import Path
    if not re.match(r"^[a-f0-9]{32}\.mp3$", filename):
        raise HTTPException(status_code=404)
    filepath = Path("/tmp/cleo_audio") / filename
    if not filepath.exists():
        raise HTTPException(status_code=404)
    return FileResponse(str(filepath), media_type="audio/mpeg")


if os.path.isdir(_static_dir):
    app.mount("/dashboard", StaticFiles(directory=_static_dir, html=True), name="dashboard")
