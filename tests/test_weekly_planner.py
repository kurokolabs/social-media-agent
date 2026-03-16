"""Tests for the weekly batch planner."""
import os
import sqlite3
import tempfile
import pytest

os.environ.setdefault("USE_MOCK_APIS", "true")


@pytest.fixture
def tmp_db(monkeypatch, tmp_path):
    db = str(tmp_path / "test.db")
    monkeypatch.setenv("DATABASE_PATH", db)
    from storage.database import initialize, initialize_social
    initialize()
    initialize_social()
    return db


def test_run_weekly_creates_posts(tmp_db):
    from scheduler.weekly_planner import run_weekly

    result = run_weekly()
    assert isinstance(result, dict)
    assert "posts_created" in result
    assert result["posts_created"] > 0


def test_run_weekly_covers_all_platforms(tmp_db):
    from scheduler.weekly_planner import run_weekly
    from storage.database import get_connection

    run_weekly()

    conn = get_connection()
    rows = conn.execute("SELECT DISTINCT platform FROM social_posts").fetchall()
    conn.close()

    platforms_found = {r["platform"] for r in rows}
    # At least LinkedIn, Twitter, Instagram should be present
    assert "linkedin" in platforms_found
    assert "twitter" in platforms_found
    assert "instagram" in platforms_found


def test_run_weekly_posts_have_scheduled_at(tmp_db):
    from scheduler.weekly_planner import run_weekly
    from storage.database import get_connection

    run_weekly()
    conn = get_connection()
    rows = conn.execute("SELECT scheduled_at FROM social_posts").fetchall()
    conn.close()

    for row in rows:
        assert row["scheduled_at"] is not None


def test_run_weekly_returns_week_start(tmp_db):
    from scheduler.weekly_planner import run_weekly
    result = run_weekly()
    assert "week_start" in result
    assert result["week_start"]  # non-empty
