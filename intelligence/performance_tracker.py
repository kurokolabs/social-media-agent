"""Performance Feedback Loop — syncs Buffer Analytics and computes engagement stats."""
import os
from datetime import datetime, timezone, timedelta
from typing import Optional

from security.audit_log import audit_log


class PerformanceTracker:
    """Fetches Buffer analytics and stores engagement data in social_posts."""

    def sync_analytics(self) -> dict:
        """Pull analytics for all published posts and update DB. Returns summary dict."""
        from storage.database import get_connection

        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT id, buffer_post_id, platform FROM social_posts "
                "WHERE status = 'published' AND buffer_post_id IS NOT NULL"
            ).fetchall()
        finally:
            conn.close()

        updated = 0
        errors = 0
        for row in rows:
            try:
                metrics = self._fetch_metrics(row["buffer_post_id"])
                if metrics:
                    self._update_metrics(row["id"], metrics)
                    updated += 1
            except Exception:
                errors += 1

        audit_log.log("buffer", "sync_analytics", 0, 0, 0.0, "success")
        return {"updated": updated, "errors": errors}

    def _fetch_metrics(self, buffer_post_id: str) -> Optional[dict]:
        """Fetch analytics from Buffer API for a single post."""
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            # Return mock metrics for testing
            import random
            return {
                "likes": random.randint(0, 150),
                "comments": random.randint(0, 30),
                "shares": random.randint(0, 50),
                "reach": random.randint(100, 5000),
                "impressions": random.randint(200, 10000),
            }

        import httpx
        token = os.getenv("BUFFER_ACCESS_TOKEN", "")
        try:
            resp = httpx.get(
                f"https://api.bufferapp.com/1/updates/{buffer_post_id}/interactions.json",
                params={"access_token": token, "event": "likes", "count": 1},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "likes": data.get("total", 0),
                "comments": data.get("comments", 0),
                "shares": data.get("shares", 0),
                "reach": data.get("reach", 0),
                "impressions": data.get("impressions", 0),
            }
        except Exception:
            return None

    def _update_metrics(self, post_id: int, metrics: dict) -> None:
        from storage.database import update_social_post
        update_social_post(post_id, metrics)

    def get_top_performing_post_types(self, platform: str, n: int = 5) -> list[dict]:
        """Return post types ranked by average engagement score for a platform."""
        from storage.database import get_connection

        conn = get_connection()
        try:
            rows = conn.execute(
                """SELECT post_type,
                          COUNT(*) as post_count,
                          AVG(likes + comments * 2 + shares * 3) as avg_engagement
                   FROM social_posts
                   WHERE platform = ? AND status = 'published'
                   GROUP BY post_type
                   HAVING post_count >= 1
                   ORDER BY avg_engagement DESC
                   LIMIT ?""",
                (platform, n),
            ).fetchall()
        finally:
            conn.close()

        return [dict(r) for r in rows]

    def get_optimal_posting_windows(self, platform: str) -> list[dict]:
        """Return hours ranked by average engagement, based on published_at times."""
        from storage.database import get_connection

        conn = get_connection()
        try:
            rows = conn.execute(
                """SELECT CAST(strftime('%H', published_at) AS INTEGER) as hour,
                          COUNT(*) as post_count,
                          AVG(likes + comments * 2 + shares * 3) as avg_engagement
                   FROM social_posts
                   WHERE platform = ? AND status = 'published' AND published_at IS NOT NULL
                   GROUP BY hour
                   ORDER BY avg_engagement DESC
                   LIMIT 5""",
                (platform,),
            ).fetchall()
        finally:
            conn.close()

        return [dict(r) for r in rows]
