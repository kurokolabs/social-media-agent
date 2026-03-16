"""OpenAI blog scraper — model announcements for Instagram."""
from scraper.base_scraper import BaseScraper
from config import MAX_ARTICLE_WORDS


class OpenAIBlogScraper(BaseScraper):
    SOURCE = "openai_blog"
    _URL = "https://openai.com/news/"
    _RSS = "https://openai.com/blog/rss.xml"

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
                "title": "OpenAI News — Latest",
                "summary": self.truncate(text, MAX_ARTICLE_WORDS),
                "source": self.SOURCE,
            }]
        except Exception:
            return []
