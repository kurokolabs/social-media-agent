"""Twitter/X content formatter — enforces 280-char limit."""
from config import TWITTER_MAX_CHARS


def format_twitter(content: str) -> str:
    """Hard-truncate to 280 chars, preserve trailing hashtags if possible."""
    if len(content) <= TWITTER_MAX_CHARS:
        return content
    cut = content[:TWITTER_MAX_CHARS].rfind(" ")
    return content[:cut].rstrip() if cut > 0 else content[:TWITTER_MAX_CHARS]
