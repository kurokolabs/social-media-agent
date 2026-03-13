"""Post generator — orchestrates Claude/mock to create LinkedIn posts."""
import os

from generator.quality_checker import QualityChecker
from security.audit_log import audit_log
from config import QUALITY_SCORE_THRESHOLD, MAX_GENERATION_RETRIES


class PostGenerator:
    """Generates LinkedIn posts using Claude or mock."""

    def __init__(self) -> None:
        self.quality_checker = QualityChecker()

    def _get_client(self):
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            from generator.mocks.mock_claude import MockClaudeClient
            return MockClaudeClient()
        import anthropic
        return anthropic.Anthropic()

    def generate(self, article: dict, post_type: str) -> dict:
        """Generate a LinkedIn post from an article. Returns post dict."""
        from generator.prompts import WESSAL_SYSTEM_PROMPT, POST_TYPE_PROMPTS

        client = self._get_client()
        user_prompt = (
            f"{POST_TYPE_PROMPTS.get(post_type, POST_TYPE_PROMPTS['trend'])}\n\n"
            f"Basierend auf diesem Artikel:\n"
            f"Titel: {article['title']}\n"
            f"Zusammenfassung: {article['summary']}"
        )

        for attempt in range(MAX_GENERATION_RETRIES + 1):
            result = client.generate_post(WESSAL_SYSTEM_PROMPT, user_prompt, post_type)
            content = result["content"]
            quality = self.quality_checker.evaluate(content)

            audit_log.log(
                service="claude",
                endpoint="generate_post",
                tokens_in=result.get("tokens_in", 0),
                tokens_out=result.get("tokens_out", 0),
                cost_usd=result.get("cost_usd", 0.0),
                status="success",
            )

            if quality["score"] >= QUALITY_SCORE_THRESHOLD:
                return {
                    "content": content,
                    "post_type": post_type,
                    "quality_score": quality["score"],
                    "article_id": article.get("id"),
                }

        # Below threshold after retries — send to review queue
        self.quality_checker.save_to_review_queue({
            "content": content,
            "post_type": post_type,
            "quality_score": quality["score"],
        })
        return {
            "content": content,
            "post_type": post_type,
            "quality_score": quality["score"],
            "article_id": article.get("id"),
            "needs_review": True,
        }
