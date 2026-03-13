"""Bitkom press release scraper — RSS with HTML fallback."""
import os

from bs4 import BeautifulSoup

from scraper.rss_scraper import RSSBaseScraper
from scraper.mocks.mock_scraper import MockScraper
from config import MAX_ARTICLE_WORDS

RSS_URL = "https://www.bitkom.org/rss.xml"
FALLBACK_URL = "https://www.bitkom.org/Presse/Presseinformation.html"
BASE_URL = "https://www.bitkom.org"
MAX_ITEMS = 8

FOCUS_KEYWORDS = [
    "ki", "ai", "automatisierung", "automation", "manufacturing", "fertigung",
    "industrie 4.0", "industry 4.0", "mittelstand", "iot", "robotik", "digital",
    "predictive", "maschinenbau", "produktion", "it-branche", "digitalisierung",
]


class BitkomScraper(RSSBaseScraper):
    SOURCE = "Bitkom"
    RSS_URL = RSS_URL
    MAX_ITEMS = MAX_ITEMS

    def _is_relevant(self, text: str) -> bool:
        lower = text.lower()
        return any(kw in lower for kw in FOCUS_KEYWORDS)

    def _scrape_html_fallback(self) -> list[dict]:
        html = self.fetch(FALLBACK_URL)
        soup = BeautifulSoup(html, "lxml")
        articles = []
        links = []
        for selector in [".press-list__item a", "h3 a", "h2 a", "article a"]:
            for a in soup.select(selector):
                href = a.get("href", "")
                title_text = a.get_text(strip=True)
                if href and title_text:
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
            results = self._parse_rss(xml_text)
            if results:
                return results
        except Exception:
            pass
        try:
            return self._scrape_html_fallback()
        except Exception:
            return []
