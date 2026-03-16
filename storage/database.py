"""SQLite database initialization and helpers."""
import os
import sqlite3
from pathlib import Path
from typing import Optional

from config import ALLOWED_PLATFORMS, MAX_POST_CONTENT_LEN


def _validate_platform(platform: str) -> str:
    """Raise ValueError if platform is not a known social platform. Return platform."""
    if platform not in ALLOWED_PLATFORMS:
        raise ValueError(
            f"Unknown platform {platform!r}. "
            f"Allowed values: {sorted(ALLOWED_PLATFORMS)}"
        )
    return platform


def _validate_content_length(content: str) -> str:
    """Raise ValueError if content exceeds the maximum allowed length. Return content."""
    if len(content) > MAX_POST_CONTENT_LEN:
        raise ValueError(
            f"Content too long: {len(content)} characters "
            f"(maximum is {MAX_POST_CONTENT_LEN})."
        )
    return content


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


def initialize_social() -> None:
    """Run migration 002 to create social_posts and post_edits tables."""
    migration_path = Path(__file__).parent / "migrations" / "002_social_media.sql"
    sql = migration_path.read_text(encoding="utf-8")
    conn = get_connection()
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()


def save_social_post(post: dict) -> int:
    """Insert a social post. Returns row id."""
    platform = _validate_platform(post["platform"])
    content = _validate_content_length(post["content"])
    conn = get_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO social_posts
               (platform, content, image_path, status, scheduled_at, article_id, post_type, quality_score)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                platform,
                content,
                post.get("image_path"),
                post.get("status", "pending"),
                post.get("scheduled_at"),
                post.get("article_id"),
                post.get("post_type"),
                post.get("quality_score"),
            ),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_social_post(post_id: int) -> Optional[dict]:
    """Fetch a single social post by id."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM social_posts WHERE id = ?", (post_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_social_post(post_id: int, fields: dict) -> None:
    """Update arbitrary fields on a social post."""
    if not fields:
        return
    conn = get_connection()
    try:
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [post_id]
        conn.execute(f"UPDATE social_posts SET {set_clause} WHERE id = ?", values)
        conn.commit()
    finally:
        conn.close()


def get_posts_for_month(year: int, month: int, platform: Optional[str] = None) -> list:
    """Return all social posts scheduled in a given month, optionally filtered by platform."""
    if platform is not None:
        platform = _validate_platform(platform)
    conn = get_connection()
    try:
        if platform is not None:
            rows = conn.execute(
                """SELECT * FROM social_posts
                   WHERE strftime('%Y', scheduled_at) = ?
                   AND strftime('%m', scheduled_at) = ?
                   AND platform = ?
                   ORDER BY scheduled_at""",
                (str(year), f"{month:02d}", platform),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM social_posts
                   WHERE strftime('%Y', scheduled_at) = ?
                   AND strftime('%m', scheduled_at) = ?
                   ORDER BY scheduled_at""",
                (str(year), f"{month:02d}"),
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def save_post_edit(post_id: int, role: str, message: str) -> int:
    """Save a chat edit message for a post. Returns row id."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO post_edits (post_id, role, message) VALUES (?, ?, ?)",
            (post_id, role, message),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_post_edits(post_id: int) -> list:
    """Return all chat edits for a post, ordered by creation."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM post_edits WHERE post_id = ? ORDER BY created_at",
            (post_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Alerts (migration 003)
# ---------------------------------------------------------------------------

def initialize_alerts() -> None:
    """Run migration 003 if not already applied."""
    migration_path = Path(__file__).parent / "migrations" / "003_alerts.sql"
    sql = migration_path.read_text(encoding="utf-8")
    conn = get_connection()
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()


def save_alert(
    source: str,
    title: str,
    url: str,
    summary: str,
    alert_type: str,
    priority: int = 0,
) -> Optional[int]:
    """Insert alert, ignore if URL already exists. Return new id or None."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            """INSERT OR IGNORE INTO news_alerts
               (source, title, url, summary, alert_type, priority)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (source, title, url, summary, alert_type, priority),
        )
        conn.commit()
        return cursor.lastrowid if cursor.lastrowid else None
    finally:
        conn.close()


def get_unread_alerts(limit: int = 50) -> list[dict]:
    """Return unread, non-dismissed alerts ordered by priority desc, created_at desc."""
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT * FROM news_alerts
               WHERE is_read = 0 AND is_dismissed = 0
               ORDER BY priority DESC, created_at DESC
               LIMIT ?""",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def mark_alert_read(alert_id: int) -> None:
    """Mark a single alert as read."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE news_alerts SET is_read = 1 WHERE id = ?",
            (alert_id,),
        )
        conn.commit()
    finally:
        conn.close()


def mark_alert_dismissed(alert_id: int) -> None:
    """Mark a single alert as dismissed."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE news_alerts SET is_dismissed = 1 WHERE id = ?",
            (alert_id,),
        )
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Analytics & Phase 2 (migration 004)
# ---------------------------------------------------------------------------

def initialize_analytics() -> None:
    """Run migration 004 (ALTER TABLE statements) if not already applied."""
    migration_path = Path(__file__).parent / "migrations" / "004_analytics.sql"
    raw = migration_path.read_text(encoding="utf-8")

    # Strip comment lines then split on semicolons to get individual ALTER TABLE stmts
    clean_lines = [
        line for line in raw.splitlines()
        if line.strip() and not line.strip().startswith("--")
    ]
    clean_sql = " ".join(clean_lines)

    conn = get_connection()
    try:
        for statement in clean_sql.split(";"):
            stmt = statement.strip()
            if not stmt:
                continue
            try:
                conn.execute(stmt)
            except Exception:
                pass  # column already exists — safe to ignore
        conn.commit()
    finally:
        conn.close()


def update_post_status(buffer_post_id: str, new_status: str, published_at=None) -> None:
    """Update social_posts.status (and optionally published_at) by buffer_post_id."""
    conn = get_connection()
    try:
        if published_at:
            conn.execute(
                "UPDATE social_posts SET status = ?, published_at = ? WHERE buffer_post_id = ?",
                (new_status, published_at, buffer_post_id),
            )
        else:
            conn.execute(
                "UPDATE social_posts SET status = ? WHERE buffer_post_id = ?",
                (new_status, buffer_post_id),
            )
        conn.commit()
    finally:
        conn.close()


def get_repurposable_posts(quality_threshold: float = 8.5, limit: int = 5) -> list[dict]:
    """Return LinkedIn posts that have not yet been repurposed and meet quality threshold."""
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT * FROM social_posts
               WHERE platform = 'linkedin'
               AND quality_score >= ?
               AND repurposed_from_id IS NULL
               AND id NOT IN (
                   SELECT DISTINCT repurposed_from_id
                   FROM social_posts
                   WHERE repurposed_from_id IS NOT NULL
               )
               ORDER BY quality_score DESC, created_at DESC
               LIMIT ?""",
            (quality_threshold, limit),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def save_repurposed_post(
    platform: str,
    content: str,
    scheduled_at: str,
    repurposed_from_id: int,
    post_type: str = "repurposed",
    quality_score: float = 7.5,
) -> int:
    """Insert a repurposed post. Returns new row id."""
    platform = _validate_platform(platform)
    content = _validate_content_length(content)
    conn = get_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO social_posts
               (platform, content, status, scheduled_at, post_type, quality_score, repurposed_from_id)
               VALUES (?, ?, 'pending', ?, ?, ?, ?)""",
            (platform, content, scheduled_at, post_type, quality_score, repurposed_from_id),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def save_carousel_path(post_id: int, pdf_path: str) -> None:
    """Store the carousel PDF path for a post."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE social_posts SET carousel_pdf_path = ? WHERE id = ?",
            (pdf_path, post_id),
        )
        conn.commit()
    finally:
        conn.close()


def get_alert_count() -> dict:
    """Return {'total': n, 'unread': n, 'breaking': n}."""
    conn = get_connection()
    try:
        total = conn.execute(
            "SELECT COUNT(*) as cnt FROM news_alerts WHERE is_dismissed = 0"
        ).fetchone()["cnt"]
        unread = conn.execute(
            "SELECT COUNT(*) as cnt FROM news_alerts WHERE is_read = 0 AND is_dismissed = 0"
        ).fetchone()["cnt"]
        breaking = conn.execute(
            "SELECT COUNT(*) as cnt FROM news_alerts WHERE priority = 2 AND is_read = 0 AND is_dismissed = 0"
        ).fetchone()["cnt"]
        return {"total": total, "unread": unread, "breaking": breaking}
    finally:
        conn.close()
