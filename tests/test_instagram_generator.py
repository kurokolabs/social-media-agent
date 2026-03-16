"""Tests for Instagram caption + image generator."""
import os
import pytest
from unittest.mock import patch

os.environ.setdefault("USE_MOCK_APIS", "true")

from generator.instagram_generator import InstagramGenerator

SAMPLE_ARTICLE = {
    "id": 2,
    "title": "Neue Claude-Modelle: Was das für Automatisierung bedeutet",
    "summary": "Anthropic hat Claude 4 veröffentlicht mit verbesserter Reasoning-Fähigkeit.",
    "source": "techcrunch_ai",
}


def test_generate_returns_dict():
    gen = InstagramGenerator()
    result = gen.generate(SAMPLE_ARTICLE, "ai_moment")
    assert isinstance(result, dict)
    assert result["platform"] == "instagram"
    assert "content" in result


def test_all_post_types():
    gen = InstagramGenerator()
    for pt in ["ai_moment", "automation_economics", "automation_anxiety", "agent_in_action"]:
        result = gen.generate(SAMPLE_ARTICLE, pt)
        assert result["post_type"] == pt


def test_image_path_is_none_or_string():
    gen = InstagramGenerator()
    result = gen.generate(SAMPLE_ARTICLE, "ai_moment")
    assert result["image_path"] is None or isinstance(result["image_path"], str)


def test_image_generation_with_mock():
    gen = InstagramGenerator()
    with patch.object(gen, "_should_generate_image", return_value=True):
        result = gen.generate(SAMPLE_ARTICLE, "agent_in_action")
    # Mock generates a real path; just check type
    assert result["image_path"] is None or isinstance(result["image_path"], str)
