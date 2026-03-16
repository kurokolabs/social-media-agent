"""Chat route — agent-based post editing via HTMX."""
import time
from collections import defaultdict
from typing import DefaultDict

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse

from config import MAX_CHAT_MESSAGE_LEN
from security.input_validator import sanitize_text

router = APIRouter(prefix="/posts")

# ---------------------------------------------------------------------------
# In-memory per-post_id rate limiter
# Maps post_id -> list of request timestamps (monotonic)
# ---------------------------------------------------------------------------
_CHAT_WINDOW_SECONDS = 60.0
_CHAT_MAX_PER_WINDOW = 5
_chat_timestamps: DefaultDict[int, list[float]] = defaultdict(list)


def _chat_rate_check(post_id: int) -> bool:
    """Return True if the request is within the rate limit, False if exceeded."""
    now = time.monotonic()
    window_start = now - _CHAT_WINDOW_SECONDS
    timestamps = _chat_timestamps[post_id]
    timestamps[:] = [t for t in timestamps if t > window_start]
    if len(timestamps) >= _CHAT_MAX_PER_WINDOW:
        return False
    timestamps.append(now)
    return True


@router.post("/{post_id}/chat", response_class=HTMLResponse)
async def chat_edit(request: Request, post_id: int, message: str = Form(...)):
    """Process a chat edit instruction and return updated chat bubbles."""
    import os
    from storage.database import (
        get_social_post, update_social_post, save_post_edit, get_post_edits
    )
    from generator.prompts_extended import EDIT_SYSTEM_PROMPT, EDIT_USER_TEMPLATE

    # --- Input length check ---
    if len(message) > MAX_CHAT_MESSAGE_LEN:
        return JSONResponse(
            {
                "detail": (
                    f"Message too long. Maximum is {MAX_CHAT_MESSAGE_LEN} characters "
                    f"(received {len(message)})."
                )
            },
            status_code=400,
        )

    # --- Input sanitization ---
    message = sanitize_text(message, max_len=MAX_CHAT_MESSAGE_LEN)

    # --- Per-post_id rate limit ---
    if not _chat_rate_check(post_id):
        return JSONResponse(
            {
                "detail": (
                    f"Rate limit exceeded. Maximum {_CHAT_MAX_PER_WINDOW} messages "
                    "per minute per post."
                )
            },
            status_code=429,
            headers={"Retry-After": "60"},
        )

    post = get_social_post(post_id)
    if not post:
        return HTMLResponse("<div class='chat-msg assistant'>Post nicht gefunden.</div>")

    save_post_edit(post_id, "user", message)

    user_prompt = EDIT_USER_TEMPLATE.format(
        platform=post["platform"],
        post_content=post["content"],
        user_message=message,
    )

    # Generate revised post
    if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
        from generator.mocks.mock_claude import MockClaudeClient
        result = MockClaudeClient().generate_post(EDIT_SYSTEM_PROMPT, user_prompt, "edit")
        new_content = result["content"]
    else:
        import anthropic
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=EDIT_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        new_content = resp.content[0].text.strip()

    # Persist updated content
    update_social_post(post_id, {"content": new_content})
    save_post_edit(post_id, "assistant", new_content)

    # Return two chat bubbles (user message + assistant reply)
    user_html = f'<div class="chat-msg user">{_escape(message)}</div>'
    assistant_html = (
        f'<div class="chat-msg assistant">'
        f'{_escape(new_content[:300])}{"…" if len(new_content) > 300 else ""}'
        f'</div>'
    )
    return HTMLResponse(user_html + assistant_html)


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )
