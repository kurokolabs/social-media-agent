"""Central scraper registry — all available scrapers by category."""

CONSULTING_SCRAPERS = [
    "scraper.mckinsey.McKinseyScraper",
    "scraper.bcg.BCGScraper",
    "scraper.roland_berger.RolandBergerScraper",
    "scraper.deloitte.DeloitteScraper",
]

INDUSTRY_DE_SCRAPERS = [
    "scraper.fraunhofer.FraunhoferScraper",
    "scraper.vdi.VDIScraper",
    "scraper.bitkom.BitkomScraper",
    "scraper.plattform_i40.PlattformI40Scraper",
    "scraper.iw_koeln.IWKoelnScraper",
]

JAPAN_SCRAPERS = [
    "scraper.meti.METIScraper",
]

RESEARCH_SCRAPERS = [
    "scraper.arxiv.ArXivScraper",
    "scraper.arxiv_llm.ArXivLLMScraper",
    "scraper.papers_with_code.PapersWithCodeScraper",
    "scraper.semantic_scholar.SemanticScholarScraper",
    "scraper.acl_anthology.ACLAnthologyScraper",
]

AI_LAB_SCRAPERS = [
    "scraper.anthropic_research.AnthropicResearchScraper",
    "scraper.deepmind_blog.DeepMindBlogScraper",
    "scraper.google_ai_blog.GoogleAIBlogScraper",
    "scraper.huggingface_blog.HuggingFaceBlogScraper",
    "scraper.openai_blog.OpenAIBlogScraper",
]

NEWS_SCRAPERS = [
    "scraper.techcrunch_ai.TechCrunchAIScraper",
    "scraper.venturebeat_ai.VentureBeatAIScraper",
    "scraper.mit_tech_review.MITTechReviewScraper",
    "scraper.reuters_tech.ReutersTechScraper",
]

# Competitor monitoring (Feature 4)
COMPETITOR_SCRAPERS = [
    "scraper.aleph_alpha.AlephAlphaScraper",
    "scraper.deepl_blog.DeepLBlogScraper",
    "scraper.sap_news.SAPNewsScraper",
    "scraper.siemens_insights.SiemensInsightsScraper",
    "scraper.bosch_tech.BoschTechScraper",
]

# Alert monitor only checks these high-signal sources
BREAKING_NEWS_SCRAPERS = AI_LAB_SCRAPERS + NEWS_SCRAPERS[:2]

ALL_SCRAPERS = (
    CONSULTING_SCRAPERS
    + INDUSTRY_DE_SCRAPERS
    + JAPAN_SCRAPERS
    + RESEARCH_SCRAPERS
    + AI_LAB_SCRAPERS
    + NEWS_SCRAPERS
    + COMPETITOR_SCRAPERS
)


def load_scraper(dotted_path: str):
    """Dynamically import and instantiate a scraper class by dotted path.

    Example:
        scraper = load_scraper("scraper.arxiv.ArXivScraper")
    """
    module_path, class_name = dotted_path.rsplit(".", 1)
    import importlib
    module = importlib.import_module(module_path)
    cls = getattr(module, class_name)
    return cls()


def get_all_scrapers() -> list:
    """Instantiate and return all registered scrapers."""
    return [load_scraper(p) for p in ALL_SCRAPERS]


def get_breaking_news_scrapers() -> list:
    """Instantiate and return only the high-signal scrapers used by alert_monitor."""
    return [load_scraper(p) for p in BREAKING_NEWS_SCRAPERS]


def get_competitor_scrapers() -> list:
    """Instantiate and return competitor monitoring scrapers (Feature 4)."""
    return [load_scraper(p) for p in COMPETITOR_SCRAPERS]
