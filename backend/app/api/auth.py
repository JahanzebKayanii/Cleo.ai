import secrets

from fastapi import APIRouter, Form, Response
from fastapi.responses import RedirectResponse

from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

_sessions: set[str] = set()


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
