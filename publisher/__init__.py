"""Publisher module — scheduling helpers."""
from datetime import datetime, timezone, timedelta
import pytz


def get_next_slot() -> datetime:
    """Return next available posting slot (Tue/Thu 08-10 or 12-13 CET)."""
    tz = pytz.timezone("Europe/Berlin")
    now = datetime.now(tz)
    # POSTING_DAYS: 1=Tuesday, 3=Thursday (weekday: Mon=0)
    target_days = [1, 3]
    target_hours = [8, 12]

    candidate = now.replace(second=0, microsecond=0)
    # Search up to 14 days × 24 hours to guarantee finding a Tue/Thu slot
    for _ in range(14 * 24):
        candidate += timedelta(hours=1)
        if candidate.weekday() in target_days and candidate.hour in target_hours:
            return candidate.astimezone(timezone.utc)

    # Should be unreachable, but satisfy the type checker
    return (now + timedelta(days=2)).astimezone(timezone.utc)
