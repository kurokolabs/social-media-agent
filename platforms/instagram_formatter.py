"""Instagram caption formatter."""


def format_instagram(content: str, image_path: str | None = None) -> dict:
    """Return dict with formatted caption and image_path."""
    # Instagram captions: max 2200 chars, max 30 hashtags
    caption = content.strip()
    if len(caption) > 2200:
        caption = caption[:2197] + "..."
    return {"caption": caption, "image_path": image_path}
