"""Semantic Scholar scraper — citation-weighted AI/ML papers via public API."""
import json
import os

from scraper.base_scraper import BaseScraper
from config import MAX_ARTICLE_WORDS

# Semantic Scholar public API — no key required for reasonable rates
# Fetches highly-cited recent papers in AI/ML/NLP
SEARCH_QUERIES = [
    "large language model agents",
    "retrieval augmented generation",
    "LLM fine-tuning efficiency",
]

API_BASE = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS   = "paperId,title,abstract,year,authors,citationCount,externalIds"


class SemanticScholarScraper(BaseScraper):
    SOURCE = "Semantic Scholar"

    def _fetch_query(self, query: str) -> list[dict]:
        import urllib.parse
        params = urllib.parse.urlencode({
            "query":  query,
            "limit":  6,
            "fields": FIELDS,
            "sort":   "citationCount",
        })
        url = f"{API_BASE}?{params}"
        raw = self.fetch(url)
        data = json.loads(raw)
        articles = []
        for paper in data.get("data", []):
            title    = (paper.get("title") or "").strip()
            abstract = (paper.get("abstract") or "").strip()
            authors  = [a.get("name", "") for a in (paper.get("authors") or [])[:3]]
            ext_ids  = paper.get("externalIds") or {}
            arxiv_id = ext_ids.get("ArXiv", "")
            paper_id = paper.get("paperId", "")
            url = (
                f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id
                else f"https://www.semanticscholar.org/paper/{paper_id}"
            )
            citations = paper.get("citationCount", 0)
            if title and url:
                author_str = ", ".join(authors)
                if len(paper.get("authors") or []) > 3:
                    author_str += " et al."
                articles.append({
                    "url":       url,
                    "title":     title,
                    "summary":   self.truncate(abstract, MAX_ARTICLE_WORDS),
                    "authors":   author_str,
                    "citations": citations,
                    "source":    self.SOURCE,
                })
        return articles

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return []
        all_articles = []
        seen_urls = set()
        for query in SEARCH_QUERIES:
            try:
                for article in self._fetch_query(query):
                    if article["url"] not in seen_urls:
                        seen_urls.add(article["url"])
                        all_articles.append(article)
            except Exception:
                continue
        # sort by citation count descending
        return sorted(all_articles, key=lambda a: a.get("citations", 0), reverse=True)
