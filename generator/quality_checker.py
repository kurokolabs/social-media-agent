"""Quality checker — evaluates posts using Claude or mock."""
import os
import re
from datetime import datetime, timezone
from pathlib import Path


class QualityChecker:
    """Evaluates LinkedIn post quality using LLM rubric."""

    FORBIDDEN_PHRASES = [
        "freue mich bekannt zu geben",
        "ich freue mich",
        "spannend",
        "game-changer",
        "revolutioniert",
        "bahnbrechend",
        "cutting-edge",
    ]

    def _get_client(self):
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            from generator.mocks.mock_claude import MockClaudeClient
            return MockClaudeClient()
        import anthropic
        return anthropic.Anthropic()

    def evaluate(self, post_content: str) -> dict:
        """Return score dict with score/reason/passed."""
        client = self._get_client()
        result = client.evaluate_post(post_content)
        score = result.get("score", 5)
        return {
            "score": score,
            "reason": result.get("reason", ""),
            "passed": score >= 7,
        }

    def save_to_review_queue(self, post: dict) -> str:
        """Save post needing human review to output/review_queue/."""
        os.makedirs("output/review_queue", exist_ok=True)
        now = datetime.now(timezone.utc)
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        content = post.get("content", "")
        slug = re.sub(r"[^a-z0-9]+", "-", content[:30].lower()).strip("-")
        filename = f"output/review_queue/{timestamp}_{slug}.md"
        body = f"""---
quality_score: {post.get("quality_score", 0)}
post_type: {post.get("post_type", "")}
created_at: {now.isoformat()}
status: needs_review
---

{content}
"""
        Path(filename).write_text(body, encoding="utf-8")
        return filename
