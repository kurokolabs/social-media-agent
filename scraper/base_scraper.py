"""Base scraper class — implemented in Iteration 2."""


class BaseScraper:
    """Base class for all source scrapers."""

    def scrape(self) -> list[dict]:
        raise NotImplementedError
