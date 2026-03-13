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
            now = time.time()
            elapsed = now - last
            delay = random.uniform(2.5, 5.0)
            if elapsed < delay:
                time.sleep(delay - elapsed)
            self._last_request[domain] = time.time()
