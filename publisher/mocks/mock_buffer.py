"""Mock Buffer client for local testing."""
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class MockBufferClient:
    """Simulates Buffer API — saves to output/mock_published/ instead."""

    def schedule_post(
        self, content: str, scheduled_time: str, image_path: Optional[str] = None
    ) -> dict:
        os.makedirs("output/mock_published", exist_ok=True)
        now = datetime.now(timezone.utc)
        timestamp = now.strftime("%Y%m%d_%H%M%S_%f")
        post_id = f"mock_{timestamp}"
        filename = f"output/mock_published/{timestamp}.md"
        body = f"""---
post_id: {post_id}
scheduled_at: {scheduled_time}
image_path: {image_path or "none"}
published_at: {now.isoformat()}
---

{content}
"""
        Path(filename).write_text(body, encoding="utf-8")
        return {"success": True, "post_id": post_id, "scheduled_at": str(scheduled_time)}
