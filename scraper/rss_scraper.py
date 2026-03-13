"""Base class for RSS/Atom feed scrapers."""
import os
import xml.etree.ElementTree as ET

from scraper.base_scraper import BaseScraper


class RSSBaseScraper(BaseScraper):
    """Fetches and parses RSS/Atom feeds."""

    RSS_URL: str = ""
    SOURCE: str = "rss"
    MAX_ITEMS: int = 8

    # Namespaces used in RSS/Atom feeds
    _NS = {
        "atom": "http://www.w3.org/2005/Atom",
        "content": "http://purl.org/rss/1.0/modules/content/",
        "dc": "http://purl.org/dc/elements/1.1/",
    }

    def _parse_rss(self, xml_text: str) -> list[dict]:
        """Parse RSS 2.0 or Atom feed, return list of article dicts."""
        articles = []
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return []

        # RSS 2.0
        items = root.findall(".//item")
        if items:
            for item in items[: self.MAX_ITEMS]:
                title = (item.findtext("title") or "").strip()
                link = (item.findtext("link") or "").strip()
                desc = (
                    item.findtext("description")
                    or item.findtext("content:encoded", namespaces=self._NS)
                    or ""
                ).strip()
                if title and link:
                    summary = self.extract_text(desc) if "<" in desc else desc
                    articles.append(
                        {
                            "url": link,
                            "title": title,
                            "summary": self.truncate(summary, 200) if summary else title,
                            "source": self.SOURCE,
                        }
                    )
            return articles

        # Atom
        ns = self._NS["atom"]
        entries = root.findall(f"{{{ns}}}entry")
        for entry in entries[: self.MAX_ITEMS]:
            title_el = entry.find(f"{{{ns}}}title")
            link_el = entry.find(f"{{{ns}}}link")
            summary_el = entry.find(f"{{{ns}}}summary") or entry.find(
                f"{{{ns}}}content"
            )
            title = (title_el.text or "").strip() if title_el is not None else ""
            link = link_el.get("href", "") if link_el is not None else ""
            summary_text = (
                (summary_el.text or "").strip() if summary_el is not None else ""
            )
            if title and link:
                articles.append(
                    {
                        "url": link,
                        "title": title,
                        "summary": (
                            self.truncate(self.extract_text(summary_text), 200)
                            if summary_text
                            else title
                        ),
                        "source": self.SOURCE,
                    }
                )
        return articles

    def scrape(self) -> list[dict]:
        from scraper.mocks.mock_scraper import MockScraper

        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            return [a for a in MockScraper().scrape() if a["source"] == self.SOURCE]
        try:
            xml_text = self.fetch(self.RSS_URL)
            return self._parse_rss(xml_text)
        except Exception:
            return []
