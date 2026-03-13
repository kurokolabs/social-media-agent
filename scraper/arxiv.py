"""arXiv scraper for manufacturing AI papers."""
import os
from scraper.base_scraper import BaseScraper
from scraper.mocks.mock_scraper import MockScraper
from config import MAX_ARTICLE_WORDS


class ArXivScraper(BaseScraper):
    SOURCE = "arxiv"
    SEARCH_URL = "https://arxiv.org/search/?searchtype=all&query=manufacturing+AI+automation&start=0"

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return [a for a in MockScraper().scrape() if a["source"] == "arXiv"]
        try:
            html = self.fetch(self.SEARCH_URL)
            text = self.extract_text(html)
            summary = self.truncate(text, MAX_ARTICLE_WORDS)
            return [{
                "url": self.SEARCH_URL,
                "title": "arXiv: Manufacturing AI Research",
                "summary": summary,
                "source": self.SOURCE,
            }]
        except Exception:
            return []
