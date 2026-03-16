"""Abstract base for social platform clients."""
from abc import ABC, abstractmethod
from typing import Optional


class AbstractSocialClient(ABC):
    """Base interface for posting to social platforms via Buffer."""

    @abstractmethod
    def schedule_post(
        self,
        content: str,
        scheduled_time: str,
        image_path: Optional[str] = None,
        channel_id: Optional[str] = None,
    ) -> dict:
        """Schedule a post. Returns dict with success, post_id, scheduled_at."""
        ...
