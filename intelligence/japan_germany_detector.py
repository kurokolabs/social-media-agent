"""Detects articles relevant to Japan-Germany manufacturing intersection."""

JAPAN_KEYWORDS = ["japan", "japanisch", "meti", "kaizen", "monozukuri", "toyota", "lean", "nagoya"]
GERMANY_KEYWORDS = ["deutschland", "mittelstand", "fraunhofer", "vdi", "german", "germany", "münchen", "berlin"]
MANUFACTURING_KEYWORDS = ["fertigung", "manufacturing", "produktion", "fabrik", "factory", "industrie"]


class JapanGermanyDetector:
    """Returns True if article covers Japan-Germany manufacturing intersection."""

    def detect(self, article: dict) -> bool:
        text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
        has_japan = any(kw in text for kw in JAPAN_KEYWORDS)
        has_germany = any(kw in text for kw in GERMANY_KEYWORDS)
        has_manufacturing = any(kw in text for kw in MANUFACTURING_KEYWORDS)
        score = article.get("relevance_score", 0.0)

        if has_japan and has_germany:
            return True
        if has_japan and has_manufacturing and score > 5:
            return True
        return False
