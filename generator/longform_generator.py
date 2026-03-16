"""LinkedIn Long-Form Post Generator — Feature 7.

Generates 600–800 word deep-analysis posts using Claude Sonnet.
Post structure:
  Hook (1 sentence)
  \n\n\n\n
  H2 sections with **Bold** subheadings
  Fazit
  Hashtags
"""
import os

from security.audit_log import audit_log


class LongformGenerator:
    """Generates long-form LinkedIn analysis posts (600–800 Wörter)."""

    def _get_client(self):
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            from generator.mocks.mock_claude import MockClaudeClient
            return MockClaudeClient()
        import anthropic
        return anthropic.Anthropic()

    def generate(self, article: dict) -> dict:
        """Generate a long-form LinkedIn post from an article.

        Returns: {platform, content, post_type, quality_score, article_id}
        """
        from generator.prompts_extended import LONGFORM_SYSTEM_PROMPT, LONGFORM_USER_TEMPLATE

        client = self._get_client()
        user_prompt = LONGFORM_USER_TEMPLATE.format(
            title=article.get("title", ""),
            summary=article.get("summary", ""),
        )

        result = client.generate_post(LONGFORM_SYSTEM_PROMPT, user_prompt, "longform_analysis")

        audit_log.log(
            service="claude",
            endpoint="longform_generate",
            tokens_in=result.get("tokens_in", 0),
            tokens_out=result.get("tokens_out", 0),
            cost_usd=result.get("cost_usd", 0.0),
            status="success",
        )

        content = result["content"]
        word_count = len(content.split())
        # Score based on word count target (600–800)
        if 600 <= word_count <= 800:
            quality_score = 9.0
        elif 500 <= word_count <= 900:
            quality_score = 7.5
        else:
            quality_score = 6.0

        return {
            "platform": "linkedin",
            "content": content,
            "post_type": "longform_analysis",
            "quality_score": quality_score,
            "article_id": article.get("id"),
            "word_count": word_count,
        }
