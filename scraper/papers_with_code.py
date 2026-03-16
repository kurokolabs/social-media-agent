"""Papers with Code scraper — trending ML papers with open implementations."""
import json
import os

from scraper.base_scraper import BaseScraper
from config import MAX_ARTICLE_WORDS

# Public REST API, no auth required
API_URL = "https://paperswithcode.com/api/v1/papers/?ordering=-stars&page=1&items_per_page=15"


class PapersWithCodeScraper(BaseScraper):
    SOURCE = "PapersWithCode"

    def _parse_response(self, raw: str) -> list[dict]:
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return []

        articles = []
        for item in data.get("results", []):
            title   = (item.get("title") or "").strip()
            url     = (item.get("url_pdf") or item.get("url_abs") or "").strip()
            summary = (item.get("abstract") or "").strip()
            authors = item.get("authors") or []

            if not url:
                arxiv_id = item.get("arxiv_id", "")
                if arxiv_id:
                    url = f"https://arxiv.org/abs/{arxiv_id}"

            if not (title and url):
                continue

            author_str = ", ".join(authors[:3])
            if len(authors) > 3:
                author_str += " et al."

            articles.append({
                "url":     url,
                "title":   title,
                "summary": self.truncate(summary, MAX_ARTICLE_WORDS),
                "authors": author_str,
                "stars":   item.get("github_link_count", 0),
                "source":  self.SOURCE,
            })
        return articles

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return []
        try:
            raw = self.fetch(API_URL)
            return self._parse_response(raw)
        except Exception:
            return []
