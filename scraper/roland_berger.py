"""Roland Berger Insights scraper — consulting firm HTML scraper."""
import os

from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper
from scraper.mocks.mock_scraper import MockScraper
from config import MAX_ARTICLE_WORDS

FOCUS_KEYWORDS = [
    "manufacturing", "ai", "ki", "automation", "automatisierung", "industry",
    "industrie", "digital", "mittelstand", "robot", "iot", "produktion",
    "operational", "maschinenbau", "transformation",
]

LISTING_URL = "https://www.rolandberger.com/en/Insights/"
BASE_URL = "https://www.rolandberger.com"
MAX_ARTICLES = 6


class RolandBergerScraper(BaseScraper):
    SOURCE = "Roland Berger"

    def _is_relevant(self, text: str) -> bool:
        lower = text.lower()
        return any(kw in lower for kw in FOCUS_KEYWORDS)

    def _extract_article_urls(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "lxml")
        links = []
        for selector in [
            ".rb-insights-item a",
            ".insight-card a",
            "article a",
            "h3 a",
            "h2 a",
            ".teaser-headline a",
            ".card a",
        ]:
            for a in soup.select(selector):
                href = a.get("href", "")
                title_text = a.get_text(strip=True)
                if href and self._is_relevant(title_text):
                    if href.startswith("/"):
                        href = BASE_URL + href
                    if href.startswith("http"):
                        links.append(href)
        return list(dict.fromkeys(links))[:MAX_ARTICLES]

    def _fetch_article(self, url: str) -> dict:
        html = self.fetch(url)
        soup = BeautifulSoup(html, "lxml")
        title = ""
        for sel in ["h1", "meta[property='og:title']", "title"]:
            el = soup.select_one(sel)
            if el:
                title = el.get("content", "") or el.get_text(strip=True)
                if title:
                    break
        summary = ""
        meta = soup.select_one("meta[name='description']") or soup.select_one(
            "meta[property='og:description']"
        )
        if meta:
            summary = meta.get("content", "")
        if not summary:
            for p in soup.select("article p, .content p, main p"):
                text = p.get_text(strip=True)
                if len(text.split()) > 20:
                    summary = text
                    break
        return {
            "url": url,
            "title": title or url,
            "summary": self.truncate(summary, MAX_ARTICLE_WORDS),
            "source": self.SOURCE,
        }

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return [a for a in MockScraper().scrape() if a["source"] == self.SOURCE]
        try:
            html = self.fetch(LISTING_URL)
            urls = self._extract_article_urls(html)
            articles = []
            for url in urls:
                try:
                    articles.append(self._fetch_article(url))
                except Exception:
                    continue
            return articles
        except Exception:
            return []
