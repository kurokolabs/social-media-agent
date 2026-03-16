"""Bosch Tech Blog scraper — competitor monitoring."""
from scraper.base_scraper import BaseScraper
from config import MAX_ARTICLE_WORDS


class BoschTechScraper(BaseScraper):
    SOURCE = "bosch_tech"
    _URL = "https://www.bosch.com/stories/artificial-intelligence/"
    _RSS = "https://www.bosch.com/stories/rss/"

    def scrape(self) -> list[dict]:
        try:
            from scraper.rss_scraper import RssScraper
            rss = RssScraper(self._RSS, source=self.SOURCE, max_items=5)
            return rss.scrape()
        except Exception:
            pass
        try:
            html = self.fetch(self._URL)
            text = self.extract_text(html)
            return [{
                "url": self._URL,
                "title": "Bosch — KI und Automatisierung",
                "summary": self.truncate(text, MAX_ARTICLE_WORDS),
                "source": self.SOURCE,
            }]
        except Exception:
            return []
