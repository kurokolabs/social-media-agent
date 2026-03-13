"""Base scraper with rate limiting, robots.txt, retry, and HTML extraction."""
import random
import re
import threading
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup

from security.rate_limiter import RateLimiter
from security.audit_log import audit_log

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
]

_rate_limiter = RateLimiter()
_robots_cache: dict[str, RobotFileParser] = {}
_robots_lock = threading.Lock()


class ScraperBlockedError(Exception):
    """Raised when robots.txt blocks access."""


class BaseScraper:
    """Base class with fetch, extract_text, truncate, robots.txt checking."""

    SOURCE = "base"

    def scrape(self) -> list[dict]:
        raise NotImplementedError

    def _check_robots(self, url: str) -> None:
        """Raise ScraperBlockedError if robots.txt disallows this URL."""
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        with _robots_lock:
            if robots_url not in _robots_cache:
                rp = RobotFileParser()
                rp.set_url(robots_url)
                try:
                    rp.read()
                except Exception:
                    _robots_cache[robots_url] = None
                    return
                _robots_cache[robots_url] = rp
            rp = _robots_cache[robots_url]

        if rp and not rp.can_fetch("*", url):
            raise ScraperBlockedError(f"robots.txt blocks: {url}")

    def fetch(self, url: str) -> str:
        """Fetch URL with rate limiting, user-agent rotation, retries."""
        domain = urlparse(url).netloc
        _rate_limiter.wait(domain)
        self._check_robots(url)

        headers = {"User-Agent": random.choice(USER_AGENTS)}
        last_error = None
        for attempt in range(3):
            try:
                resp = httpx.get(url, headers=headers, timeout=30, follow_redirects=True)
                if resp.status_code in (429, 503):
                    wait = 2 ** attempt * 5
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                audit_log.log(self.SOURCE, url, 0, 0, 0.0, "success")
                return resp.text
            except ScraperBlockedError:
                raise
            except Exception as e:
                last_error = e
                if attempt < 2:
                    time.sleep(2 ** attempt)
        audit_log.log(self.SOURCE, url, 0, 0, 0.0, "error", str(last_error))
        raise RuntimeError(f"Failed to fetch {url} after 3 attempts: {last_error}")

    def extract_text(self, html: str) -> str:
        """Strip all HTML tags, collapse whitespace."""
        soup = BeautifulSoup(html, "lxml")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator=" ")
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def truncate(self, text: str, max_words: int) -> str:
        """Return first max_words words of text."""
        words = text.split()
        if len(words) <= max_words:
            return text
        return " ".join(words[:max_words])
