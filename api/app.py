"""FastAPI dashboard application."""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from security.middleware import (
    AuthMiddleware,
    CSRFMiddleware,
    RequestSizeLimitMiddleware,
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from storage.database import initialize, initialize_social, initialize_alerts, initialize_analytics
    from intelligence.alert_monitor import alert_monitor
    from security.secrets_rotation import audit_secrets_on_startup
    os.makedirs("output/images", exist_ok=True)
    os.makedirs("output/review_queue", exist_ok=True)
    os.makedirs("output/mock_published", exist_ok=True)
    os.makedirs("output/carousels", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    initialize()
    initialize_social()
    initialize_alerts()
    initialize_analytics()
    audit_secrets_on_startup()
    alert_monitor.start()
    yield
    alert_monitor.stop()


from api.routes.auth import router as auth_router
from api.routes.calendar import router as calendar_router
from api.routes.posts import router as posts_router
from api.routes.chat import router as chat_router
from api.routes.settings import router as settings_router
from api.routes.webhooks import router as webhooks_router
from api.routes.webhooks_buffer import router as webhooks_buffer_router
from api.routes.alerts import router as alerts_router

app = FastAPI(
    title="Kuroko Labs — Social Agent Dashboard",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Global error handler — never leak stack traces or internal details
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    from security.audit_log import audit_log
    import traceback
    request_id = getattr(request.state, "request_id", "unknown")
    audit_log.log(
        "dashboard", "unhandled_exception", 0, 0, 0.0, "error",
        f"request_id={request_id} path={request.url.path} "
        f"exc={type(exc).__name__}: {str(exc)[:200]}"
    )
    # In development, include a safe summary; in production, generic message
    if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
        detail = f"{type(exc).__name__}: {str(exc)[:120]}"
    else:
        detail = "Ein interner Fehler ist aufgetreten. Bitte die Logs prüfen."
    return JSONResponse(
        {"detail": detail, "request_id": request_id},
        status_code=500,
    )


# ---------------------------------------------------------------------------
# Middleware — LIFO order (last added = outermost)
# Desired flow: SecurityHeaders → Auth → CSRF → RateLimit → SizeLimit → handler
# ---------------------------------------------------------------------------

app.add_middleware(SecurityHeadersMiddleware)   # outermost
app.add_middleware(AuthMiddleware)              # session check / redirect to /login
app.add_middleware(CSRFMiddleware)              # CSRF token validation
app.add_middleware(RateLimitMiddleware)         # per-IP sliding-window
app.add_middleware(RequestSizeLimitMiddleware)  # reject oversized bodies early

# CORS: restrict to localhost only — no wildcard origins
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-CSRF-Token", "HX-Request",
                   "HX-Current-URL", "HX-Trigger", "HX-Target"],
    allow_credentials=True,   # needed for session cookies
)

# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output", StaticFiles(directory="output"), name="output")

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(auth_router)               # GET/POST /login, POST /logout
app.include_router(calendar_router)           # GET /
app.include_router(posts_router)              # GET/POST /posts
app.include_router(chat_router)               # POST /posts/{id}/chat
app.include_router(settings_router)           # GET/POST /settings
app.include_router(webhooks_router)           # GET/POST /webhooks/instagram
app.include_router(webhooks_buffer_router)    # POST /webhooks/buffer
app.include_router(alerts_router)             # GET/POST /alerts
