"""METI scraper — stub, implemented in Iteration 2."""
import os
from scraper.base_scraper import BaseScraper
from scraper.mocks.mock_scraper import MockScraper


class METIScraper(BaseScraper):
    SOURCE = "meti"

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return [a for a in MockScraper().scrape() if "METI" in a.get("source", "")]
        raise NotImplementedError("Real scraper implemented in Iteration 2")
