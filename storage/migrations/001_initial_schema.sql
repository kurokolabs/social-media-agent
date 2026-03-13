CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    source TEXT NOT NULL,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    relevance_score REAL DEFAULT 0.0,
    japan_germany_flag BOOLEAN DEFAULT FALSE,
    used_for_post BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    post_type TEXT NOT NULL,
    quality_score REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    article_id INTEGER REFERENCES articles(id),
    image_path TEXT,
    scheduled_at TIMESTAMP,
    published_at TIMESTAMP,
    buffer_post_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS image_counter (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    post_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS topic_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_slug TEXT NOT NULL,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO image_counter (id, post_count) VALUES (1, 0);
