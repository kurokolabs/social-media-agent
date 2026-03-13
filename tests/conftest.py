"""Pytest fixtures for all tests."""
import os
import sqlite3
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def mock_env(monkeypatch, tmp_path):
    """Set all required env vars with USE_MOCK_APIS=true."""
    monkeypatch.setenv("USE_MOCK_APIS", "true")
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("LOG_PATH", str(tmp_path / "logs"))
    monkeypatch.setenv("BUFFER_CHANNEL_ID", "mock_channel_123")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    monkeypatch.setenv("GEMINI_API_KEY", "")
    monkeypatch.setenv("BUFFER_ACCESS_TOKEN", "")
    os.makedirs(str(tmp_path / "logs"), exist_ok=True)
    return tmp_path


@pytest.fixture
def tmp_database(tmp_path, monkeypatch):
    """Create a fresh SQLite database in a temp directory."""
    db_path = str(tmp_path / "test.db")
    monkeypatch.setenv("DATABASE_PATH", db_path)
    from storage.database import initialize
    initialize()
    return db_path


@pytest.fixture
def mock_articles():
    """Return 5 test articles."""
    return [
        {
            "url": f"https://example.com/article-{i}",
            "title": f"KI in der Fertigung: Automatisierung Teil {i}",
            "summary": f"Dieser Artikel beschreibt KI-Agenten und Automatisierung in der Produktion. Mittelstand und Industrie 4.0 sind die Hauptthemen. Artikel Nummer {i}.",
            "source": "TestSource",
            "relevance_score": float(5 + i),
        }
        for i in range(1, 6)
    ]
