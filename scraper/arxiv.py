"""arXiv scraper for manufacturing AI papers — uses arXiv API with ElementTree."""
import os
import re
import xml.etree.ElementTree as ET

from scraper.base_scraper import BaseScraper
from scraper.mocks.mock_scraper import MockScraper
from config import MAX_ARTICLE_WORDS

API_URL = (
    "https://export.arxiv.org/api/query"
    "?search_query=all:manufacturing+AND+(all:AI+OR+all:automation)"
    "&sortBy=submittedDate&sortOrder=descending&max_results=8"
)

ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_NS = "http://arxiv.org/schemas/atom"

_LATEX_PATTERNS = [
    re.compile(r"\$[^$]*\$"),          # inline math $...$
    re.compile(r"\\\w+\{[^}]*\}"),     # \command{arg}
    re.compile(r"\\\w+"),              # \command
    re.compile(r"\{[^}]*\}"),          # bare braces
]


def _strip_latex(text: str) -> str:
    """Remove common LaTeX artifacts from abstract text."""
    for pattern in _LATEX_PATTERNS:
        text = pattern.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


class ArXivScraper(BaseScraper):
    SOURCE = "arXiv"

    def _parse_feed(self, xml_text: str) -> list[dict]:
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return []

        articles = []
        for entry in root.findall(f"{{{ATOM_NS}}}entry"):
            title_el = entry.find(f"{{{ATOM_NS}}}title")
            summary_el = entry.find(f"{{{ATOM_NS}}}summary")
            id_el = entry.find(f"{{{ATOM_NS}}}id")

            title = (title_el.text or "").strip() if title_el is not None else ""
            raw_summary = (summary_el.text or "").strip() if summary_el is not None else ""
            link = (id_el.text or "").strip() if id_el is not None else ""

            # Convert arXiv ID URL to abstract URL if needed
            if link.startswith("http://arxiv.org/abs/") or link.startswith("https://arxiv.org/abs/"):
                pass  # already a valid URL
            elif link:
                link = f"https://arxiv.org/abs/{link}"

            if title and link:
                clean_summary = _strip_latex(raw_summary)
                articles.append(
                    {
                        "url": link,
                        "title": _strip_latex(title),
                        "summary": self.truncate(clean_summary, MAX_ARTICLE_WORDS),
                        "source": self.SOURCE,
                    }
                )
        return articles

    def scrape(self) -> list[dict]:
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return [a for a in MockScraper().scrape() if a["source"] == self.SOURCE]
        try:
            xml_text = self.fetch(API_URL)
            return self._parse_feed(xml_text)
        except Exception:
            return []
