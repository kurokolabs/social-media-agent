"""Anthropic research blog scraper — model cards, alignment papers, safety research."""
import os

from scraper.base_scraper import BaseScraper
from scraper.rss_scraper import RssScraper
from config import MAX_ARTICLE_WORDS

RSS_URL  = "https://www.anthropic.com/rss.xml"
HTML_URL = "https://www.anthropic.com/research"


class AnthropicResearchScraper(BaseScraper):
    SOURCE = "Anthropic"

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return []
        try:
            articles = RssScraper(self.SOURCE, RSS_URL, max_items=10).scrape()
            if articles:
                # filter to research posts only
                return [a for a in articles if any(
                    kw in (a.get("title", "") + a.get("summary", "")).lower()
                    for kw in ["model", "research", "safety", "alignment", "claude", "agent"]
                )]
        except Exception:
            pass

        try:
            html = self.fetch(HTML_URL)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "lxml")
            articles = []
            for card in soup.select("a[href*='/research/']")[:10]:
                href  = card.get("href", "")
                url   = href if href.startswith("http") else f"https://www.anthropic.com{href}"
                title = card.get_text(strip=True)
                if len(title) > 10 and url != HTML_URL:
                    articles.append({
                        "url":     url,
                        "title":   title,
                        "summary": "",
                        "source":  self.SOURCE,
                    })
            # deduplicate by url
            seen = set()
            unique = []
            for a in articles:
                if a["url"] not in seen:
                    seen.add(a["url"])
                    unique.append(a)
            return unique
        except Exception:
            return []
