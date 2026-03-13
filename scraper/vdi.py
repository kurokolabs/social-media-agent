"""VDI scraper."""
import os
from scraper.base_scraper import BaseScraper
from scraper.mocks.mock_scraper import MockScraper
from config import MAX_ARTICLE_WORDS


class VDIScraper(BaseScraper):
    SOURCE = "vdi"
    BASE_URL = "https://www.vdi.de/news"

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return [a for a in MockScraper().scrape() if a["source"] == "VDI"]
        try:
            html = self.fetch(self.BASE_URL)
            text = self.extract_text(html)
            summary = self.truncate(text, MAX_ARTICLE_WORDS)
            return [{
                "url": self.BASE_URL,
                "title": "VDI: Industrie und Digitalisierung",
                "summary": summary,
                "source": self.SOURCE,
            }]
        except Exception:
            return []
