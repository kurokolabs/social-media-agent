"""Calendar routes — monthly view + FullCalendar events endpoint."""
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="api/templates")


@router.get("/", response_class=HTMLResponse)
async def calendar_view(request: Request):
    return templates.TemplateResponse(
        request, "calendar.html",
        {"active": "calendar"},
    )


@router.get("/api/calendar/events")
async def calendar_events(year: int = None, month: int = None):
    """Return FullCalendar-compatible event list for the given month."""
    from storage.database import get_posts_for_month

    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    posts = get_posts_for_month(year, month)
    events = []
    for p in posts:
        scheduled = p.get("scheduled_at") or ""
        events.append({
            "id": p["id"],
            "title": p["content"][:55],
            "start": scheduled,
            "extendedProps": {
                "platform": p["platform"],
                "post_id": p["id"],
                "status": p["status"],
                # Phase 2 indicators for calendar event rendering
                "is_longform":   p.get("post_type") == "longform_analysis",
                "is_evergreen":  bool(p.get("is_evergreen")),
                "is_repurposed": p.get("repurposed_from_id") is not None,
                "has_carousel":  bool(p.get("carousel_pdf_path")),
            },
        })
    return JSONResponse(events)
