"""Tests for intelligence module."""
import pytest


def test_trend_analyzer_scores_manufacturing():
    """Manufacturing articles should score higher than generic ones."""
    from intelligence.trend_analyzer import TrendAnalyzer
    analyzer = TrendAnalyzer()
    articles = [
        {
            "url": "a",
            "title": "KI Fertigung Automatisierung Mittelstand",
            "summary": "Manufacturing IoT Industrie 4.0 Predictive Maintenance factory Produktion",
            "source": "test",
            "relevance_score": 0,
        },
        {
            "url": "b",
            "title": "Fashion trends 2024",
            "summary": "Consumer retail shopping B2C lifestyle brands Mode",
            "source": "test",
            "relevance_score": 0,
        },
    ]
    scored = analyzer.analyze(articles)
    assert scored[0]["relevance_score"] > scored[1]["relevance_score"]


def test_trend_analyzer_top_n():
    """top_trends should return at most n items sorted by score."""
    from intelligence.trend_analyzer import TrendAnalyzer
    analyzer = TrendAnalyzer()
    articles = [{"url": str(i), "title": "t", "summary": "s", "source": "x", "relevance_score": float(i)} for i in range(10)]
    scored = analyzer.analyze(articles)
    top = analyzer.top_trends(scored, n=3)
    assert len(top) == 3
    assert top[0]["relevance_score"] >= top[1]["relevance_score"]


def test_japan_germany_detection():
    """Article with both Japan and Germany keywords should be flagged."""
    from intelligence.japan_germany_detector import JapanGermanyDetector
    detector = JapanGermanyDetector()
    article = {
        "title": "Japan und Deutschland: Kaizen trifft Mittelstand",
        "summary": "Japanische METI-Strategie und deutsche Fraunhofer Forschung in der Fertigung.",
        "relevance_score": 7.0,
    }
    assert detector.detect(article) is True


def test_japan_germany_no_false_positive():
    """Generic article should NOT be flagged as Japan-Germany."""
    from intelligence.japan_germany_detector import JapanGermanyDetector
    detector = JapanGermanyDetector()
    article = {
        "title": "E-Commerce trends 2024",
        "summary": "Online shopping consumer behavior retail market analysis",
        "relevance_score": 2.0,
    }
    assert detector.detect(article) is False


def test_dedup_blocks_repeat(tmp_database, mock_env):
    """Recording a topic should make it appear as duplicate."""
    from intelligence.dedup_checker import DedupChecker
    checker = DedupChecker()
    slug = "ki-in-der-fertigung-2024"
    checker.record_topic(slug)
    assert checker.is_duplicate(slug) is True


def test_dedup_allows_new_topic(tmp_database, mock_env):
    """A never-seen topic should not be a duplicate."""
    from intelligence.dedup_checker import DedupChecker
    checker = DedupChecker()
    assert checker.is_duplicate("brand-new-unique-topic-xyz") is False


def test_slug_generation():
    """generate_slug should produce clean lowercase slug <= 60 chars."""
    from intelligence.dedup_checker import DedupChecker
    checker = DedupChecker()
    slug = checker.generate_slug("KI in der Fertigung: Trends 2024!")
    assert slug == slug.lower()
    assert len(slug) <= 60
    assert " " not in slug
    assert "!" not in slug


def test_dedup_allows_after_expiry(tmp_database, mock_env, monkeypatch):
    """Topic posted > DEDUP_DAYS ago should not be flagged as duplicate."""
    from intelligence.dedup_checker import DedupChecker
    from datetime import datetime, timezone, timedelta
    import sqlite3
    import os

    checker = DedupChecker()
    slug = "old-topic-slug"
    # Insert directly with old date
    old_date = (datetime.now(timezone.utc) - timedelta(days=20)).isoformat()
    db_path = os.getenv("DATABASE_PATH", "./kuroko.db")
    conn = sqlite3.connect(db_path)
    conn.execute("INSERT INTO topic_history (topic_slug, posted_at) VALUES (?, ?)", (slug, old_date))
    conn.commit()
    conn.close()
    assert checker.is_duplicate(slug) is False
