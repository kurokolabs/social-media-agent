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


def run_weekly_planner_job() -> None:
    """Sunday 22:00 CET — generate next week's posts for all platforms."""
    try:
        from scheduler.weekly_planner import run_weekly
        result = run_weekly()
        print(f"Weekly planner: {result}")
    except Exception as e:
        os.makedirs("logs/failures", exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        failure = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": str(e),
            "traceback": traceback.format_exc(),
        }
        Path(f"logs/failures/{timestamp}_weekly_failure.json").write_text(
            json.dumps(failure, indent=2), encoding="utf-8"
        )
        raise


def _make_job_wrapper(fn_path: str, label: str):
    """Return a safe job wrapper that logs failures to logs/failures/."""
    def job():
        try:
            module_path, fn_name = fn_path.rsplit(".", 1)
            import importlib
            mod = importlib.import_module(module_path)
            result = getattr(mod, fn_name)()
            print(f"{label}: {result}")
        except Exception as e:
            os.makedirs("logs/failures", exist_ok=True)
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            failure = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "job": label,
                "error": str(e),
                "traceback": traceback.format_exc(),
            }
            Path(f"logs/failures/{timestamp}_{label}_failure.json").write_text(
                json.dumps(failure, indent=2), encoding="utf-8"
            )
    job.__name__ = label
    return job


def start_scheduler() -> None:
    """Start the blocking APScheduler."""
    scheduler = BlockingScheduler()

    # ---- Existing jobs ----
    scheduler.add_job(
        run_pipeline_job,
        CronTrigger(day_of_week="tue,thu", hour=7, minute=0, timezone="Europe/Berlin"),
    )
    scheduler.add_job(
        run_weekly_planner_job,
        CronTrigger(day_of_week="sun", hour=22, minute=0, timezone="Europe/Berlin"),
    )

    # ---- Phase 2 jobs ----
    # Feature 5: Analytics sync — daily 04:00
    scheduler.add_job(
        _make_job_wrapper("scheduler.weekly_planner.run_analytics_sync", "analytics_sync"),
        CronTrigger(hour=4, minute=0, timezone="Europe/Berlin"),
    )
    # Feature 2: Repurposing — daily 06:00
    scheduler.add_job(
        _make_job_wrapper("scheduler.weekly_planner.run_repurposing", "repurposing"),
        CronTrigger(hour=6, minute=0, timezone="Europe/Berlin"),
    )
    # Feature 6: Evergreen rotation — every Monday 07:00
    scheduler.add_job(
        _make_job_wrapper("scheduler.weekly_planner.run_evergreen_rotation", "evergreen_rotation"),
        CronTrigger(day_of_week="mon", hour=7, minute=0, timezone="Europe/Berlin"),
    )
    # Feature 7: Longform post — every Wednesday 07:30
    scheduler.add_job(
        _make_job_wrapper("scheduler.weekly_planner.run_longform_wednesday", "longform_wednesday"),
        CronTrigger(day_of_week="wed", hour=7, minute=30, timezone="Europe/Berlin"),
    )

    scheduler.start()


if __name__ == "__main__":
    start_scheduler()
