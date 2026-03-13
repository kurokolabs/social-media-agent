"""McKinsey Insights scraper."""
import os
from scraper.base_scraper import BaseScraper
from scraper.mocks.mock_scraper import MockScraper
from config import MAX_ARTICLE_WORDS

FOCUS_KEYWORDS = [
    "KI", "AI", "Automatisierung", "Manufacturing", "IoT", "Fertigung",
    "Japan", "Deutschland", "Mittelstand", "Industry 4.0", "Predictive Maintenance",
]


class McKinseyScraper(BaseScraper):
    SOURCE = "mckinsey"
    BASE_URL = "https://www.mckinsey.com/industries/industrials-and-electronics/our-insights"

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return [a for a in MockScraper().scrape() if a["source"] == "McKinsey"]
        try:
            html = self.fetch(self.BASE_URL)
            text = self.extract_text(html)
            summary = self.truncate(text, MAX_ARTICLE_WORDS)
            return [{
                "url": self.BASE_URL,
                "title": "McKinsey: Industrial AI Insights",
                "summary": summary,
                "source": self.SOURCE,
            }]
        except Exception:
            return []
