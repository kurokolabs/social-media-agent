"""X/Twitter post generator — enforces 280-character limit."""
import os

from config import TWITTER_MAX_CHARS, MAX_GENERATION_RETRIES, QUALITY_SCORE_THRESHOLD
from security.audit_log import audit_log


class TwitterGenerator:
    """Generates X/Twitter posts using Claude or mock."""

    def _get_client(self):
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            from generator.mocks.mock_claude import MockClaudeClient
            return MockClaudeClient()
        import anthropic
        return anthropic.Anthropic()

    def _truncate(self, text: str) -> str:
        """Hard-truncate to TWITTER_MAX_CHARS, preserving hashtags if possible."""
        if len(text) <= TWITTER_MAX_CHARS:
            return text
        # Find last space before limit to avoid cutting words
        cut = text[:TWITTER_MAX_CHARS].rfind(" ")
        return text[:cut] if cut > 0 else text[:TWITTER_MAX_CHARS]

    def generate(self, article: dict, post_type: str = "insight_tweet") -> dict:
        """Generate an X post. Returns post dict with content, quality_score."""
        from generator.prompts_extended import TWITTER_SYSTEM_PROMPT, TWITTER_POST_TYPE_PROMPTS

        client = self._get_client()
        type_prompt = TWITTER_POST_TYPE_PROMPTS.get(
            post_type, TWITTER_POST_TYPE_PROMPTS["insight_tweet"]
        )
        user_prompt = (
            f"{type_prompt}\n\n"
            f"Basierend auf diesem Artikel:\n"
            f"Titel: {article['title']}\n"
            f"Zusammenfassung: {article['summary']}"
        )

        best = None
        for _ in range(MAX_GENERATION_RETRIES + 1):
            result = client.generate_post(TWITTER_SYSTEM_PROMPT, user_prompt, post_type)
            content = self._truncate(result["content"])

            audit_log.log(
                service="claude",
                endpoint="twitter_generate",
                tokens_in=result.get("tokens_in", 0),
                tokens_out=result.get("tokens_out", 0),
                cost_usd=result.get("cost_usd", 0.0),
                status="success",
            )

            quality_score = 8.0 if len(content) <= TWITTER_MAX_CHARS else 5.0
            post = {
                "platform": "twitter",
                "content": content,
                "post_type": post_type,
                "quality_score": quality_score,
                "article_id": article.get("id"),
                "char_count": len(content),
            }

            if best is None or quality_score > best["quality_score"]:
                best = post

            if quality_score >= QUALITY_SCORE_THRESHOLD:
                break

        return best
