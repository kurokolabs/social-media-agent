"""Extended Buffer API client — LinkedIn, X, Instagram, Threads."""
import os
from typing import Optional

from platforms.base import AbstractSocialClient
from security.audit_log import audit_log


CHANNEL_ENV = {
    "linkedin": "BUFFER_CHANNEL_ID",
    "twitter": "BUFFER_X_CHANNEL_ID",
    "instagram": "BUFFER_IG_CHANNEL_ID",
    "threads": "BUFFER_THREADS_CHANNEL_ID",
}


class BufferExtendedClient(AbstractSocialClient):
    """Posts to any Buffer-supported platform channel."""

    def _get_channel_id(self, platform: str) -> str:
        env_key = CHANNEL_ENV.get(platform, "BUFFER_CHANNEL_ID")
        return os.getenv(env_key, "")

    def schedule_post(
        self,
        content: str,
        scheduled_time: str,
        image_path: Optional[str] = None,
        channel_id: Optional[str] = None,
        platform: str = "linkedin",
    ) -> dict:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            from publisher.mocks.mock_buffer import MockBufferClient
            return MockBufferClient().schedule_post(content, scheduled_time, image_path)

        import httpx

        token = os.getenv("BUFFER_ACCESS_TOKEN", "")
        ch_id = channel_id or self._get_channel_id(platform)

        payload = {
            "text": content,
            "profile_ids[]": ch_id,
            "scheduled_at": scheduled_time,
        }

        files = {}
        if image_path and os.path.exists(image_path):
            files["media[photo]"] = open(image_path, "rb")

        try:
            resp = httpx.post(
                "https://api.bufferapp.com/1/updates/create.json",
                data={**payload, "access_token": token},
                files=files if files else None,
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            audit_log.log("buffer_extended", f"schedule_{platform}", 0, 0, 0.0, "success")
            return {
                "success": True,
                "post_id": data.get("id"),
                "scheduled_at": scheduled_time,
                "platform": platform,
            }
        except Exception as e:
            audit_log.log("buffer_extended", f"schedule_{platform}", 0, 0, 0.0, "error", str(e))
            return {"success": False, "error": str(e), "platform": platform}
        finally:
            for f in files.values():
                f.close()
