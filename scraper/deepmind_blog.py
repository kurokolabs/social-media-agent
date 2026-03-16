"""Google DeepMind research blog scraper — RSS feed with HTML fallback."""
import os

from scraper.base_scraper import BaseScraper
from scraper.rss_scraper import RssScraper
from config import MAX_ARTICLE_WORDS

RSS_URL  = "https://deepmind.google/blog/feed/rss/"
HTML_URL = "https://deepmind.google/discover/blog/"


class DeepMindBlogScraper(BaseScraper):
    SOURCE = "DeepMind"

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return []
        try:
            articles = RssScraper(self.SOURCE, RSS_URL, max_items=10).scrape()
            if articles:
                return articles
        except Exception:
            pass

        # HTML fallback — DeepMind blog cards
        try:
            html = self.fetch(HTML_URL)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "lxml")
            articles = []
            for card in soup.select("article, [data-testid='blog-card']")[:10]:
                a_tag = card.find("a", href=True)
                if not a_tag:
                    continue
                href  = a_tag["href"]
                url   = href if href.startswith("http") else f"https://deepmind.google{href}"
                title_el = card.find(["h2", "h3"])
                title    = title_el.get_text(strip=True) if title_el else a_tag.get_text(strip=True)
                summary_el = card.find("p")
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
