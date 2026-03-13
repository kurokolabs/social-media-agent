"""Image generator — generates images every IMAGE_EVERY_N_POSTS posts."""
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from config import IMAGE_EVERY_N_POSTS
from security.audit_log import audit_log


class ImageGenerator:
    """Generates post images using Gemini or mock, every N posts."""

    def _get_client(self):
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            from generator.mocks.mock_gemini import MockGeminiClient
            return MockGeminiClient()
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        return genai

    def should_generate(self) -> bool:
        """Return True every IMAGE_EVERY_N_POSTS posts based on DB counter."""
        import sqlite3
        db_path = os.getenv("DATABASE_PATH", "./kuroko.db")
        try:
            conn = sqlite3.connect(db_path)
            row = conn.execute("SELECT post_count FROM image_counter WHERE id = 1").fetchone()
            count = row[0] if row else 0
            new_count = count + 1
            conn.execute("UPDATE image_counter SET post_count = ? WHERE id = 1", (new_count,))
            conn.commit()
            conn.close()
            return new_count % IMAGE_EVERY_N_POSTS == 0
        except Exception:
            return False

    def _get_prompt(self, post_content: str) -> str:
        """Generate an image prompt via Claude or mock."""
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            from generator.mocks.mock_claude import MockClaudeClient
            return MockClaudeClient().generate_image_prompt(post_content)
        import anthropic
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            messages=[{"role": "user", "content": f"Generate a Midjourney image prompt for this LinkedIn post. Reply with the prompt only.\n\n{post_content}"}],
        )
        return msg.content[0].text.strip()

    def generate(self, post_content: str) -> Optional[str]:
        """Generate image for post. Returns file path or None on failure."""
        try:
            prompt = self._get_prompt(post_content)

            client = self._get_client()
            result = client.generate_image(prompt)
            image_bytes = result["image_bytes"]

            if len(image_bytes) < 8:
                return None

            os.makedirs("output/images", exist_ok=True)
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            img_path = f"output/images/{timestamp}.png"
            Path(img_path).write_bytes(image_bytes)

            audit_log.log("gemini", "generate_image", 0, 0, 0.0, "success")
            return img_path
        except Exception as e:
            audit_log.log("gemini", "generate_image", 0, 0, 0.0, "error", str(e))
            return None
