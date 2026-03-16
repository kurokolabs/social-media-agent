"""LinkedIn content formatter."""
from config import POST_MAX_HASHTAGS


def format_linkedin(content: str) -> str:
    """Ensure hashtag count is within limits. Returns formatted content."""
    lines = content.strip().split("\n")
    hashtag_lines = [l for l in lines if l.strip().startswith("#")]
    if len(hashtag_lines) <= POST_MAX_HASHTAGS:
        return content
    # Keep only the last POST_MAX_HASHTAGS hashtag tokens
    import re
    hashtags = re.findall(r"#\w+", content)
    if len(hashtags) > POST_MAX_HASHTAGS:
        keep = set(hashtags[-POST_MAX_HASHTAGS:])
        for tag in hashtags[:-POST_MAX_HASHTAGS]:
            content = content.replace(tag + " ", "", 1).replace(tag, "", 1)
    return content.strip()
