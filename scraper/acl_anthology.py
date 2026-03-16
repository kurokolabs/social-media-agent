"""ACL Anthology scraper — peer-reviewed NLP/CL papers from major conferences."""
import json
import os

from scraper.base_scraper import BaseScraper
from config import MAX_ARTICLE_WORDS

# ACL Anthology Semantic Scholar-style search for recent high-impact NLP papers
# Uses the public anthology search endpoint
SEARCH_URL = (
    "https://aclanthology.org/search/?q=large+language+model+agent&fq=year%3A2025+OR+year%3A2026"
)

# Fallback: recent EMNLP/ACL/NAACL proceedings RSS
RSS_FEEDS = [
    "https://aclanthology.org/anthology+recent.rss",
]


class ACLAnthologyScraper(BaseScraper):
    SOURCE = "ACL Anthology"

    def _parse_html(self, html: str) -> list[dict]:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "lxml")
        articles = []
        for item in soup.select(".card, .paper-card, [class*='paper']")[:15]:
            a_tag = item.find("a", href=True)
            if not a_tag:
                continue
            href  = a_tag["href"]
            url   = href if href.startswith("http") else f"https://aclanthology.org{href}"
            title_el = item.find(["strong", "b", "h5", "h4"])
            title    = title_el.get_text(strip=True) if title_el else a_tag.get_text(strip=True)
            abstract_el = item.find("div", class_=lambda c: c and "abstract" in c.lower())
            summary = abstract_el.get_text(strip=True) if abstract_el else ""
            if title and url and len(title) > 10:
                articles.append({
                    "url":     url,
                    "title":   title,
                    "summary": self.truncate(summary, MAX_ARTICLE_WORDS),
                    "source":  self.SOURCE,
                })
        return articles

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return []
        try:
            html = self.fetch(SEARCH_URL)
            articles = self._parse_html(html)
            if articles:
                return articles
        except Exception:
            pass

        # RSS fallback
        from scraper.rss_scraper import RssScraper
        for rss_url in RSS_FEEDS:
            try:
                articles = RssScraper(self.SOURCE, rss_url, max_items=10).scrape()
                if articles:
                    return articles
            except Exception:
                continue
        return []
