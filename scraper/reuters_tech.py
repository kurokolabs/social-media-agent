"""Reuters Technology scraper — RSS feed with HTML fallback and keyword filtering."""
import os

from bs4 import BeautifulSoup

from scraper.rss_scraper import RSSBaseScraper
from scraper.mocks.mock_scraper import MockScraper
from config import MAX_ARTICLE_WORDS

RSS_URL = "https://feeds.reuters.com/reuters/technologyNews"
FALLBACK_URL = "https://www.reuters.com/technology/"
BASE_URL = "https://www.reuters.com"
MAX_ITEMS = 6

FOCUS_KEYWORDS = [
    "ai", "manufacturing", "industrial", "automation", "robot",
    "factory", "production", "supply chain", "machine learning",
    "industry 4.0", "semiconductor", "chip",
]


class ReutersTechScraper(RSSBaseScraper):
    SOURCE = "Reuters"
    RSS_URL = RSS_URL
    MAX_ITEMS = MAX_ITEMS

    def _is_relevant(self, text: str) -> bool:
        lower = text.lower()
        return any(kw in lower for kw in FOCUS_KEYWORDS)

    def _parse_rss_filtered(self, xml_text: str) -> list[dict]:
        all_items = self._parse_rss(xml_text)
        relevant = [a for a in all_items if self._is_relevant(a["title"] + " " + a["summary"])]
        return relevant[:self.MAX_ITEMS]

    def _scrape_html_fallback(self) -> list[dict]:
        html = self.fetch(FALLBACK_URL)
        soup = BeautifulSoup(html, "lxml")
        articles = []
        links = []
        for selector in ["h3 a", "h2 a", "a[data-testid='Heading']", "article a"]:
            for a in soup.select(selector):
                href = a.get("href", "")
                title_text = a.get_text(strip=True)
                if href and title_text and self._is_relevant(title_text):
                    if href.startswith("/"):
                        href = BASE_URL + href
                    if href.startswith("http"):
                        links.append((href, title_text))
        seen = set()
        for href, title_text in links:
            if href not in seen:
                seen.add(href)
                articles.append(
                    {
                        "url": href,
                        "title": title_text,
                        "summary": self.truncate(title_text, MAX_ARTICLE_WORDS),
                        "source": self.SOURCE,
                    }
                )
            if len(articles) >= MAX_ITEMS:
                break
        return articles

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return [a for a in MockScraper().scrape() if a["source"] == self.SOURCE]
        try:
            xml_text = self.fetch(self.RSS_URL)
            results = self._parse_rss_filtered(xml_text)
            if results:
                return results
        except Exception:
            pass
        try:
            return self._scrape_html_fallback()
        except Exception:
            return []
