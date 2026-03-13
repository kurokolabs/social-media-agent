"""APScheduler job runner — runs pipeline on Tue/Thu at 07:00 CET."""
import json
import os
import traceback
from datetime import datetime, timezone
from pathlib import Path

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


def run_pipeline_job() -> None:
    """Scheduled job wrapper with failure logging."""
    try:
        from main import run_full_pipeline
        run_full_pipeline()
    except Exception as e:
        os.makedirs("logs/failures", exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        failure = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": str(e),
            "traceback": traceback.format_exc(),
        }
        Path(f"logs/failures/{timestamp}_failure.json").write_text(
            json.dumps(failure, indent=2), encoding="utf-8"
        )
        raise


def start_scheduler() -> None:
    """Start the blocking APScheduler."""
    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_pipeline_job,
        CronTrigger(
            day_of_week="tue,thu",
            hour=7,
            minute=0,
            timezone="Europe/Berlin",
        ),
    )
    scheduler.start()


if __name__ == "__main__":
    start_scheduler()
