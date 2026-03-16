"""Tests for X/Twitter post generator."""
import os
import pytest

os.environ.setdefault("USE_MOCK_APIS", "true")

from generator.twitter_generator import TwitterGenerator
from config import TWITTER_MAX_CHARS

SAMPLE_ARTICLE = {
    "id": 1,
    "title": "KI-Agenten in der Fertigung: McKinsey-Studie",
    "summary": "Laut McKinsey setzen 34% der Fertigungsbetriebe KI-Agenten für Prozessoptimierung ein.",
    "source": "mckinsey",
}


def test_generate_returns_dict():
    gen = TwitterGenerator()
    result = gen.generate(SAMPLE_ARTICLE, "insight_tweet")
    assert isinstance(result, dict)
    assert "content" in result
    assert "platform" in result
    assert result["platform"] == "twitter"


def test_char_limit_enforced():
    gen = TwitterGenerator()
    result = gen.generate(SAMPLE_ARTICLE, "insight_tweet")
    assert len(result["content"]) <= TWITTER_MAX_CHARS, (
        f"Tweet too long: {len(result['content'])} chars"
    )


def test_all_post_types():
    gen = TwitterGenerator()
    for pt in ["insight_tweet", "case_study_tweet", "model_fact", "rag_tip"]:
        result = gen.generate(SAMPLE_ARTICLE, pt)
        assert result["post_type"] == pt
        assert len(result["content"]) <= TWITTER_MAX_CHARS


def test_truncate():
    gen = TwitterGenerator()
    long_text = "a " * 200
    truncated = gen._truncate(long_text)
    assert len(truncated) <= TWITTER_MAX_CHARS
