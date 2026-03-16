"""Publisher module — scheduling helpers."""
from datetime import datetime, timezone, timedelta
import pytz


def get_next_slot(platform: str = "linkedin") -> datetime:
    """Return next available posting slot.

    Delegates to PostingTimeOptimizer when sufficient analytics data exists
    (MIN_ANALYTICS_SAMPLES), otherwise falls back to the hardcoded Tue/Thu schedule
    for LinkedIn and to the weekly planner schedule for other platforms.
    """
    try:
        from intelligence.posting_time_optimizer import PostingTimeOptimizer
        return PostingTimeOptimizer().get_optimal_slot(platform)
    except Exception:
        pass

    # Hard fallback: Tue/Thu 08:00 or 12:00 CET (original behaviour)
    tz = pytz.timezone("Europe/Berlin")
    now = datetime.now(tz)
    target_days = [1, 3]
    target_hours = [8, 12]

    candidate = now.replace(second=0, microsecond=0)
    for _ in range(14 * 24):
        candidate += timedelta(hours=1)
        if candidate.weekday() in target_days and candidate.hour in target_hours:
            return candidate.astimezone(timezone.utc)

    return (now + timedelta(days=2)).astimezone(timezone.utc)
