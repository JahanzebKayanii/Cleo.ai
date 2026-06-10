import secrets
import time
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

_SESSION_TTL = 86400 * 7  # 7 days

# session_token -> {"role": "admin"|"tenant", "business_id": int, "created": float}
_sessions: dict[str, dict] = {}
_jobber_states: set[str] = set()


def _cleanup_expired_sessions() -> None:
    now = time.time()
    expired = [k for k, v in _sessions.items() if now - v.get("created", 0) > _SESSION_TTL]
    for k in expired:
        _sessions.pop(k, None)

_JOBBER_AUTH_URL = "https://api.getjobber.com/api/oauth/authorize"
_JOBBER_TOKEN_URL = "https://api.getjobber.com/api/oauth/token"


def is_valid_session(token: str | None) -> bool:
    if not token or token not in _sessions:
        return False
    if time.time() - _sessions[token].get("created", 0) > _SESSION_TTL:
        _sessions.pop(token, None)
        return False
    return True


def get_session(token: str | None) -> dict | None:
    if not is_valid_session(token):
        return None
    return _sessions.get(token)


def session_business_id(token: str | None) -> int:
    s = get_session(token)
    if not s:
        return 1
    return s.get("business_id", 1)


def require_tenant_access(request, business_id: int) -> dict:
    """Reject if the logged-in session can't access this business_id.
    Admins can access any tenant. Tenants can only access their own.
    Returns the session dict on success. Raises 401/403 on failure.
    """
    from fastapi import HTTPException
    token = request.cookies.get("cleo_session")
    s = get_session(token)
    if not s:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if s.get("role") == "admin":
        return s
    if s.get("business_id") != business_id:
        raise HTTPException(status_code=403, detail="Access denied for this tenant")
    return s


def require_admin(request) -> dict:
    """Reject if the logged-in session is not an admin."""
    from fastapi import HTTPException
    token = request.cookies.get("cleo_session")
    s = get_session(token)
    if not s:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if s.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return s


def _make_session(role: str, business_id: int) -> str:
    _cleanup_expired_sessions()
    token = secrets.token_hex(32)
    _sessions[token] = {"role": role, "business_id": business_id, "created": time.time()}
    return token


@router.post("/login")
async def login(password: str = Form(...), db: AsyncSession = Depends(get_db)):
    # Admin login
    if password == settings.dashboard_password:
        token = _make_session("admin", 1)
        response = RedirectResponse("/dashboard/", status_code=302)
        response.set_cookie("cleo_session", token, httponly=True, max_age=86400 * 7, samesite="lax")
        return response

    # Tenant login — check all businesses with a dashboard_password set
    from app.models.business import Business
    result = await db.execute(
        select(Business).where(Business.dashboard_password == password, Business.is_active == True)
    )
    business = result.scalar_one_or_none()
    if business:
        token = _make_session("tenant", business.id)
        response = RedirectResponse("/dashboard/", status_code=302)
        response.set_cookie("cleo_session", token, httponly=True, max_age=86400 * 7, samesite="lax")
        return response

    return RedirectResponse("/dashboard/login.html?error=1", status_code=302)


@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse("/dashboard/login.html", status_code=302)
    response.delete_cookie("cleo_session")
    return response


@router.get("/session")
async def session_info(request: Request):
    token = request.cookies.get("cleo_session")
    s = get_session(token)
    if not s:
        return {"authenticated": False}
    return {"authenticated": True, "role": s["role"], "business_id": s["business_id"]}


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
async def jobber_callback(code: str, state: str, request: Request, db: AsyncSession = Depends(get_db)):
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

    token = request.cookies.get("cleo_session")
    s = get_session(token)
    if not s:
        return RedirectResponse("/dashboard/login.html", status_code=302)
    business_id = s["business_id"]

    from app.models.business import Business
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if business:
        business.jobber_api_key = access_token
        business.jobber_refresh_token = refresh_token
        await db.commit()

    return RedirectResponse("/dashboard/config.html?jobber=connected", status_code=302)


@router.post("/jobber/disconnect")
async def jobber_disconnect(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("cleo_session")
    business_id = session_business_id(token)

    from app.models.business import Business
    result = await db.execute(select(Business).where(Business.id == business_id))
    business = result.scalar_one_or_none()
    if business:
        business.jobber_api_key = None
        business.jobber_refresh_token = None
        await db.commit()
    return RedirectResponse("/dashboard/config.html", status_code=302)
