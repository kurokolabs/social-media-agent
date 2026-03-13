"""SQLite database initialization and helpers."""
import os
import sqlite3
from pathlib import Path
from typing import Optional


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection with row factory enabled."""
    db_path = os.getenv("DATABASE_PATH", "./kuroko.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def initialize() -> None:
    """Run migrations to create tables if they don't exist."""
    migration_path = Path(__file__).parent / "migrations" / "001_initial_schema.sql"
    sql = migration_path.read_text(encoding="utf-8")
    conn = get_connection()
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()


def save_article(article: dict) -> Optional[int]:
    """Insert article into DB. Returns row id or None on duplicate."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            """INSERT OR IGNORE INTO articles
               (url, title, summary, source, relevance_score, japan_germany_flag)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                article["url"],
                article["title"],
                article["summary"],
                article["source"],
                article.get("relevance_score", 0.0),
                article.get("japan_germany_flag", False),
            ),
        )
        conn.commit()
        return cursor.lastrowid if cursor.lastrowid else None
    finally:
        conn.close()


def save_post(post: dict) -> int:
    """Insert post into DB. Returns row id."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO posts
               (content, post_type, quality_score, status, article_id, image_path, scheduled_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                post["content"],
                post["post_type"],
                post["quality_score"],
                post.get("status", "pending"),
                post.get("article_id"),
                post.get("image_path"),
                post.get("scheduled_at"),
            ),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def count_posts() -> int:
    """Return total number of posts in DB."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT COUNT(*) as cnt FROM posts").fetchone()
        return row["cnt"] if row else 0
    finally:
        conn.close()
