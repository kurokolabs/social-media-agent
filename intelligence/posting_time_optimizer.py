"""Data-driven posting time optimizer — Feature 8.

Falls back to hardcoded WEEKLY_SCHEDULE when fewer than MIN_ANALYTICS_SAMPLES
data points exist per platform.
"""
import random
from datetime import datetime, timedelta, timezone


class PostingTimeOptimizer:
    """Computes optimal posting slots based on historical engagement data."""

    # Fallback schedule per platform: list of (weekday, hour_min, hour_max)
    _FALLBACK = {
        "linkedin":  [(0, 8, 10), (2, 8, 10), (4, 8, 10)],
        "twitter":   [(0, 8, 10), (1, 12, 14), (2, 8, 10), (3, 12, 14), (4, 8, 10), (5, 12, 14), (6, 10, 12)],
        "instagram": [(0, 8, 10), (1, 12, 14), (2, 8, 10), (3, 12, 14), (4, 8, 10), (5, 12, 14), (6, 10, 12)],
        "threads":   [(0, 8, 10), (2, 8, 10), (4, 8, 10)],
    }

    def get_optimal_slot(self, platform: str) -> datetime:
        """Return the next optimal posting datetime for the given platform.

        Uses analytics data when sufficient samples exist; otherwise falls back
        to the hardcoded weekly schedule.
        """
        from config import MIN_ANALYTICS_SAMPLES
        from intelligence.performance_tracker import PerformanceTracker

        windows = PerformanceTracker().get_optimal_posting_windows(platform)
        if len(windows) >= MIN_ANALYTICS_SAMPLES:
            return self._slot_from_analytics(platform, windows)
        return self._fallback_slot(platform)

    def _slot_from_analytics(self, platform: str, windows: list[dict]) -> datetime:
        """Pick next slot from the top-3 engagement hours."""
        top_hours = [w["hour"] for w in windows[:3]]
        now = datetime.now(timezone.utc)
        # Look ahead up to 7 days for next occurrence of a top hour
        for delta_hours in range(1, 7 * 24):
            candidate = now + timedelta(hours=delta_hours)
            if candidate.hour in top_hours:
                # Apply ±15 min jitter
                jitter = random.randint(-15, 15)
                return candidate.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=jitter)
        return self._fallback_slot(platform)

    def _fallback_slot(self, platform: str) -> datetime:
        """Return next slot from the hardcoded fallback schedule with ±15 min jitter."""
        slots = self._FALLBACK.get(platform, self._FALLBACK["linkedin"])
        now = datetime.now(timezone.utc)
        # Find next matching weekday+hour slot within the next 14 days
        for delta_hours in range(1, 14 * 24):
            candidate = now + timedelta(hours=delta_hours)
            for weekday, h_min, h_max in slots:
                if candidate.weekday() == weekday and h_min <= candidate.hour < h_max:
                    jitter = random.randint(-15, 15)
                    return candidate.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=jitter)
        # Ultimate fallback: 24 h from now
        return now + timedelta(hours=24)
