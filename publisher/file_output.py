"""File-based output fallback publisher."""
import os
import re
from datetime import datetime, timezone
from pathlib import Path


class FileOutput:
    """Saves posts as markdown files with YAML frontmatter."""

    def save(self, post: dict, reason: str = "fallback") -> str:
        """Write post to output/ as dated markdown file. Returns file path."""
        os.makedirs("output", exist_ok=True)
        now = datetime.now(timezone.utc)
        timestamp = now.strftime("%Y-%m-%d_%H-%M")
        content = post.get("content", "")
        slug = re.sub(r"[^a-z0-9]+", "-", content[:40].lower()).strip("-")
        filename = f"output/{timestamp}_{slug}_{reason}.md"
        frontmatter = f"""---
reason: {reason}
scheduled_at: {post.get("scheduled_at", "")}
post_type: {post.get("post_type", "")}
quality_score: {post.get("quality_score", 0)}
created_at: {now.isoformat()}
---

{content}
"""
        Path(filename).write_text(frontmatter, encoding="utf-8")
        return filename
