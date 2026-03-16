"""Per-domain rate limiter using a token bucket algorithm for polite scraping."""
import threading
import time


class RateLimiter:
    """Thread-safe token bucket rate limiter with per-domain tracking.

    Each domain gets its own bucket that refills at `rate` tokens/second up to
    a maximum of `burst` tokens. Callers block in `wait()` until a token is
    available.

    Default: 1 req/sec, burst of 3 (suitable for scrapers).
    """

    def __init__(self, rate: float = 1.0, burst: int = 3) -> None:
        """Initialise with a refill rate and maximum burst size.

        Parameters
        ----------
        rate:
            Tokens (requests) added per second for each domain bucket.
        burst:
            Maximum number of tokens a bucket can accumulate.
        """
        self._rate = rate
        self._burst = burst
        self._lock = threading.Lock()
        # Per-domain state: (tokens_available, last_refill_time)
        self._buckets: dict[str, tuple[float, float]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def wait(self, domain: str) -> None:
        """Block until a token is available for the given domain.

        The lock is held only while checking/updating state; sleeping happens
        outside the lock so other domains are not blocked during the wait.
        """
        while True:
            sleep_for = self._consume(domain)
            if sleep_for <= 0:
                return
            time.sleep(sleep_for)

    def reset(self, domain: str | None = None) -> None:
        """Reset bucket state.  Useful in tests.

        If *domain* is given, only that domain's bucket is removed.
        If *domain* is None, all buckets are cleared.
        """
        with self._lock:
            if domain is None:
                self._buckets.clear()
            else:
                self._buckets.pop(domain, None)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _consume(self, domain: str) -> float:
        """Try to consume one token.  Returns 0 on success, or seconds to wait."""
        with self._lock:
            now = time.monotonic()
            tokens, last_refill = self._buckets.get(domain, (float(self._burst), now))

            # Refill bucket proportionally to elapsed time
            elapsed = now - last_refill
            tokens = min(float(self._burst), tokens + elapsed * self._rate)

            if tokens >= 1.0:
                # Token available — consume it immediately
                self._buckets[domain] = (tokens - 1.0, now)
                return 0.0
            else:
                # Not enough tokens — calculate how long to wait for 1 token
                wait_seconds = (1.0 - tokens) / self._rate
                # Update last_refill so the next call accounts for elapsed time
                self._buckets[domain] = (tokens, now)
                return wait_seconds
