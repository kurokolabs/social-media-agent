"""Weekly batch content planner — runs Sunday 22:00 CET.

Generates posts for all 4 platforms for the upcoming week and stores
them in social_posts with status='pending' for operator approval.
"""
import random
from datetime import datetime, timedelta, timezone


# Posting schedule: {weekday: {platform: (hour_min, hour_max)}}
# weekday: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
WEEKLY_SCHEDULE = {
    0: {"linkedin": (8, 10), "twitter": (8, 10), "instagram": (8, 10), "threads": (8, 10)},
    1: {"twitter": (12, 14), "instagram": (12, 14)},
    2: {"linkedin": (8, 10), "twitter": (8, 10), "instagram": (8, 10), "threads": (8, 10)},
    3: {"twitter": (12, 14), "instagram": (12, 14)},
    4: {"linkedin": (8, 10), "twitter": (8, 10), "instagram": (8, 10), "threads": (8, 10)},
    5: {"twitter": (12, 14), "instagram": (12, 14)},
    6: {"twitter": (10, 12), "instagram": (10, 12)},
}

PLATFORM_POST_TYPES = {
    "linkedin": ["trend", "japan_germany", "manufacturing_iot", "thought_leadership", "behind_scenes", "model_selection", "rag_agent"],
    "twitter": ["insight_tweet", "case_study_tweet", "model_fact", "rag_tip"],
    "instagram": ["ai_moment", "automation_economics", "automation_anxiety", "agent_in_action"],
    "threads": ["threads_question", "threads_insight", "threads_echo"],
}

PLATFORM_SOURCES = {
    "linkedin": ["mckinsey", "bcg", "roland_berger", "deloitte", "fraunhofer", "vdi", "bitkom",
                 "plattform_i40", "iw_koeln", "mit_tech_review", "reuters_tech", "meti"],
    "twitter": ["mckinsey", "bcg", "techcrunch_ai", "venturebeat_ai", "openai_blog"],
    "instagram": ["techcrunch_ai", "venturebeat_ai", "openai_blog"],
    "threads": ["mckinsey", "bcg", "techcrunch_ai", "venturebeat_ai"],
}


def _get_slot_for_day(base_date: datetime, platform: str, hour_range: tuple) -> datetime:
    """Return a datetime in the given hour range with ±15 min jitter."""
    h_min, h_max = hour_range
    hour = random.randint(h_min, h_max - 1)
    minute = random.randint(0, 59)
    # ±15 min jitter
    jitter = random.randint(-15, 15)
    dt = base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
    dt += timedelta(minutes=jitter)
    return dt


def _scrape_articles(source_hint: str) -> list[dict]:
    """Attempt to scrape from the given source, fall back to mock."""
    import os
    if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
        from scraper.mocks.mock_scraper import MockScraper
        return MockScraper().scrape()

    scraper_map = {
        "mckinsey": "scraper.mckinsey.McKinseyScraper",
        "bcg": "scraper.bcg.BCGScraper",
        "roland_berger": "scraper.roland_berger.RolandBergerScraper",
        "deloitte": "scraper.deloitte.DeloitteScraper",
        "fraunhofer": "scraper.fraunhofer.FraunhoferScraper",
        "vdi": "scraper.vdi.VDIScraper",
        "bitkom": "scraper.bitkom.BitkomScraper",
        "plattform_i40": "scraper.plattform_i40.PlattformI40Scraper",
        "iw_koeln": "scraper.iw_koeln.IWKoelnScraper",
        "mit_tech_review": "scraper.mit_tech_review.MITTechReviewScraper",
        "reuters_tech": "scraper.reuters_tech.ReutersTechScraper",
        "meti": "scraper.meti.METIScraper",
        "techcrunch_ai": "scraper.techcrunch_ai.TechCrunchAIScraper",
        "venturebeat_ai": "scraper.venturebeat_ai.VentureBeatAIScraper",
        "openai_blog": "scraper.openai_blog.OpenAIBlogScraper",
    }
    class_path = scraper_map.get(source_hint)
    if not class_path:
        from scraper.mocks.mock_scraper import MockScraper
        return MockScraper().scrape()

    module_path, class_name = class_path.rsplit(".", 1)
    import importlib
    mod = importlib.import_module(module_path)
    scraper = getattr(mod, class_name)()
    try:
        return scraper.scrape()
    except Exception:
        from scraper.mocks.mock_scraper import MockScraper
        return MockScraper().scrape()


def _generate_for_platform(article: dict, platform: str) -> dict | None:
    post_type = random.choice(PLATFORM_POST_TYPES[platform])
    try:
        if platform == "twitter":
            from generator.twitter_generator import TwitterGenerator
            return TwitterGenerator().generate(article, post_type)
        elif platform == "instagram":
            from generator.instagram_generator import InstagramGenerator
            return InstagramGenerator().generate(article, post_type)
        elif platform == "threads":
            from generator.threads_generator import ThreadsGenerator
            return ThreadsGenerator().generate(article, post_type)
        else:
            from generator.post_generator import PostGenerator
            return PostGenerator().generate(article, post_type)
    except Exception:
        return None


def run_weekly() -> dict:
    """Generate the full week of posts, save to social_posts with status=pending."""
    from storage.database import initialize_social, save_social_post

    initialize_social()

    # Next Monday = start of upcoming week
    now = datetime.now(timezone.utc)
    days_until_monday = (7 - now.weekday()) % 7 or 7
    week_start = now + timedelta(days=days_until_monday)
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

    posts_created = 0
    errors = 0

    for day_offset, platform_schedule in WEEKLY_SCHEDULE.items():
        day_date = week_start + timedelta(days=day_offset)

        for platform, hour_range in platform_schedule.items():
            sources = PLATFORM_SOURCES[platform]
            source = random.choice(sources)
            articles = _scrape_articles(source)

            if not articles:
                errors += 1
                continue

            article = random.choice(articles)
            post = _generate_for_platform(article, platform)
            if not post:
                errors += 1
                continue

            scheduled_at = _get_slot_for_day(day_date, platform, hour_range)
            post["scheduled_at"] = scheduled_at.isoformat()
            post["status"] = "pending"
            post.setdefault("platform", platform)  # LinkedIn generator doesn't set this

            article_id = article.get("id")
            if article_id:
                post["article_id"] = article_id

            save_social_post(post)
            posts_created += 1

    return {"posts_created": posts_created, "errors": errors, "week_start": week_start.isoformat()}


# ---------------------------------------------------------------------------
# Phase 2 scheduled routines
# ---------------------------------------------------------------------------

def run_analytics_sync() -> dict:
    """Sync Buffer analytics for all published posts (runs daily 04:00)."""
    from intelligence.performance_tracker import PerformanceTracker
    return PerformanceTracker().sync_analytics()


def run_evergreen_rotation() -> dict:
    """Re-schedule high-engagement X/Threads posts after 60 days (runs every Monday 07:00)."""
    from scheduler.evergreen_rotator import EvergreenRotator
    return EvergreenRotator().rotate()


def run_repurposing() -> dict:
    """Repurpose top LinkedIn posts to X and Threads (runs daily 06:00)."""
    from tasks.repurpose_tasks import repurpose_top_posts
    return repurpose_top_posts()


def run_longform_wednesday() -> dict:
    """Generate one long-form LinkedIn post on Wednesday for the upcoming week."""
    import random
    articles = _scrape_articles(random.choice(PLATFORM_SOURCES["linkedin"]))
    if not articles:
        return {"error": "no_articles"}
    article = random.choice(articles)
    try:
        from generator.longform_generator import LongformGenerator
        from storage.database import initialize_social, save_social_post
        from intelligence.posting_time_optimizer import PostingTimeOptimizer

        initialize_social()
        post = LongformGenerator().generate(article)
        scheduled_at = PostingTimeOptimizer().get_optimal_slot("linkedin")
        post["scheduled_at"] = scheduled_at.isoformat()
        post["status"] = "pending"
        post_id = save_social_post(post)
        return {"post_id": post_id, "word_count": post.get("word_count", 0)}
    except Exception as exc:
        return {"error": str(exc)}
