"""Tests for intelligence module."""
import pytest


def test_trend_analyzer_scores_manufacturing():
    """Manufacturing articles should score higher than generic ones."""
    from intelligence.trend_analyzer import TrendAnalyzer
    analyzer = TrendAnalyzer()
    articles = [
        {"url": "a", "title": "KI Fertigung Automatisierung Mittelstand Produktionsanlage", "summary": "Manufacturing IoT Industrie 4.0 Predictive Maintenance factory", "source": "test", "relevance_score": 0},
        {"url": "b", "title": "Fashion trends 2024", "summary": "Consumer retail shopping B2C lifestyle brands", "source": "test", "relevance_score": 0},
    ]
    scored = analyzer.analyze(articles)
    assert scored[0]["relevance_score"] >= scored[1]["relevance_score"]


def test_japan_germany_detection():
    """Article with both Japan and Germany manufacturing keywords should be flagged."""
    from intelligence.japan_germany_detector import JapanGermanyDetector
    detector = JapanGermanyDetector()
    article = {
        "title": "Japan und Deutschland: Kaizen trifft Mittelstand",
        "summary": "Japanische METI-Strategie und deutsche Fraunhofer Forschung in der Fertigung.",
        "relevance_score": 7.0,
    }
    assert detector.detect(article) is True


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
    """generate_slug should produce clean lowercase slug."""
    from intelligence.dedup_checker import DedupChecker
    checker = DedupChecker()
    slug = checker.generate_slug("KI in der Fertigung: Trends 2024!")
    assert slug == slug.lower()
    assert len(slug) <= 60
    assert " " not in slug
