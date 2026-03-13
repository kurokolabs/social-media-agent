"""Tests for publisher module."""
import os
import pytest
from pathlib import Path


def test_mock_buffer_creates_file(mock_env):
    """MockBufferClient should create a file in output/mock_published/."""
    from publisher.mocks.mock_buffer import MockBufferClient
    client = MockBufferClient()
    result = client.schedule_post("Test post content", "2026-03-15T08:00:00Z")
    assert result["success"] is True
    assert result["post_id"].startswith("mock_")
    # Check file was created
    published_dir = Path("output/mock_published")
    files = list(published_dir.glob("*.md"))
    assert len(files) >= 1


def test_file_output_creates_markdown(mock_env, tmp_path, monkeypatch):
    """FileOutput.save should create a readable .md file with frontmatter."""
    monkeypatch.chdir(tmp_path)
    from publisher.file_output import FileOutput
    fo = FileOutput()
    post = {"content": "Test LinkedIn post content.", "post_type": "trend", "quality_score": 8}
    path = fo.save(post, "test")
    assert Path(path).exists()
    content = Path(path).read_text()
    assert "---" in content
    assert "Test LinkedIn post content." in content


def test_buffer_client_uses_mock(mock_env):
    """BufferClient should use MockBufferClient when USE_MOCK_APIS=true."""
    from publisher.buffer_client import BufferClient
    client = BufferClient()
    result = client.schedule_post("Post content", "2026-03-15T08:00:00Z")
    assert result["success"] is True
