"""Login / logout routes for the operator dashboard."""
import os

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from security.auth import (
    check_auth, is_password_configured, make_csrf_token,
    make_session_token, verify_password,
    _SESSION_COOKIE, _CSRF_COOKIE,
)
from security.audit_log import audit_log

router = APIRouter()
templates = Jinja2Templates(directory="api/templates")

_SECURE_COOKIE = os.getenv("HTTPS_ENABLED", "false").lower() == "true"


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, next: str = "/"):
    if check_auth(request):
        return RedirectResponse(url=next, status_code=303)
    pw_missing = not is_password_configured()
    return templates.TemplateResponse(
        request, "login.html",
        {"pw_missing": pw_missing, "next": next, "error": None},
    )


@router.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    password: str = Form(...),
    next: str = Form(default="/"),
):
    ip = request.client.host if request.client else "unknown"

    if not verify_password(password):
        audit_log.log("dashboard", "login_failed", 0, 0, 0.0, "warning",
                      f"ip={ip} reason=wrong_password")
        return templates.TemplateResponse(
            request, "login.html",
            {"pw_missing": False, "next": next, "error": "Falsches Passwort."},
            status_code=401,
        )

    audit_log.log("dashboard", "login_success", 0, 0, 0.0, "success", f"ip={ip}")

    session_token = make_session_token()
    csrf_token    = make_csrf_token(session_token)

    # Redirect to requested page
    dest = next if next.startswith("/") else "/"
    response = RedirectResponse(url=dest, status_code=303)

    # Session cookie — HttpOnly, not readable by JS
    response.set_cookie(
        _SESSION_COOKIE,
        session_token,
        max_age=86_400,
        httponly=True,
        samesite="lax",
        secure=_SECURE_COOKIE,
        path="/",
    )
    # CSRF cookie — NOT HttpOnly so JS/HTMX can read it
    response.set_cookie(
        _CSRF_COOKIE,
        csrf_token,
        max_age=86_400,
        httponly=False,
        samesite="strict",
        secure=_SECURE_COOKIE,
        path="/",
    )
    return response


@router.post("/logout")
async def logout(request: Request):
    ip = request.client.host if request.client else "unknown"
    audit_log.log("dashboard", "logout", 0, 0, 0.0, "success", f"ip={ip}")
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(_SESSION_COOKIE, path="/")
    response.delete_cookie(_CSRF_COOKIE, path="/")
    return response
