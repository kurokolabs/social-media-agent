"""Alerts routes — unread count, list, mark read/dismissed, manual check."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/alerts")
templates = Jinja2Templates(directory="api/templates")


@router.get("/count")
async def alert_count():
    """HTMX-friendly: returns JSON with unread count."""
    from storage.database import get_alert_count
    return JSONResponse(get_alert_count())


@router.get("", response_class=HTMLResponse)
async def alerts_list(request: Request):
    """Render alerts page."""
    from storage.database import get_unread_alerts
    alerts = get_unread_alerts(limit=50)
    return templates.TemplateResponse(request, "alerts.html", {
        "active": "alerts",
        "alerts": alerts,
    })


@router.post("/{alert_id}/read", response_class=HTMLResponse)
async def mark_read(alert_id: int):
    from storage.database import mark_alert_read
    mark_alert_read(alert_id)
    return HTMLResponse("")


@router.post("/{alert_id}/dismiss", response_class=HTMLResponse)
async def dismiss_alert(alert_id: int):
    from storage.database import mark_alert_dismissed
    mark_alert_dismissed(alert_id)
    return HTMLResponse("")


@router.post("/check-now")
async def check_now():
    """Manually trigger an alert check."""
    from intelligence.alert_monitor import alert_monitor
    count = alert_monitor.check_now()
    return JSONResponse({"new_alerts": count})
