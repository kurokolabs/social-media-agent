"""IW Köln press release scraper — HTML."""
import os

from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper
from scraper.mocks.mock_scraper import MockScraper
from config import MAX_ARTICLE_WORDS

LISTING_URL = "https://www.iwkoeln.de/presse/pressemitteilungen.html"
BASE_URL = "https://www.iwkoeln.de"
MAX_ARTICLES = 6

FOCUS_KEYWORDS = [
    "ki", "ai", "automatisierung", "automation", "manufacturing", "fertigung",
    "industrie 4.0", "industry 4.0", "mittelstand", "iot", "robotik", "digital",
    "predictive", "maschinenbau", "produktion", "wettbewerb", "konjunktur",
    "arbeitsmarkt", "wirtschaft",
]


class IWKoelnScraper(BaseScraper):
    SOURCE = "IW Köln"

    def _is_relevant(self, text: str) -> bool:
        lower = text.lower()
        return any(kw in lower for kw in FOCUS_KEYWORDS)

    def _extract_article_urls(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "lxml")
        links = []
        for selector in [
            ".press-item a",
            "h3 a",
            "h2 a",
            "article a",
            ".press-list a",
            ".news-item a",
        ]:
            for a in soup.select(selector):
                href = a.get("href", "")
                title_text = a.get_text(strip=True)
                if href:
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
