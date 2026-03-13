"""Per-domain rate limiter with jitter for polite scraping."""
import random
import threading
import time


class RateLimiter:
    """Thread-safe rate limiter enforcing minimum delay between requests per domain."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._last_request: dict[str, float] = {}

    def wait(self, domain: str) -> None:
        """Block until it is safe to make a request to the given domain."""
        with self._lock:
            last = self._last_request.get(domain, 0.0)
            delay = random.uniform(2.5, 5.0)
            sleep_for = delay - (time.time() - last)
            # Reserve the slot before releasing the lock so no other thread steals it
            self._last_request[domain] = time.time() + max(sleep_for, 0)

        # Sleep OUTSIDE the lock — other domains must not be blocked during our wait
        if sleep_for > 0:
            time.sleep(sleep_for)
