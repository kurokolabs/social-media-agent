"""DeepL blog scraper — competitor monitoring."""
from scraper.base_scraper import BaseScraper
from config import MAX_ARTICLE_WORDS


class DeepLBlogScraper(BaseScraper):
    SOURCE = "deepl_blog"
    _URL = "https://www.deepl.com/en/blog"
    _RSS = "https://www.deepl.com/blog/feed.xml"

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
                "title": "DeepL Blog — Latest",
                "summary": self.truncate(text, MAX_ARTICLE_WORDS),
                "source": self.SOURCE,
            }]
        except Exception:
            return []
