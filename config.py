"""Global configuration constants for kuroko-linkedin-agent."""
import os

MAX_SCRAPE_REQUESTS_PER_DOMAIN = 20
SCRAPE_DELAY_MIN = 2.5
SCRAPE_DELAY_MAX = 5.0
MAX_ARTICLE_WORDS = 500
MAX_TOKENS_CLAUDE = 1500
POST_MIN_WORDS = 150
POST_MAX_WORDS = 300
POST_MAX_HASHTAGS = 4
QUALITY_SCORE_THRESHOLD = 7
MAX_GENERATION_RETRIES = 2
IMAGE_EVERY_N_POSTS = 3
DEDUP_DAYS = 14
POSTING_DAYS = [1, 3]  # Tuesday=1, Thursday=3
POSTING_HOURS = [(8, 10), (12, 13)]

# Platform constraints
TWITTER_MAX_CHARS = 280
INSTAGRAM_IMAGE_SIZE = (1080, 1080)
THREADS_MAX_CHARS = 500
INSTAGRAM_IMAGE_RATIO = 60  # % of IG posts that get AI-generated image

# Platform identifiers
PLATFORM_LINKEDIN = "linkedin"
PLATFORM_TWITTER = "twitter"
PLATFORM_INSTAGRAM = "instagram"
PLATFORM_THREADS = "threads"

ALL_PLATFORMS = [PLATFORM_LINKEDIN, PLATFORM_TWITTER, PLATFORM_INSTAGRAM, PLATFORM_THREADS]

# Instagram DM automation feature flag
IG_DM_AUTOMATION_ENABLED = os.getenv("IG_DM_AUTOMATION_ENABLED", "false").lower() == "true"

# Dashboard
DASHBOARD_PORT       = int(os.getenv("DASHBOARD_PORT", "8080"))
DASHBOARD_SECRET_KEY = os.getenv("DASHBOARD_SECRET_KEY", "change-me-in-production")
DASHBOARD_PASSWORD   = os.getenv("DASHBOARD_PASSWORD", "")   # required in production
HTTPS_ENABLED        = os.getenv("HTTPS_ENABLED", "false").lower() == "true"

# Security constants
MAX_WEBHOOK_BODY_BYTES = 65_536          # 64 KB
MAX_CHAT_MESSAGE_LEN   = 2_000
MAX_POST_CONTENT_LEN   = 5_000
API_RATE_LIMIT_RPM     = 60             # requests per minute per IP (general)
CHAT_RATE_LIMIT_RPM    = 5              # chat endpoint
SCRAPER_RATE_PER_SEC   = 1.0           # max 1 request/sec per domain
SCRAPER_BURST          = 3             # burst size
ALLOWED_PLATFORMS      = frozenset({"linkedin", "twitter", "instagram", "threads"})

# Phase 2 constants
BUFFER_WEBHOOK_SECRET  = os.getenv("BUFFER_WEBHOOK_SECRET", "")
MIN_ANALYTICS_SAMPLES  = 10   # minimum data points before PostingTimeOptimizer uses analytics
