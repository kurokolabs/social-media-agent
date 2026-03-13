"""Kuroko Labs LinkedIn Content Agent — main entry point."""
import os
import sys

from dotenv import load_dotenv

load_dotenv()

from security.secrets_validator import validate  # noqa: E402

validate()

from storage.database import initialize  # noqa: E402


def run_full_pipeline() -> dict:
    """Run the complete LinkedIn content pipeline."""
    import os
    os.makedirs(os.getenv("LOG_PATH", "./logs"), exist_ok=True)
    os.makedirs("output/review_queue", exist_ok=True)
    os.makedirs("output/mock_published", exist_ok=True)

    initialize()

    # Scrape
    if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
        from scraper.mocks.mock_scraper import MockScraper
        articles = MockScraper().scrape()
    else:
        sources = [
            __import__("scraper.mckinsey", fromlist=["McKinseyScraper"]).McKinseyScraper(),
            __import__("scraper.bcg", fromlist=["BCGScraper"]).BCGScraper(),
            __import__("scraper.fraunhofer", fromlist=["FraunhoferScraper"]).FraunhoferScraper(),
        ]
        articles = []
        for s in sources:
            articles.extend(s.scrape())

    # Analyze
    from intelligence.trend_analyzer import TrendAnalyzer
    from intelligence.japan_germany_detector import JapanGermanyDetector
    from intelligence.dedup_checker import DedupChecker

    analyzer = TrendAnalyzer()
    detector = JapanGermanyDetector()
    dedup = DedupChecker()

    articles = analyzer.analyze(articles)
    for a in articles:
        a["japan_germany_flag"] = detector.detect(a)

    top_articles = analyzer.top_trends(articles, n=3)

    # Generate + publish
    from generator.post_generator import PostGenerator
    from generator.image_generator import ImageGenerator
    from publisher.buffer_client import BufferClient
    from publisher import get_next_slot
    from storage.database import save_article, save_post

    generator = PostGenerator()
    image_gen = ImageGenerator()
    buffer = BufferClient()
    dedup = DedupChecker()

    posts_scheduled = 0
    posts_in_review = 0
    articles_scraped = len(articles)

    for article in top_articles:
        slug = dedup.generate_slug(article["title"])
        if dedup.is_duplicate(slug):
            continue

        post_type = "japan_germany" if article.get("japan_germany_flag") else "trend"
        post = generator.generate(article, post_type)

        if post["quality_score"] < 7:
            posts_in_review += 1
            continue

        image_path = None
        if image_gen.should_generate():
            image_path = image_gen.generate(post["content"])
        post["image_path"] = image_path

        article_id = save_article(article)
        post["article_id"] = article_id
        post["scheduled_at"] = str(get_next_slot())
        post["status"] = "scheduled"
        save_post(post)

        buffer.schedule_post(post["content"], post["scheduled_at"], image_path)
        dedup.record_topic(slug)
        posts_scheduled += 1

    from security.audit_log import audit_log
    audit_log.log(
        service="pipeline",
        endpoint="run_full_pipeline",
        tokens_in=0,
        tokens_out=0,
        cost_usd=0.0,
        status="success",
    )

    summary = {
        "articles_scraped": articles_scraped,
        "posts_scheduled": posts_scheduled,
        "posts_in_review": posts_in_review,
    }
    print(f"Pipeline complete: {summary}")
    return summary


if __name__ == "__main__":
    run_full_pipeline()
