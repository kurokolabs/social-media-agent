"""Background monitor that checks high-signal sources every 2 hours."""
import threading
import time
from datetime import datetime


# Mapping from friendly source name to scraper class import path
_SOURCE_SCRAPER_MAP = {
    "OpenAI Blog":    ("scraper.openai_blog",         "OpenAIBlogScraper"),
    "Anthropic":      ("scraper.anthropic_research",  "AnthropicResearchScraper"),
    "DeepMind":       ("scraper.deepmind_blog",       "DeepMindBlogScraper"),
    "Google AI Blog": ("scraper.google_ai_blog",      "GoogleAIBlogScraper"),
    "HuggingFace":    ("scraper.huggingface_blog",    "HuggingFaceBlogScraper"),
    "arXiv-LLM":      ("scraper.arxiv_llm",           "ArXivLLMScraper"),
    "PapersWithCode": ("scraper.papers_with_code",    "PapersWithCodeScraper"),
}


class AlertMonitor:
    """Polls breaking-news sources and saves new alerts to DB."""

    CHECK_INTERVAL_SECONDS = 7200  # 2 hours

    # Sources to poll for breaking news (subset of all scrapers, highest signal)
    MONITORED_SOURCES = [
        "OpenAI Blog",
        "Anthropic",
        "DeepMind",
        "Google AI Blog",
        "HuggingFace",
        "arXiv-LLM",
        "PapersWithCode",
    ]

    def __init__(self):
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._last_check: datetime | None = None

    def _run_check(self) -> int:
        """Run one alert check cycle. Returns number of new alerts saved."""
        from intelligence.alert_classifier import classify
        from storage.database import save_alert

        new_count = 0

        for source_name in self.MONITORED_SOURCES:
            if source_name not in _SOURCE_SCRAPER_MAP:
                continue

            module_path, class_name = _SOURCE_SCRAPER_MAP[source_name]
            try:
                import importlib
                module = importlib.import_module(module_path)
                scraper_cls = getattr(module, class_name)
                scraper = scraper_cls()
                articles = scraper.scrape()
            except Exception:
                continue

            for article in articles:
                try:
                    alert_type, priority = classify(article)
                    row_id = save_alert(
                        source=article.get("source", source_name),
                        title=article.get("title", ""),
                        url=article.get("url", ""),
                        summary=article.get("summary", ""),
                        alert_type=alert_type,
                        priority=priority,
                    )
                    if row_id:
                        new_count += 1
                except Exception:
                    continue

        self._last_check = datetime.utcnow()
        return new_count

    def _loop(self) -> None:
        """Background thread loop: check immediately, then every CHECK_INTERVAL_SECONDS."""
        self._run_check()
        while not self._stop_event.wait(self.CHECK_INTERVAL_SECONDS):
            self._run_check()

    def start(self) -> None:
        """Start background monitoring thread."""
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._loop,
            name="alert-monitor",
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        """Stop the background thread."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None

    def check_now(self) -> int:
        """Manually trigger a check. Returns count of new alerts."""
        return self._run_check()

    def status(self) -> dict:
        """Return monitor status dict."""
        return {
            "running": self._thread is not None and self._thread.is_alive(),
            "last_check": self._last_check.isoformat() if self._last_check else None,
            "check_interval_seconds": self.CHECK_INTERVAL_SECONDS,
            "monitored_sources": self.MONITORED_SOURCES,
        }


# Singleton
alert_monitor = AlertMonitor()
