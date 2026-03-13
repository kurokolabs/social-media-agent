"""Tests for scraper module."""
import os
import pytest


def test_mock_scraper_returns_articles():
    """MockScraper must return >= 8 items with required fields."""
    from scraper.mocks.mock_scraper import MockScraper
    articles = MockScraper().scrape()
    assert len(articles) >= 8
    for a in articles:
        assert "url" in a
        assert "title" in a
        assert "summary" in a
        assert "source" in a


def test_mock_scraper_summary_length():
    """Each mock article summary should be at least 50 words."""
    from scraper.mocks.mock_scraper import MockScraper
    articles = MockScraper().scrape()
    for a in articles:
        word_count = len(a["summary"].split())
        assert word_count >= 50, f"Summary too short: {a['title']} ({word_count} words)"


def test_html_stripping():
    """extract_text should strip HTML tags."""
    from scraper.base_scraper import BaseScraper

    class TestScraper(BaseScraper):
        def scrape(self):
            return []

    scraper = TestScraper()
    html = "<h1>Title</h1><p>Content with <b>bold</b> text.</p><script>evil()</script>"
    text = scraper.extract_text(html)
    assert "<" not in text
    assert "Title" in text
    assert "bold" in text


def test_base_scraper_truncate():
    """truncate should limit to max_words."""
    from scraper.base_scraper import BaseScraper

    class TestScraper(BaseScraper):
        def scrape(self):
            return []

    scraper = TestScraper()
    text = " ".join(["word"] * 600)
    result = scraper.truncate(text, 100)
    assert len(result.split()) == 100
