"""Google AI Blog scraper — research publications and model announcements."""
import os

from scraper.base_scraper import BaseScraper
from scraper.rss_scraper import RssScraper
from config import MAX_ARTICLE_WORDS

RSS_FEEDS = [
    "https://blog.research.google/feeds/posts/default?alt=rss",
    "https://ai.googleblog.com/feeds/posts/default?alt=rss",
]
HTML_URL = "https://blog.research.google/"


class GoogleAIBlogScraper(BaseScraper):
    SOURCE = "Google AI Blog"

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return []

        for rss_url in RSS_FEEDS:
            try:
                articles = RssScraper(self.SOURCE, rss_url, max_items=10).scrape()
                if articles:
                    return articles
            except Exception:
                continue

        # HTML fallback
        try:
            html = self.fetch(HTML_URL)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "lxml")
            articles = []
            for item in soup.select("article, .post, [class*='Post']")[:10]:
                a_tag = item.find("a", href=True)
                if not a_tag:
                    continue
                href  = a_tag["href"]
                url   = href if href.startswith("http") else f"https://blog.research.google{href}"
                title_el = item.find(["h2", "h3"])
                title    = title_el.get_text(strip=True) if title_el else a_tag.get_text(strip=True)
                summary_el = item.find("p")
                summary    = summary_el.get_text(strip=True) if summary_el else ""
                if title and url:
                    articles.append({
                        "url":     url,
                        "title":   title,
                        "summary": self.truncate(summary, MAX_ARTICLE_WORDS),
                        "source":  self.SOURCE,
                    })
            return articles
        except Exception:
            return []
