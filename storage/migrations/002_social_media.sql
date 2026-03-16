-- Migration 002: Multi-platform social media support

CREATE TABLE IF NOT EXISTS social_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    content TEXT NOT NULL,
    image_path TEXT,
    status TEXT DEFAULT 'pending',
    scheduled_at TIMESTAMP,
    published_at TIMESTAMP,
    buffer_post_id TEXT,
    article_id INTEGER,
    post_type TEXT,
    quality_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles(id)
);

CREATE TABLE IF NOT EXISTS post_edits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES social_posts(id)
);
