"""Generator for breaking-news posts triggered by alert_monitor alerts."""
from anthropic import Anthropic


class BreakingNewsGenerator:
    """
    Generates urgent, timely posts when a high-priority alert is detected.
    Produces platform-appropriate versions for LinkedIn, X, and Instagram.

    Expected alert dict structure:
        {
            "title": str,          # Headline of the news item
            "summary": str,        # 1–3 sentence summary
            "source": str,         # Source name (e.g. "OpenAI Blog")
            "url": str,            # Optional source URL
            "published_at": str,   # ISO datetime string
        }
    """

    SYSTEM_PROMPT = """Du bist der Kuroko Labs Social Media Agent.
Sprache: Deutsch. Stil: beobachtend, sachlich, kein Sales-Pitch.
Du berichtest über neue KI-Entwicklungen (neue Modelle, Paper, Benchmarks).
Keine Buzzwords wie "revolutionär", "disruptiv", "bahnbrechend", "innovativ".
Benutze keine Bindestriche als Stilmittel zwischen Satzteilen.
Bleibe bei den Fakten aus dem Artikel. Keine Erfindungen.
Firmenperspektive: "Wir sehen...", "Was das für DACH-Unternehmen bedeutet:", "Unsere Einschätzung:".
"""

    def __init__(self):
        import os
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def _call(self, user_prompt: str, max_tokens: int = 800) -> str:
        """Internal helper: call Claude and return the text content."""
        message = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=max_tokens,
            system=self.SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return message.content[0].text.strip()

    def generate_linkedin(self, alert: dict) -> str:
        """Generate a LinkedIn breaking-news post.

        Format:
          - 1-2 sentence dramatic hook containing the key fact
          - 4 blank lines (\\n\\n\\n\\n)
          - Substantive body: what it is, what changed, what it means for
            DACH enterprises, Kuroko Labs perspective
          - 3-5 hashtags
        """
        prompt = (
            "Schreibe einen LinkedIn-Breaking-News-Post basierend auf dieser Meldung.\n\n"
            "Format:\n"
            "- Erster Abschnitt: 1-2 Sätze dramatischer Hook mit der Kernaussage (konkrete Zahl "
            "oder überraschende Tatsache falls vorhanden).\n"
            "- Dann exakt vier Leerzeilen (\\n\\n\\n\\n).\n"
            "- Body (4-5 Absätze): Was ist passiert, was hat sich verändert, was bedeutet das "
            "für Unternehmen im DACH-Raum, Kuroko-Labs-Perspektive.\n"
            "- Hashtags am Ende (3-5 Stück).\n\n"
            f"Meldung:\n"
            f"Titel: {alert.get('title', '')}\n"
            f"Zusammenfassung: {alert.get('summary', '')}\n"
            f"Quelle: {alert.get('source', '')}"
        )
        return self._call(prompt, max_tokens=900)

    def generate_twitter(self, alert: dict) -> str:
        """Generate an X/Twitter post about the breaking news. Max 280 characters."""
        prompt = (
            "Schreibe einen Tweet über diese Breaking-News-Meldung. "
            "Maximal 280 Zeichen — hartes Limit. "
            "Eine Kernaussage: was ist passiert, konkrete Zahl wenn vorhanden, 1-2 Hashtags am Ende.\n\n"
            f"Meldung:\n"
            f"Titel: {alert.get('title', '')}\n"
            f"Zusammenfassung: {alert.get('summary', '')}\n"
            f"Quelle: {alert.get('source', '')}"
        )
        raw = self._call(prompt, max_tokens=120)
        # Hard truncate to 280 chars, preserving word boundaries
        if len(raw) <= 280:
            return raw
        cut = raw[:280].rfind(" ")
        return raw[:cut] if cut > 0 else raw[:280]

    def generate_instagram(self, alert: dict) -> str:
        """Generate an Instagram caption about the breaking news. 150-250 words."""
        prompt = (
            "Schreibe einen Instagram-Post über diese Breaking-News-Meldung. "
            "150-250 Wörter. Öffne mit einer konkreten Aussage oder Frage. "
            "Erkläre was passiert ist, was sich verändert, was das für den KI-Markt bedeutet. "
            "Emojis sparsam (max 2). Max 5 Hashtags am Ende.\n\n"
            f"Meldung:\n"
            f"Titel: {alert.get('title', '')}\n"
            f"Zusammenfassung: {alert.get('summary', '')}\n"
            f"Quelle: {alert.get('source', '')}"
        )
        return self._call(prompt, max_tokens=500)

    def generate_all(self, alert: dict) -> dict:
        """Generate posts for all three platforms.

        Returns:
            {
                'linkedin':  str,
                'twitter':   str,
                'instagram': str,
            }
        """
        return {
            "linkedin":  self.generate_linkedin(alert),
            "twitter":   self.generate_twitter(alert),
            "instagram": self.generate_instagram(alert),
        }
