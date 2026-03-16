"""Celery tasks for async content generation."""
from tasks.celery_app import celery_app


@celery_app.task(bind=True, max_retries=2)
def generate_weekly_batch(self) -> dict:
    """Generate a full week of posts for all platforms. Called Sunday 22:00."""
    try:
        from scheduler.weekly_planner import run_weekly
        return run_weekly()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(bind=True, max_retries=2)
def generate_single_post(self, article: dict, platform: str, post_type: str) -> dict:
    """Generate a single post for a given platform and article."""
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
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)
