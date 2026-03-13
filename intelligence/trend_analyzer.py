"""Trend analyzer — stub for Iteration 1, fully implemented in Iteration 3."""


class TrendAnalyzer:
    """Scores articles by relevance to manufacturing/KI topics."""

    def analyze(self, articles: list[dict]) -> list[dict]:
        for article in articles:
            article["relevance_score"] = article.get("relevance_score", 0.0)
        return articles

    def top_trends(self, articles: list[dict], n: int = 3) -> list[dict]:
        sorted_articles = sorted(articles, key=lambda a: a.get("relevance_score", 0), reverse=True)
        return sorted_articles[:n]
