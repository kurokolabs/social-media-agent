"""TechCrunch AI section scraper — for Instagram and X content."""
from scraper.base_scraper import BaseScraper
from config import MAX_ARTICLE_WORDS


class TechCrunchAIScraper(BaseScraper):
    SOURCE = "techcrunch_ai"
    _URL = "https://techcrunch.com/category/artificial-intelligence/"
    _RSS = "https://techcrunch.com/category/artificial-intelligence/feed/"

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
                "title": "TechCrunch AI — Latest",
                "summary": self.truncate(text, MAX_ARTICLE_WORDS),
                "source": self.SOURCE,
            }]
        except Exception:
            return []
