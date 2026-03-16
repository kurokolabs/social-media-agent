"""Celery task: repurpose top LinkedIn posts to X and Threads — Feature 2."""
from tasks.celery_app import celery_app


@celery_app.task(name="tasks.repurpose_tasks.repurpose_top_posts", bind=True, max_retries=2)
def repurpose_top_posts(self) -> dict:
    """Find high-quality LinkedIn posts and repurpose them to X and Threads.

    Runs daily at 06:00. Targets posts with quality_score >= 8.5 that have
    not yet been repurposed (repurposed_from_id IS NULL on originals means they
    are not copies; we track copies via repurposed_from_id).
    """
    from storage.database import get_repurposable_posts, save_repurposed_post
    from generator.repurposing_generator import RepurposingGenerator
    from intelligence.posting_time_optimizer import PostingTimeOptimizer

    generator = RepurposingGenerator()
    optimizer = PostingTimeOptimizer()
    posts = get_repurposable_posts(quality_threshold=8.5, limit=5)

    created = 0
    for post in posts:
        linkedin_content = post["content"]
        post_id = post["id"]

        for target_platform, repurpose_fn in [
            ("twitter", generator.repurpose_to_twitter),
            ("threads", generator.repurpose_to_threads),
        ]:
            try:
                repurposed_content = repurpose_fn(linkedin_content)
                scheduled_at = optimizer.get_optimal_slot(target_platform)
                save_repurposed_post(
                    platform=target_platform,
                    content=repurposed_content,
                    scheduled_at=scheduled_at.isoformat(),
                    repurposed_from_id=post_id,
                    post_type=f"repurposed_{post.get('post_type', 'general')}",
                    quality_score=7.5,  # default — repurposed content gets lower initial score
                )
                created += 1
            except Exception as exc:
                self.retry(exc=exc, countdown=60)

    return {"repurposed": created, "source_posts": len(posts)}
