"""Celery tasks for async publishing via Buffer."""
import random
from datetime import datetime, timedelta

from tasks.celery_app import celery_app


def get_jitter_time(scheduled_time: datetime) -> datetime:
    """±15 minutes jitter for human-like posting behaviour."""
    jitter = random.randint(-15, 15)
    return scheduled_time + timedelta(minutes=jitter)


@celery_app.task(bind=True, max_retries=3)
def publish_post_to_buffer(self, post_id: int) -> dict:
    """Publish an approved post to Buffer. Applies jitter to scheduled time."""
    try:
        from storage.database import get_social_post, update_social_post
        from platforms.buffer_extended import BufferExtendedClient

        post = get_social_post(post_id)
        if not post:
            return {"success": False, "error": f"Post {post_id} not found"}

        scheduled_raw = post.get("scheduled_at")
        if scheduled_raw:
            scheduled_dt = datetime.fromisoformat(str(scheduled_raw))
            scheduled_dt = get_jitter_time(scheduled_dt)
            scheduled_str = scheduled_dt.isoformat()
        else:
            scheduled_str = datetime.utcnow().isoformat()

        client = BufferExtendedClient()
        result = client.schedule_post(
            content=post["content"],
            scheduled_time=scheduled_str,
            image_path=post.get("image_path"),
            platform=post["platform"],
        )

        if result.get("success"):
            update_social_post(post_id, {
                "status": "scheduled",
                "buffer_post_id": result.get("post_id"),
                "scheduled_at": scheduled_str,
            })
        else:
            update_social_post(post_id, {"status": "failed"})

        return result
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(bind=True, max_retries=2)
def handle_instagram_dm(self, user_id: str, message_text: str) -> dict:
    """Handle incoming Instagram DM — only runs when IG_DM_AUTOMATION_ENABLED=true."""
    import os
    if os.getenv("IG_DM_AUTOMATION_ENABLED", "false").lower() != "true":
        return {"status": "dm_automation_disabled"}

    try:
        import anthropic
        from generator.prompts import WESSAL_SYSTEM_PROMPT

        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=WESSAL_SYSTEM_PROMPT + "\n\nDu antwortest auf eine Instagram-DM. Sei freundlich, kurz, hilfreich.",
            messages=[{"role": "user", "content": message_text}],
        )
        reply = response.content[0].text.strip()

        # Send reply via Instagram Graph API
        ig_token = os.getenv("IG_ACCESS_TOKEN", "")
        ig_account_id = os.getenv("IG_ACCOUNT_ID", "")
        if ig_token and ig_account_id:
            import httpx
            httpx.post(
                f"https://graph.instagram.com/v18.0/{ig_account_id}/messages",
                json={"recipient": {"id": user_id}, "message": {"text": reply}},
                params={"access_token": ig_token},
                timeout=15,
            )

        from storage.database import save_post_edit
        # Reuse post_edits table with post_id=0 for DMs
        save_post_edit(0, "user", f"DM from {user_id}: {message_text}")
        save_post_edit(0, "assistant", reply)

        return {"success": True, "reply": reply}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)
