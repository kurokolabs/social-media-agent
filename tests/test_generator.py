"""Tests for generator module."""
import pytest


def test_mock_claude_all_post_types(mock_env):
    """MockClaudeClient should generate a post for each of 5 post types."""
    from generator.mocks.mock_claude import MockClaudeClient
    client = MockClaudeClient()
    post_types = ["trend", "japan_germany", "manufacturing_iot", "thought_leadership", "behind_scenes"]
    for pt in post_types:
        result = client.generate_post("system", "user", pt)
        assert "content" in result
        words = len(result["content"].split())
        assert words >= 100, f"Post too short for type {pt}: {words} words"


def test_quality_checker_passes_good_post(mock_env):
    """A realistic post should pass quality check."""
    from generator.quality_checker import QualityChecker
    checker = QualityChecker()
    good_post = """Letzte Woche war ich bei einem Maschinenbauer in Bayern.
    250 Mitarbeiter, Familienunternehmen, hervorragende Qualität.
    Sie hatten 47 Maschinen mit Sensoren aber keine Auswertung.
    In vier Stunden hatten wir einen KI-Agenten laufen.
    Ergebnis: 34% weniger ungeplante Stillstände nach drei Monaten.
    Das ist kein Zufall. Das ist Datenstrategie.
    #KIAgenten #Fertigung #Mittelstand #PredictiveMaintenance"""
    result = checker.evaluate(good_post)
    assert result["score"] >= 6


def test_mock_gemini_returns_valid_png(mock_env):
    """MockGeminiClient should return valid PNG bytes."""
    from generator.mocks.mock_gemini import MockGeminiClient, MINIMAL_PNG_BYTES
    client = MockGeminiClient()
    result = client.generate_image("test prompt")
    assert "image_bytes" in result
    assert result["image_bytes"][:8] == MINIMAL_PNG_BYTES[:8]  # PNG signature
    assert len(result["image_bytes"]) > 10


def test_post_generator_generates_post(mock_env, tmp_database, mock_articles):
    """PostGenerator should produce a post with required fields."""
    from generator.post_generator import PostGenerator
    gen = PostGenerator()
    post = gen.generate(mock_articles[0], "trend")
    assert "content" in post
    assert "quality_score" in post
    assert "post_type" in post
