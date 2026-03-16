-- Migration 004: Analytics, Repurposing, Carousel, Evergreen
-- Run via initialize_analytics() in database.py

-- Engagement metrics for Performance Feedback Loop (Feature 5)
ALTER TABLE social_posts ADD COLUMN likes INTEGER DEFAULT 0;
ALTER TABLE social_posts ADD COLUMN comments INTEGER DEFAULT 0;
ALTER TABLE social_posts ADD COLUMN shares INTEGER DEFAULT 0;
ALTER TABLE social_posts ADD COLUMN reach INTEGER DEFAULT 0;
ALTER TABLE social_posts ADD COLUMN impressions INTEGER DEFAULT 0;

-- Evergreen Rotation (Feature 6)
ALTER TABLE social_posts ADD COLUMN is_evergreen INTEGER DEFAULT 0;

-- Content Repurposing (Feature 2)
ALTER TABLE social_posts ADD COLUMN repurposed_from_id INTEGER REFERENCES social_posts(id);

-- Carousel PDF (Feature 3)
ALTER TABLE social_posts ADD COLUMN carousel_pdf_path TEXT;
