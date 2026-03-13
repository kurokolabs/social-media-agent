"""Deduplication checker using SQLite topic_history table."""
import os
import re
import sqlite3
from datetime import datetime, timezone, timedelta

from config import DEDUP_DAYS


class DedupChecker:
    """Prevents posting duplicate topics within DEDUP_DAYS window."""

    def _conn(self) -> sqlite3.Connection:
        db_path = os.getenv("DATABASE_PATH", "./kuroko.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def is_duplicate(self, topic_slug: str) -> bool:
        """Return True if this slug was posted within DEDUP_DAYS."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=DEDUP_DAYS)).isoformat()
        conn = self._conn()
        try:
            row = conn.execute(
                "SELECT id FROM topic_history WHERE topic_slug = ? AND posted_at > ?",
                (topic_slug, cutoff),
            ).fetchone()
            return row is not None
        finally:
            conn.close()

    def record_topic(self, topic_slug: str) -> None:
        """Record this topic as posted now."""
        conn = self._conn()
        try:
            conn.execute(
                "INSERT INTO topic_history (topic_slug, posted_at) VALUES (?, ?)",
                (topic_slug, datetime.now(timezone.utc).isoformat()),
            )
            conn.commit()
        finally:
            conn.close()

    def generate_slug(self, title: str) -> str:
        """Convert title to lowercase URL-safe slug, max 60 chars."""
        slug = title.lower()
        slug = re.sub(r"[äöüß]", lambda m: {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}[m.group()], slug)
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        slug = slug.strip("-")
        return slug[:60]
