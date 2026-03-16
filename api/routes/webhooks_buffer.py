"""Buffer Webhook receiver — Feature 1: Post-Status-Sync.

Buffer POSTs to /webhooks/buffer when a post is published or fails.
We verify the HMAC-SHA256 signature and update social_posts.status in DB.
"""
import hashlib
import hmac
import os

from fastapi import APIRouter, Request, Response, status

router = APIRouter(tags=["webhooks"])

_SUPPORTED_EVENTS = {"post.published", "post.failed"}


def _verify_signature(body: bytes, signature: str) -> bool:
    """Return True if the Buffer webhook signature is valid."""
    secret = os.getenv("BUFFER_WEBHOOK_SECRET", "")
    if not secret:
        # No secret configured — skip verification in dev mode
        return os.getenv("USE_MOCK_APIS", "true").lower() == "true"
    expected = "sha256=" + hmac.new(
        secret.encode(), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/webhooks/buffer", status_code=status.HTTP_204_NO_CONTENT)
async def buffer_webhook(request: Request) -> Response:
    """Receive Buffer post lifecycle events and sync DB status."""
    body = await request.body()
    sig = request.headers.get("x-buffer-signature", "")

    if not _verify_signature(body, sig):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        payload = await request.json()
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    event = payload.get("event", "")
    if event not in _SUPPORTED_EVENTS:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    buffer_post_id = payload.get("post_id") or payload.get("id", "")
    if not buffer_post_id:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    if event == "post.published":
        published_at = payload.get("published_at")
        _update_status(str(buffer_post_id), "published", published_at)
    elif event == "post.failed":
        _update_status(str(buffer_post_id), "failed")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _update_status(buffer_post_id: str, new_status: str, published_at=None) -> None:
    from storage.database import update_post_status
    update_post_status(buffer_post_id, new_status, published_at)
