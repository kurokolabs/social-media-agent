-- Breaking news alerts
CREATE TABLE IF NOT EXISTS news_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    summary TEXT,
    alert_type TEXT NOT NULL,  -- 'new_model', 'research_paper', 'product_launch', 'benchmark', 'other'
    priority INTEGER DEFAULT 0, -- 0=normal, 1=high, 2=breaking
    is_read INTEGER DEFAULT 0,
    is_dismissed INTEGER DEFAULT 0,
    notified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_alerts_priority ON news_alerts(priority DESC, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_unread ON news_alerts(is_read, is_dismissed);
