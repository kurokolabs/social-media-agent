"""Integration tests for the full pipeline."""
import os
import pytest
from pathlib import Path


def test_full_pipeline_mock(mock_env, tmp_database):
    """Full pipeline with USE_MOCK_APIS=true should complete without errors."""
    from main import run_full_pipeline
    summary = run_full_pipeline()
    assert "articles_scraped" in summary
    assert summary["articles_scraped"] > 0
    # Check audit log exists
    log_path = os.path.join(os.getenv("LOG_PATH"), "audit.jsonl")
    assert os.path.exists(log_path)
