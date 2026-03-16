"""Security middleware stack.

Middleware order in app.py (LIFO — last added = outermost):
    RequestSizeLimitMiddleware  →  innermost (reject early)
    RateLimitMiddleware
    CSRFMiddleware
    AuthMiddleware
    SecurityHeadersMiddleware   →  outermost (always adds headers)

Request flow:
    SecurityHeaders → Auth → CSRF → RateLimit → RequestSizeLimit → handler
"""
import os
import time
import uuid
from collections import defaultdict
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, RedirectResponse
from starlette.types import ASGIApp


# ---------------------------------------------------------------------------
# 1. SecurityHeadersMiddleware
# ---------------------------------------------------------------------------

_HTTPS_ENABLED = os.getenv("HTTPS_ENABLED", "false").lower() == "true"

# Allow HTMX from unpkg, FullCalendar + Google Fonts from cdn.jsdelivr.net
_CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' "
        "unpkg.com "
        "cdn.jsdelivr.net; "
    "style-src 'self' 'unsafe-inline' "
        "cdn.jsdelivr.net "
        "fonts.googleapis.com "
        "fonts.gstatic.com; "
    "font-src 'self' fonts.gstatic.com; "
    "img-src 'self' data:; "
    "connect-src 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)

_SECURITY_HEADERS: dict[str, str] = {
    "X-Content-Type-Options":    "nosniff",
    "X-Frame-Options":           "DENY",
    "Referrer-Policy":           "strict-origin-when-cross-origin",
    "X-XSS-Protection":         "1; mode=block",
    "Content-Security-Policy":   _CSP,
    "Permissions-Policy": (
        "camera=(), microphone=(), geolocation=(), "
        "payment=(), usb=(), interest-cohort=()"
    ),
}

if _HTTPS_ENABLED:
    # Only send HSTS over TLS; 1-year max-age + includeSubDomains
    _SECURITY_HEADERS["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Attach security headers and a unique X-Request-ID to every response."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        # Make request-id available to handlers via request.state
        request.state.request_id = request_id

        response = await call_next(request)

        for name, value in _SECURITY_HEADERS.items():
            response.headers[name] = value
        response.headers["X-Request-ID"] = request_id
        return response


# ---------------------------------------------------------------------------
# 2. AuthMiddleware
# ---------------------------------------------------------------------------

# Paths that are always accessible without authentication
_AUTH_EXEMPT_PREFIXES = (
    "/login",
    "/static/",
    "/output/",
    "/webhooks/",   # external callers (Buffer, Meta)
)


class AuthMiddleware(BaseHTTPMiddleware):
    """Redirect unauthenticated browser requests to /login.

    HTMX requests (hx-request header) receive a 401 JSON response
    so the UI can show an error instead of a redirect.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path

        # Always allow exempt paths
        if any(path.startswith(p) for p in _AUTH_EXEMPT_PREFIXES):
            return await call_next(request)

        from security.auth import check_auth
        if check_auth(request):
            return await call_next(request)

        # Not authenticated
        from security.audit_log import audit_log
        ip = request.client.host if request.client else "unknown"
        audit_log.log(
            "dashboard", "auth_required", 0, 0, 0.0, "warning",
            f"ip={ip} path={path} method={request.method}"
        )

        if request.headers.get("hx-request"):
            return JSONResponse(
                {"detail": "Session abgelaufen. Bitte neu einloggen."},
                status_code=401,
            )
        # Browser navigation — redirect to login with next param
        login_url = f"/login?next={path}"
        return RedirectResponse(url=login_url, status_code=303)


# ---------------------------------------------------------------------------
# 3. CSRFMiddleware
# ---------------------------------------------------------------------------

_CSRF_SAFE_METHODS  = frozenset({"GET", "HEAD", "OPTIONS"})
# External webhook receivers must NOT require CSRF tokens
_CSRF_EXEMPT_PATHS  = frozenset({
    "/webhooks/instagram",
    "/webhooks/buffer",
    "/login",    # login uses password; no session-based CSRF applicable
    "/logout",   # worst case: attacker logs user out (not a dangerous action)
})


class CSRFMiddleware(BaseHTTPMiddleware):
    """Validate X-CSRF-Token header on all state-changing requests.

    HTMX injects the token automatically via hx-headers on the <body>.
    Standard HTML forms that don't use HTMX must include it as a header
    (set via JS) — this dashboard is fully HTMX-driven so that's fine.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.method in _CSRF_SAFE_METHODS:
            return await call_next(request)

        if request.url.path in _CSRF_EXEMPT_PATHS:
            return await call_next(request)

        from security.auth import verify_csrf_token, _SESSION_COOKIE, _CSRF_COOKIE
        session_token = request.cookies.get(_SESSION_COOKIE, "")
        csrf_token    = request.headers.get("X-CSRF-Token", "")

        if not verify_csrf_token(session_token, csrf_token):
            from security.audit_log import audit_log
            ip = request.client.host if request.client else "unknown"
            audit_log.log(
                "dashboard", "csrf_rejected", 0, 0, 0.0, "warning",
                f"ip={ip} path={request.url.path}"
            )
            return JSONResponse(
                {"detail": "CSRF-Token ungültig oder fehlend."},
                status_code=403,
            )

        return await call_next(request)


# ---------------------------------------------------------------------------
# 4. RateLimitMiddleware
# ---------------------------------------------------------------------------

# Per-route overrides — lower limit means stricter
_ROUTE_LIMITS: dict[str, int] = {
    # Calendar API — 10 RPM (frequent polling, allow reasonable refresh)
    "/api/calendar/events":        10,
    # Webhook endpoints — external callers — 30 RPM each
    "/webhooks/instagram":         30,
    "/webhooks/buffer":            30,
    # Expensive ops — 3 RPM each (manual trigger buttons)
    "/settings/run-weekly":         3,
    "/settings/run-analytics":      3,
    "/settings/run-repurposing":    3,
    "/settings/run-evergreen":      3,
    "/settings/run-longform":       3,
    "/settings/run-competitors":    3,
    # Carousel generation — AI + PDF work — 5 RPM
    "/posts/{id}/generate-carousel": 5,
}
_CHAT_ROUTE_KEY   = "/posts/{id}/chat"
_CHAT_LIMIT_RPM   = 5
_GENERAL_LIMIT_RPM = 60
_WINDOW_SECONDS   = 60.0
_MAX_TRACKED_IPS  = 5_000   # cap dict size to prevent unbounded growth

# Sliding-window bucket: (ip, route_key) → list of request timestamps
_REQUEST_WINDOWS: defaultdict[tuple[str, str], list[float]] = defaultdict(list)
_LAST_CLEANUP = 0.0
_CLEANUP_INTERVAL = 120.0   # purge stale entries every 2 minutes


def _get_route_key(path: str) -> str:
    """Normalise path to a rate-limit bucket key."""
    if path in _ROUTE_LIMITS:
        return path
    parts = path.strip("/").split("/")
    # /posts/<id>/chat
    if len(parts) == 3 and parts[0] == "posts" and parts[2] == "chat":
        return _CHAT_ROUTE_KEY
    # /posts/<id>/generate-carousel
    if len(parts) == 3 and parts[0] == "posts" and parts[2] == "generate-carousel":
        return "/posts/{id}/generate-carousel"
    return "__general__"


def _get_limit(route_key: str) -> int:
    if route_key in _ROUTE_LIMITS:
        return _ROUTE_LIMITS[route_key]
    if route_key == _CHAT_ROUTE_KEY:
        return _CHAT_LIMIT_RPM
    return _GENERAL_LIMIT_RPM


def _cleanup_stale(now: float) -> None:
    """Remove empty or entirely-expired buckets from the window dict."""
    global _LAST_CLEANUP
    if now - _LAST_CLEANUP < _CLEANUP_INTERVAL:
        return
    _LAST_CLEANUP = now
    window_start = now - _WINDOW_SECONDS
    stale = [k for k, ts in _REQUEST_WINDOWS.items() if not ts or ts[-1] <= window_start]
    for k in stale:
        del _REQUEST_WINDOWS[k]
    # Hard cap: if still too large, drop oldest keys
    if len(_REQUEST_WINDOWS) > _MAX_TRACKED_IPS:
        overflow = len(_REQUEST_WINDOWS) - _MAX_TRACKED_IPS
        for k in list(_REQUEST_WINDOWS.keys())[:overflow]:
            del _REQUEST_WINDOWS[k]


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Per-IP sliding-window rate limiter with periodic stale-entry cleanup."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        ip = request.client.host if request.client else "unknown"
        route_key = _get_route_key(request.url.path)
        limit = _get_limit(route_key)
        bucket_key = (ip, route_key)

        now = time.monotonic()
        _cleanup_stale(now)

        window_start = now - _WINDOW_SECONDS
        timestamps = _REQUEST_WINDOWS[bucket_key]
        timestamps[:] = [t for t in timestamps if t > window_start]

        if len(timestamps) >= limit:
            oldest = timestamps[0]
            retry_after = int(_WINDOW_SECONDS - (now - oldest)) + 1
            from security.audit_log import audit_log
            audit_log.log(
                "dashboard", "rate_limited", 0, 0, 0.0, "warning",
                f"ip={ip} route={route_key} limit={limit}"
            )
            return JSONResponse(
                {"detail": "Zu viele Anfragen. Bitte kurz warten."},
                status_code=429,
                headers={"Retry-After": str(retry_after)},
            )

        timestamps.append(now)
        return await call_next(request)


# ---------------------------------------------------------------------------
# 5. RequestSizeLimitMiddleware
# ---------------------------------------------------------------------------

_MAX_REQUEST_BYTES = 1 * 1024 * 1024   # 1 MB


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Reject requests whose Content-Length exceeds 1 MB."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        content_length = request.headers.get("content-length")
        if content_length is not None:
            try:
                size = int(content_length)
            except ValueError:
                size = 0
            if size > _MAX_REQUEST_BYTES:
                return JSONResponse(
                    {"detail": "Request-Body zu groß. Maximum ist 1 MB."},
                    status_code=413,
                )
        return await call_next(request)
