"""Evergreen Content Rotation — Feature 6.

Re-schedules high-engagement X and Threads posts after 60 days.
LinkedIn posts are never re-used (too close to original, audience overlap).
"""
from datetime import datetime, timezone, timedelta


_ENGAGEMENT_THRESHOLD = 50   # likes + shares combined


class EvergreenRotator:
    """Identifies evergreen candidates and creates new scheduled post entries."""

    def find_candidates(self) -> list[dict]:
        """Return posts eligible for evergreen re-scheduling."""
        from storage.database import get_connection

        cutoff = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()
        conn = get_connection()
        try:
            rows = conn.execute(
                """SELECT * FROM social_posts
                   WHERE platform IN ('twitter', 'threads')
                   AND status = 'published'
                   AND is_evergreen = 0
                   AND (likes + shares) >= ?
                   AND created_at < ?
                   ORDER BY (likes + shares) DESC""",
                (_ENGAGEMENT_THRESHOLD, cutoff),
            ).fetchall()
        finally:
            conn.close()

        return [dict(r) for r in rows]

    def rotate(self) -> dict:
        """Create new pending posts for all evergreen candidates.

        Returns a summary dict with {'rotated': n}.
        """
        from storage.database import save_social_post, update_social_post
        from intelligence.posting_time_optimizer import PostingTimeOptimizer

        optimizer = PostingTimeOptimizer()
        candidates = self.find_candidates()
        rotated = 0

        for post in candidates:
            platform = post["platform"]
            scheduled_at = optimizer.get_optimal_slot(platform)

            new_post = {
                "platform": platform,
                "content": post["content"],
                "image_path": post.get("image_path"),
                "status": "scheduled",
                "scheduled_at": scheduled_at.isoformat(),
                "post_type": post.get("post_type"),
                "quality_score": post.get("quality_score"),
                "article_id": post.get("article_id"),
            }
            new_id = save_social_post(new_post)

            # Mark the original as evergreen so it isn't rotated again
            update_social_post(post["id"], {"is_evergreen": 1})

            # Link the new post back to the original via repurposed_from_id
            update_social_post(new_id, {"repurposed_from_id": post["id"]})
            rotated += 1

        return {"rotated": rotated, "candidates_found": len(candidates)}
