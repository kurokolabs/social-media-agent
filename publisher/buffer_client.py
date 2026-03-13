"""Buffer API client with mock fallback."""
import os
from typing import Optional

from publisher.file_output import FileOutput
from security.audit_log import audit_log


class BufferClient:
    """Posts to Buffer API or delegates to MockBufferClient based on USE_MOCK_APIS."""

    def schedule_post(
        self, content: str, scheduled_time: str, image_path: Optional[str] = None
    ) -> dict:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            from publisher.mocks.mock_buffer import MockBufferClient
            return MockBufferClient().schedule_post(content, scheduled_time, image_path)

        import httpx
        token = os.getenv("BUFFER_ACCESS_TOKEN", "")
        channel_id = os.getenv("BUFFER_CHANNEL_ID", "")
        payload = {
            "text": content,
            "profile_ids[]": channel_id,
            "scheduled_at": scheduled_time,
        }
        try:
            resp = httpx.post(
                "https://api.bufferapp.com/1/updates/create.json",
                data={**payload, "access_token": token},
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            audit_log.log("buffer", "schedule_post", 0, 0, 0.0, "success")
            return {"success": True, "post_id": data.get("id"), "scheduled_at": scheduled_time}
        except Exception as e:
            audit_log.log("buffer", "schedule_post", 0, 0, 0.0, "error", str(e))
            fo = FileOutput()
            fo.save({"content": content, "scheduled_at": scheduled_time}, "buffer_failure")
            return {"success": False, "error": str(e)}
