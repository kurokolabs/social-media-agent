"""Fraunhofer press release scraper — RSS feed."""
import os

from scraper.rss_scraper import RSSBaseScraper
from scraper.mocks.mock_scraper import MockScraper

RSS_URL = "https://www.fraunhofer.de/de/presse/presseinformationen.rss2.xml"


class FraunhoferScraper(RSSBaseScraper):
    SOURCE = "Fraunhofer"
    RSS_URL = RSS_URL
    MAX_ITEMS = 8

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return [a for a in MockScraper().scrape() if a["source"] == self.SOURCE]
        try:
            xml_text = self.fetch(self.RSS_URL)
            return self._parse_rss(xml_text)
        except Exception:
            return []
