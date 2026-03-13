"""Fraunhofer scraper."""
import os
from scraper.base_scraper import BaseScraper
from scraper.mocks.mock_scraper import MockScraper
from config import MAX_ARTICLE_WORDS


class FraunhoferScraper(BaseScraper):
    SOURCE = "fraunhofer"
    BASE_URL = "https://www.fraunhofer.de/de/presse/presseinformationen.html"

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return [a for a in MockScraper().scrape() if a["source"] == "Fraunhofer"]
        try:
            html = self.fetch(self.BASE_URL)
            text = self.extract_text(html)
            summary = self.truncate(text, MAX_ARTICLE_WORDS)
            return [{
                "url": self.BASE_URL,
                "title": "Fraunhofer: KI und Automatisierung",
                "summary": summary,
                "source": self.SOURCE,
            }]
        except Exception:
            return []
