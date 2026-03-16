"""arXiv scraper for LLM, NLP, and AI-agent papers (cs.CL + cs.LG + cs.AI)."""
import os
import re
import xml.etree.ElementTree as ET

from scraper.base_scraper import BaseScraper
from config import MAX_ARTICLE_WORDS

# Focus on LLM, agents, RAG, NLP — broader than the manufacturing-only arxiv.py
API_URL = (
    "https://export.arxiv.org/api/query"
    "?search_query="
    "(cat:cs.CL+OR+cat:cs.LG+OR+cat:cs.AI)"
    "+AND+(all:large+language+model+OR+all:RAG+OR+all:agent+OR+all:fine-tuning)"
    "&sortBy=submittedDate&sortOrder=descending&max_results=12"
)

ATOM_NS = "http://www.w3.org/2005/Atom"

_LATEX_PATTERNS = [
    re.compile(r"\$[^$]*\$"),
    re.compile(r"\\\w+\{[^}]*\}"),
    re.compile(r"\\\w+"),
    re.compile(r"\{[^}]*\}"),
]


def _strip_latex(text: str) -> str:
    for pattern in _LATEX_PATTERNS:
        text = pattern.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


class ArXivLLMScraper(BaseScraper):
    SOURCE = "arXiv-LLM"

    def _parse_feed(self, xml_text: str) -> list[dict]:
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return []

        articles = []
        for entry in root.findall(f"{{{ATOM_NS}}}entry"):
            title_el   = entry.find(f"{{{ATOM_NS}}}title")
            summary_el = entry.find(f"{{{ATOM_NS}}}summary")
            id_el      = entry.find(f"{{{ATOM_NS}}}id")
            # collect author names
            authors = [
                (a.find(f"{{{ATOM_NS}}}name").text or "").strip()
                for a in entry.findall(f"{{{ATOM_NS}}}author")
                if a.find(f"{{{ATOM_NS}}}name") is not None
            ]

            title   = _strip_latex((title_el.text   or "").strip()) if title_el   else ""
            summary = _strip_latex((summary_el.text or "").strip()) if summary_el else ""
            link    = (id_el.text or "").strip()                    if id_el      else ""

            if not link.startswith("http"):
                link = f"https://arxiv.org/abs/{link}"

            if title and link:
                author_str = ", ".join(authors[:3])
                if len(authors) > 3:
                    author_str += " et al."
                articles.append({
                    "url":     link,
                    "title":   title,
                    "summary": self.truncate(summary, MAX_ARTICLE_WORDS),
                    "authors": author_str,
                    "source":  self.SOURCE,
                })
        return articles

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return []
        try:
            xml_text = self.fetch(API_URL)
            return self._parse_feed(xml_text)
        except Exception:
            return []
