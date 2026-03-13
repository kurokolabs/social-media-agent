"""Trend analyzer — scores articles by manufacturing/KI relevance."""


SCORE_RULES = [
    (["Fertigung", "Manufacturing", "Produktion", "factory", "Fabrik"], 3.0),
    (["IoT", "Predictive Maintenance", "Industrie 4.0", "Industry 4.0", "Sensor"], 3.0),
    (["KI-Agent", "AI agent", "Automatisierung", "Automation", "KI", "AI"], 2.0),
    (["Mittelstand", "SME", "KMU", "Familienunternehmen"], 2.0),
    (["Deutschland", "Germany", "Japan"], 1.0),
    (["consumer", "retail", "B2C", "Mode", "Fashion", "Lifestyle"], -1.0),
]


class TrendAnalyzer:
    """Scores articles 0.0-10.0 based on keyword relevance."""

    def _score_article(self, article: dict) -> float:
        text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
        score = article.get("relevance_score", 0.0)
        for keywords, points in SCORE_RULES:
            for kw in keywords:
                if kw.lower() in text:
                    score += points
                    break
        return min(max(round(score, 2), 0.0), 10.0)

    def analyze(self, articles: list[dict]) -> list[dict]:
        """Score each article and add relevance_score."""
        for article in articles:
            article["relevance_score"] = self._score_article(article)
        return articles

    def top_trends(self, articles: list[dict], n: int = 3) -> list[dict]:
        """Return top n articles by relevance score."""
        return sorted(articles, key=lambda a: a.get("relevance_score", 0), reverse=True)[:n]
