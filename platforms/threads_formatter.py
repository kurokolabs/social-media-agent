"""Threads content formatter — max 500 characters."""
from config import THREADS_MAX_CHARS


def format_threads(content: str) -> str:
    """Hard-truncate to 500 chars."""
    if len(content) <= THREADS_MAX_CHARS:
        return content
    cut = content[:THREADS_MAX_CHARS].rfind(" ")
    return content[:cut].rstrip() if cut > 0 else content[:THREADS_MAX_CHARS]
