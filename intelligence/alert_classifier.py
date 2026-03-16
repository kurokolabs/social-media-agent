"""Classify articles into alert types and priority scores."""

# Keywords that signal a new model release
NEW_MODEL_SIGNALS = [
    "we're releasing", "introducing", "announcing", "launch", "release",
    "gpt-", "claude-", "gemini", "llama", "mistral", "qwen", "gemma",
    "new model", "neues modell", "model release", "api access",
]

# Keywords that signal a benchmark/performance result
BENCHMARK_SIGNALS = [
    "benchmark", "mmlu", "humaneval", "swe-bench", "arena", "leaderboard",
    "outperforms", "state-of-the-art", "sota", "performance comparison",
    "beats", "surpasses", "evaluation",
]

# Keywords for RAG / architecture papers
ARCHITECTURE_SIGNALS = [
    "rag", "retrieval", "graph rag", "graphrag", "knowledge graph",
    "vector database", "embedding", "reranker", "hyde", "raptor",
    "agentic rag", "corrective rag", "self-rag",
]

# High-priority sources (breaking news)
HIGH_PRIORITY_SOURCES = {
    "OpenAI Blog", "Anthropic", "Google AI Blog", "DeepMind",
    "HuggingFace", "Meta AI",
}


def classify(article: dict) -> tuple[str, int]:
    """
    Returns (alert_type, priority).
    alert_type: 'new_model' | 'benchmark' | 'rag_architecture' | 'research_paper' | 'other'
    priority: 0=normal, 1=high, 2=breaking
    """
    text = (article.get("title", "") + " " + article.get("summary", "")).lower()
    source = article.get("source", "")

    # Determine type
    if any(signal in text for signal in NEW_MODEL_SIGNALS):
        alert_type = "new_model"
    elif any(signal in text for signal in BENCHMARK_SIGNALS):
        alert_type = "benchmark"
    elif any(signal in text for signal in ARCHITECTURE_SIGNALS):
        alert_type = "rag_architecture"
    elif source in {"arXiv-LLM", "PapersWithCode"}:
        alert_type = "research_paper"
    else:
        alert_type = "other"

    # Determine priority:
    # 2 = breaking: new_model from HIGH_PRIORITY_SOURCES
    # 1 = high: benchmark or rag_architecture from any source, or new_model from other source
    # 0 = normal: everything else
    if alert_type == "new_model" and source in HIGH_PRIORITY_SOURCES:
        priority = 2
    elif alert_type in ("benchmark", "rag_architecture"):
        priority = 1
    elif alert_type == "new_model":
        priority = 1
    else:
        priority = 0

    return alert_type, priority
