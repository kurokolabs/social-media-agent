"""Append-only JSONL audit log for all external API calls."""
import json
import os
import threading
from datetime import datetime, timezone
from typing import Optional


class AuditLog:
    """Thread-safe append-only JSONL audit logger."""

    def __init__(self) -> None:
        self._lock = threading.Lock()

    def _get_log_path(self) -> str:
        log_dir = os.getenv("LOG_PATH", "./logs")
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, "audit.jsonl")

    def log(
        self,
        service: str,
        endpoint: str,
        tokens_in: int,
        tokens_out: int,
        cost_usd: float,
        status: str,
        error: Optional[str] = None,
    ) -> None:
        """Append a log entry to audit.jsonl. Never raises."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": service,
            "endpoint": endpoint,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "cost_usd": round(cost_usd, 6),
            "status": status,
            "error": error,
        }
        try:
            with self._lock:
                with open(self._get_log_path(), "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry) + "\n")
        except Exception:
            pass  # Audit log must never crash the pipeline


audit_log = AuditLog()
