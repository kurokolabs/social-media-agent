"""Settings / Ops route — Instagram DM toggle, channel status, manual triggers."""
import os
from datetime import datetime, timezone
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/settings")
templates = Jinja2Templates(directory="api/templates")


def _channel_status() -> list:
    pairs = [
        ("linkedin",  "BUFFER_CHANNEL_ID"),
        ("twitter",   "BUFFER_X_CHANNEL_ID"),
        ("instagram", "BUFFER_IG_CHANNEL_ID"),
        ("threads",   "BUFFER_THREADS_CHANNEL_ID"),
    ]
    return [(p, k, os.getenv(k, "")) for p, k in pairs]


@router.get("", response_class=HTMLResponse)
async def settings_view(request: Request):
    ig_dm_enabled = os.getenv("IG_DM_AUTOMATION_ENABLED", "false").lower() == "true"
    ig_configured = bool(os.getenv("IG_APP_SECRET") and os.getenv("IG_WEBHOOK_VERIFY_TOKEN"))
    buffer_webhook_configured = bool(os.getenv("BUFFER_WEBHOOK_SECRET", ""))
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return templates.TemplateResponse(
        request, "settings.html",
        {
            "active": "settings",
            "ig_dm_enabled": ig_dm_enabled,
            "ig_configured": ig_configured,
            "channels": _channel_status(),
            "buffer_webhook_configured": buffer_webhook_configured,
            "current_time": current_time,
        },
    )


@router.post("/dm-toggle", response_class=HTMLResponse)
async def toggle_dm(request: Request, enabled: str = Form(default="")):
    is_enabled = enabled == "on"
    ig_configured = bool(os.getenv("IG_APP_SECRET") and os.getenv("IG_WEBHOOK_VERIFY_TOKEN"))

    if is_enabled:
        html = '<span class="status status-published">Aktiv</span>'
    elif ig_configured:
        html = '<span class="status status-scheduled">Konfiguriert — aktivierbar</span>'
    else:
        html = (
            '<span class="status status-pending">Nicht konfiguriert</span>'
            '<p class="text-muted mt-1">Setze <code>IG_APP_SECRET</code> und '
            '<code>IG_WEBHOOK_VERIFY_TOKEN</code> in <code>.env</code>.</p>'
        )
    return HTMLResponse(html)


def _run_sync(fn_path: str) -> HTMLResponse:
    """Helper: run a scheduler fn synchronously and return status fragment."""
    try:
        module_path, fn_name = fn_path.rsplit(".", 1)
        import importlib
        mod = importlib.import_module(module_path)
        result = getattr(mod, fn_name)()
        return HTMLResponse(
            f'<span class="status status-published">✓ Fertig</span> '
            f'<span class="mono" style="font-size:.75rem;color:var(--gray-600);">{result}</span>'
        )
    except Exception as e:
        return HTMLResponse(
            f'<span class="status status-failed">Fehler: {e}</span>'
        )


@router.post("/run-weekly", response_class=HTMLResponse)
async def run_weekly_now(request: Request):
    try:
        from tasks.generate_tasks import generate_weekly_batch
        task = generate_weekly_batch.delay()
        return HTMLResponse(
            f'<span class="status status-scheduled">Gestartet</span> '
            f'<span class="mono" style="font-size:.75rem;color:var(--gray-600);">task={task.id[:8]}…</span>'
        )
    except Exception:
        return _run_sync("scheduler.weekly_planner.run_weekly")


@router.post("/run-analytics", response_class=HTMLResponse)
async def run_analytics_now(request: Request):
    """Phase 2 Feature 5 — manual analytics sync."""
    return _run_sync("scheduler.weekly_planner.run_analytics_sync")


@router.post("/run-repurposing", response_class=HTMLResponse)
async def run_repurposing_now(request: Request):
    """Phase 2 Feature 2 — manual repurposing run."""
    return _run_sync("scheduler.weekly_planner.run_repurposing")


@router.post("/run-evergreen", response_class=HTMLResponse)
async def run_evergreen_now(request: Request):
    """Phase 2 Feature 6 — manual evergreen rotation."""
    return _run_sync("scheduler.weekly_planner.run_evergreen_rotation")


@router.post("/run-longform", response_class=HTMLResponse)
async def run_longform_now(request: Request):
    """Phase 2 Feature 7 — manual longform post generation."""
    return _run_sync("scheduler.weekly_planner.run_longform_wednesday")


@router.post("/run-competitors", response_class=HTMLResponse)
async def run_competitors_now(request: Request):
    """Phase 2 Feature 4 — manual competitor scrape."""
    try:
        from scraper.registry import get_competitor_scrapers
        scrapers = get_competitor_scrapers()
        total = 0
        for s in scrapers:
            try:
                articles = s.scrape()
                total += len(articles)
            except Exception:
                pass
        return HTMLResponse(
            f'<span class="status status-published">✓ Fertig</span> '
            f'<span class="mono" style="font-size:.75rem;color:var(--gray-600);">'
            f'{total} Artikel von {len(scrapers)} Quellen</span>'
        )
    except Exception as e:
        return HTMLResponse(f'<span class="status status-failed">Fehler: {e}</span>')
