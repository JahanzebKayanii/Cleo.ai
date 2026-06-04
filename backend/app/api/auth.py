import secrets
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

_sessions: set[str] = set()
_jobber_states: set[str] = set()

_JOBBER_AUTH_URL = "https://api.getjobber.com/api/oauth/authorize"
_JOBBER_TOKEN_URL = "https://api.getjobber.com/api/oauth/token"


def is_valid_session(token: str | None) -> bool:
    return bool(token and token in _sessions)


@router.post("/login")
async def login(password: str = Form(...)):
    if password != settings.dashboard_password:
        return RedirectResponse("/dashboard/login.html?error=1", status_code=302)
    token = secrets.token_hex(32)
    _sessions.add(token)
    response = RedirectResponse("/dashboard/", status_code=302)
    response.set_cookie("cleo_session", token, httponly=True, max_age=86400 * 7, samesite="lax")
    return response


@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse("/dashboard/login.html", status_code=302)
    response.delete_cookie("cleo_session")
    return response


@router.get("/jobber/connect")
async def jobber_connect(request: Request):
    state = secrets.token_hex(16)
    _jobber_states.add(state)
    redirect_uri = f"{settings.base_url}/auth/jobber/callback"
    params = urlencode({
        "client_id": settings.jobber_client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "state": state,
    })
    return RedirectResponse(f"{_JOBBER_AUTH_URL}?{params}", status_code=302)


@router.get("/jobber/callback")
async def jobber_callback(code: str, state: str, db: AsyncSession = Depends(get_db)):
    if state not in _jobber_states:
        return RedirectResponse("/dashboard/config.html?jobber=error", status_code=302)
    _jobber_states.discard(state)

    redirect_uri = f"{settings.base_url}/auth/jobber/callback"
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.post(
            _JOBBER_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": settings.jobber_client_id,
                "client_secret": settings.jobber_client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    tokens = res.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    if not access_token:
        print(f"[Jobber OAuth] Token exchange failed: {tokens}", flush=True)
        return RedirectResponse("/dashboard/config.html?jobber=error", status_code=302)

    from app.models.business import Business
    result = await db.execute(select(Business).where(Business.id == 1))
    business = result.scalar_one_or_none()
    if business:
        business.jobber_api_key = access_token
        business.jobber_refresh_token = refresh_token
        await db.commit()

    return RedirectResponse("/dashboard/config.html?jobber=connected", status_code=302)


@router.post("/jobber/disconnect")
async def jobber_disconnect(db: AsyncSession = Depends(get_db)):
    from app.models.business import Business
    result = await db.execute(select(Business).where(Business.id == 1))
    business = result.scalar_one_or_none()
    if business:
        business.jobber_api_key = None
        business.jobber_refresh_token = None
        await db.commit()
    return RedirectResponse("/dashboard/config.html", status_code=302)
