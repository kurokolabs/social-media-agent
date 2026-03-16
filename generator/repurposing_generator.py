"""Content Repurposing Generator — Feature 2.

Rewrites top-performing LinkedIn posts as X tweets and Threads posts
using Claude Haiku for cost efficiency.
"""
import os

from config import TWITTER_MAX_CHARS, THREADS_MAX_CHARS
from security.audit_log import audit_log


_REPURPOSE_TWITTER_PROMPT = """Du bist der Kuroko Labs Social Media Agent für X/Twitter.
Schreibe einen Tweet (maximal {max_chars} Zeichen) der die Kernaussage dieses LinkedIn-Posts transportiert.
Eine Kernaussage, kein Sales-Pitch, 1–2 Hashtags am Ende.
Antworte NUR mit dem Tweet-Text."""

_REPURPOSE_THREADS_PROMPT = """Du bist der Kuroko Labs Social Media Agent für Threads.
Schreibe einen Threads-Post (maximal {max_chars} Zeichen) der die Kernaussage dieses LinkedIn-Posts
zugänglicher und gesprächiger formuliert. Community-Ton, kein Verkaufspitch.
Antworte NUR mit dem Threads-Post-Text."""


class RepurposingGenerator:
    """Rewrites LinkedIn posts for X and Threads."""

    def _get_client(self):
        if os.getenv("USE_MOCK_APIS", "true").lower() == "true":
            from generator.mocks.mock_claude import MockClaudeClient
            return MockClaudeClient()
        import anthropic
        # Use Haiku for cost efficiency
        return anthropic.Anthropic()

    def _call(self, system_prompt: str, content: str, endpoint: str) -> str:
        client = self._get_client()
        result = client.generate_post(system_prompt, content, endpoint)
        audit_log.log(
            service="claude",
            endpoint=endpoint,
            tokens_in=result.get("tokens_in", 0),
            tokens_out=result.get("tokens_out", 0),
            cost_usd=result.get("cost_usd", 0.0),
            status="success",
        )
        return result["content"]

    def repurpose_to_twitter(self, linkedin_post: str) -> str:
        """Rewrite a LinkedIn post as an X tweet (≤280 chars)."""
        system = _REPURPOSE_TWITTER_PROMPT.format(max_chars=TWITTER_MAX_CHARS)
        text = self._call(system, linkedin_post, "repurpose_twitter")
        # Hard truncate
        if len(text) > TWITTER_MAX_CHARS:
            cut = text[:TWITTER_MAX_CHARS].rfind(" ")
            text = text[:cut] if cut > 0 else text[:TWITTER_MAX_CHARS]
        return text

    def repurpose_to_threads(self, linkedin_post: str) -> str:
        """Rewrite a LinkedIn post as a Threads post (≤500 chars)."""
        system = _REPURPOSE_THREADS_PROMPT.format(max_chars=THREADS_MAX_CHARS)
        text = self._call(system, linkedin_post, "repurpose_threads")
        if len(text) > THREADS_MAX_CHARS:
            cut = text[:THREADS_MAX_CHARS].rfind(" ")
            text = text[:cut] if cut > 0 else text[:THREADS_MAX_CHARS]
        return text
