"""Posts routes — list, detail, approve, carousel generation."""
import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/posts")
templates = Jinja2Templates(directory="api/templates")
templates.env.filters["basename"] = os.path.basename


@router.get("", response_class=HTMLResponse)
async def posts_list(
    request: Request,
    platform: str = "",
    feature: str = "",   # Phase 2: longform | evergreen | repurposed | carousel
):
    from storage.database import get_connection
    conn = get_connection()
    try:
        conditions = []
        params: list = []

        if platform:
            conditions.append("platform = ?")
            params.append(platform)

        # Phase 2 feature filters
        if feature == "longform":
            conditions.append("post_type = 'longform_analysis'")
        elif feature == "evergreen":
            conditions.append("is_evergreen = 1")
        elif feature == "repurposed":
            conditions.append("repurposed_from_id IS NOT NULL")
        elif feature == "carousel":
            conditions.append("carousel_pdf_path IS NOT NULL")

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        rows = conn.execute(
            f"SELECT * FROM social_posts {where} ORDER BY scheduled_at DESC",
            params,
        ).fetchall()
        posts = [dict(r) for r in rows]
    finally:
        conn.close()

    return templates.TemplateResponse(
        request, "posts.html",
        {
            "active": "posts",
            "posts": posts,
            "platform_filter": platform,
            "extra_filter": feature,
        },
    )


@router.get("/{post_id}", response_class=HTMLResponse)
async def post_detail(request: Request, post_id: int):
    from storage.database import get_social_post, get_post_edits
    post = get_social_post(post_id)
    if not post:
        return HTMLResponse("<p>Post nicht gefunden.</p>", status_code=404)
    edits = get_post_edits(post_id)
    return templates.TemplateResponse(
        request, "post_detail.html",
        {"post": post, "edits": edits},
    )


@router.post("/{post_id}/approve", response_class=HTMLResponse)
async def approve_post(request: Request, post_id: int):
    from storage.database import update_social_post, get_social_post, get_post_edits
    update_social_post(post_id, {"status": "approved"})

    try:
        from tasks.publish_tasks import publish_post_to_buffer
        publish_post_to_buffer.delay(post_id)
    except Exception:
        pass

    post = get_social_post(post_id)
    edits = get_post_edits(post_id)
    return templates.TemplateResponse(
        request, "post_detail.html",
        {"post": post, "edits": edits},
    )


@router.post("/{post_id}/generate-carousel", response_class=HTMLResponse)
async def generate_carousel(request: Request, post_id: int):
    """Phase 2 Feature 3 — generate a 10-slide PDF carousel for a LinkedIn post."""
    from storage.database import get_social_post, get_post_edits, save_carousel_path, update_social_post
    post = get_social_post(post_id)
    if not post:
        return HTMLResponse("<p>Post nicht gefunden.</p>", status_code=404)

    try:
        from generator.carousel_generator import CarouselGenerator
        import os
        os.makedirs("output/carousels", exist_ok=True)

        # Use post_type as title fallback
        title = (post.get("post_type") or "linkedin-post").replace("_", " ").title()
        pdf_path = CarouselGenerator().generate(post["content"], title)
        save_carousel_path(post_id, pdf_path)
        update_social_post(post_id, {"carousel_pdf_path": pdf_path})
    except Exception as e:
        post = get_social_post(post_id)
        edits = get_post_edits(post_id)
        return templates.TemplateResponse(
            request, "post_detail.html",
            {"post": post, "edits": edits, "carousel_error": str(e)},
        )

    post = get_social_post(post_id)
    edits = get_post_edits(post_id)
    return templates.TemplateResponse(
        request, "post_detail.html",
        {"post": post, "edits": edits},
    )
