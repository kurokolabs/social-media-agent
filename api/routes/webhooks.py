"""Instagram Webhook receiver — gated by IG_DM_AUTOMATION_ENABLED."""
import hashlib
import hmac
import logging
import os

from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from config import MAX_WEBHOOK_BODY_BYTES

router = APIRouter(prefix="/webhooks")
logger = logging.getLogger(__name__)


@router.get("/instagram")
async def instagram_verify(
    hub_mode: str = "",
    hub_verify_token: str = "",
    hub_challenge: str = "",
):
    """Meta webhook verification handshake."""
    if not os.getenv("IG_DM_AUTOMATION_ENABLED", "false").lower() == "true":
        logger.info("webhook.verify.disabled")
        return JSONResponse({"status": "dm_automation_disabled"}, status_code=200)

    expected = os.getenv("IG_WEBHOOK_VERIFY_TOKEN", "")
    if hub_mode == "subscribe" and hmac.compare_digest(hub_verify_token, expected):
        logger.info("webhook.verify.accepted")
        return Response(content=hub_challenge, media_type="text/plain")

    logger.warning("webhook.verify.rejected mode=%r token_match=False", hub_mode)
    return Response(status_code=403)


@router.post("/instagram")
async def instagram_webhook(request: Request):
    """Receive Instagram DM webhook events."""
    if not os.getenv("IG_DM_AUTOMATION_ENABLED", "false").lower() == "true":
        logger.info("webhook.post.disabled")
        return JSONResponse({"status": "dm_automation_disabled"})

    # --- Body size guard (must happen before reading body) ---
    content_length = request.headers.get("content-length")
    if content_length is not None:
        try:
            size = int(content_length)
        except ValueError:
            size = 0
        if size > MAX_WEBHOOK_BODY_BYTES:
            logger.warning("webhook.post.rejected reason=body_too_large size=%d", size)
            return Response(status_code=413)

    body = await request.body()

    # Enforce body size limit even without Content-Length header
    if len(body) > MAX_WEBHOOK_BODY_BYTES:
        logger.warning(
            "webhook.post.rejected reason=body_too_large actual=%d", len(body)
        )
        return Response(status_code=413)

    # --- Signature validation ---
    # Require X-Hub-Signature-256 header
    signature_256 = request.headers.get("X-Hub-Signature-256", "")
    app_secret = os.getenv("IG_APP_SECRET", "")

    if not signature_256:
        logger.warning("webhook.post.rejected reason=missing_signature")
        return Response(status_code=403)

    if app_secret:
        expected_sig = "sha256=" + hmac.new(
            app_secret.encode(), body, hashlib.sha256
        ).hexdigest()
        # Constant-time comparison prevents timing attacks
        if not hmac.compare_digest(signature_256, expected_sig):
            logger.warning("webhook.post.rejected reason=signature_mismatch")
            return Response(status_code=403)

    # --- Parse payload ---
    try:
        payload = await request.json()
    except Exception:
        logger.error("webhook.post.error reason=invalid_json")
        return Response(status_code=400)

    # --- Dispatch DM tasks ---
    dispatched = 0
    for entry in payload.get("entry", []):
        for messaging in entry.get("messaging", []):
            sender_id = messaging.get("sender", {}).get("id")
            message_text = messaging.get("message", {}).get("text", "")
            if sender_id and message_text:
                try:
                    from tasks.publish_tasks import handle_instagram_dm
                    handle_instagram_dm.delay(sender_id, message_text)
                    dispatched += 1
                except Exception:
                    pass  # Celery not running; silently skip

    logger.info("webhook.post.accepted dispatched=%d", dispatched)
    return JSONResponse({"status": "ok"})
