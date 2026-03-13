"""MIT Technology Review scraper — RSS feed with keyword filtering."""
import os

from scraper.rss_scraper import RSSBaseScraper
from scraper.mocks.mock_scraper import MockScraper

RSS_URL = "https://www.technologyreview.com/feed/"
MAX_ITEMS = 6

FOCUS_KEYWORDS = [
    "ai", "manufacturing", "automation", "industry", "robot",
    "machine learning", "deep learning", "industrial", "factory",
    "production", "supply chain",
]


class MITTechReviewScraper(RSSBaseScraper):
    SOURCE = "MIT Tech Review"
    RSS_URL = RSS_URL
    MAX_ITEMS = MAX_ITEMS

    def _is_relevant(self, text: str) -> bool:
        lower = text.lower()
        return any(kw in lower for kw in FOCUS_KEYWORDS)

    def _parse_rss_filtered(self, xml_text: str) -> list[dict]:
        all_items = self._parse_rss(xml_text)
        relevant = [a for a in all_items if self._is_relevant(a["title"] + " " + a["summary"])]
        return relevant[:self.MAX_ITEMS]

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return [a for a in MockScraper().scrape() if a["source"] == self.SOURCE]
        try:
            xml_text = self.fetch(self.RSS_URL)
            return self._parse_rss_filtered(xml_text)
        except Exception:
            return []
