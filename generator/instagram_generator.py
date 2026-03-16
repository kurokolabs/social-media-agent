"""Instagram caption + image generator."""
import os
import random

from config import MAX_GENERATION_RETRIES, QUALITY_SCORE_THRESHOLD, INSTAGRAM_IMAGE_RATIO
from security.audit_log import audit_log


class InstagramGenerator:
    """Generates Instagram captions (Claude) and optional images (Gemini)."""

    def _get_claude(self):
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            from generator.mocks.mock_claude import MockClaudeClient
            return MockClaudeClient()
        import anthropic
        return anthropic.Anthropic()

    def _get_gemini(self):
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            from generator.mocks.mock_gemini import MockGeminiClient
            return MockGeminiClient()
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        return genai

    def _should_generate_image(self) -> bool:
        return random.randint(1, 100) <= INSTAGRAM_IMAGE_RATIO

    def _generate_image(self, caption: str) -> str | None:
        """Generate 1080×1080 image for Instagram. Returns path or None."""
        from generator.image_generator import ImageGenerator
        from generator.prompts_extended import INSTAGRAM_IMAGE_PROMPT_TEMPLATE

        topic = caption[:200]
        prompt_request = INSTAGRAM_IMAGE_PROMPT_TEMPLATE.format(topic=topic)

        # Get image prompt via Claude
        claude = self._get_claude()
        prompt_result = claude.generate_post(
            "Du generierst Bildprompts. Antworte NUR mit dem englischen Prompt.",
            prompt_request,
            "image_prompt",
        )
        image_prompt = prompt_result["content"]

        # Generate image
        gen = ImageGenerator()
        return gen.generate(image_prompt)

    def generate(self, article: dict, post_type: str = "ai_moment") -> dict:
        """Generate IG caption and optional image. Returns post dict."""
        from generator.prompts_extended import INSTAGRAM_SYSTEM_PROMPT, INSTAGRAM_POST_TYPE_PROMPTS

        client = self._get_claude()
        type_prompt = INSTAGRAM_POST_TYPE_PROMPTS.get(
            post_type, INSTAGRAM_POST_TYPE_PROMPTS["ai_moment"]
        )
        user_prompt = (
            f"{type_prompt}\n\n"
            f"Basierend auf diesem Artikel:\n"
            f"Titel: {article['title']}\n"
            f"Zusammenfassung: {article['summary']}"
        )

        best = None
        for _ in range(MAX_GENERATION_RETRIES + 1):
            result = client.generate_post(INSTAGRAM_SYSTEM_PROMPT, user_prompt, post_type)
            content = result["content"]

            audit_log.log(
                service="claude",
                endpoint="instagram_generate",
                tokens_in=result.get("tokens_in", 0),
                tokens_out=result.get("tokens_out", 0),
                cost_usd=result.get("cost_usd", 0.0),
                status="success",
            )

            word_count = len(content.split())
            quality_score = 8.0 if 100 <= word_count <= 300 else 6.0

            post = {
                "platform": "instagram",
                "content": content,
                "post_type": post_type,
                "quality_score": quality_score,
                "article_id": article.get("id"),
                "image_path": None,
            }

            if best is None or quality_score > best["quality_score"]:
                best = post

            if quality_score >= QUALITY_SCORE_THRESHOLD:
                break

        # Generate image for a portion of posts
        if best and self._should_generate_image():
            best["image_path"] = self._generate_image(best["content"])

        return best
