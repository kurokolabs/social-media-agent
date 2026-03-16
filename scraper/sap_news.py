"""SAP News Center AI category scraper — competitor monitoring."""
from scraper.base_scraper import BaseScraper
from config import MAX_ARTICLE_WORDS


class SAPNewsScraper(BaseScraper):
    SOURCE = "sap_news"
    _URL = "https://news.sap.com/topics/artificial-intelligence/"
    _RSS = "https://news.sap.com/feed/"

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
                "title": "SAP News — AI",
                "summary": self.truncate(text, MAX_ARTICLE_WORDS),
                "source": self.SOURCE,
            }]
        except Exception:
            return []
