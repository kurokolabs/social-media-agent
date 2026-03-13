"""Tests for security module."""
import json
import os
import time
import pytest
from pathlib import Path


def test_secrets_validator_blocks_missing_key(monkeypatch):
    """secrets_validator should raise EnvironmentError for missing required var."""
    monkeypatch.setenv("USE_MOCK_APIS", "false")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("GEMINI_API_KEY", "test")
    monkeypatch.setenv("BUFFER_ACCESS_TOKEN", "test")
    monkeypatch.setenv("BUFFER_CHANNEL_ID", "test")
    monkeypatch.setenv("DATABASE_PATH", "./test.db")
    monkeypatch.setenv("LOG_PATH", "./logs")
    with pytest.raises(EnvironmentError) as exc_info:
        from security import secrets_validator
        import importlib
        importlib.reload(secrets_validator)
        secrets_validator.validate()
    assert "ANTHROPIC_API_KEY" in str(exc_info.value)


def test_secrets_validator_mock_flag_skips_api_keys(monkeypatch, tmp_path):
    """With USE_MOCK_APIS=true, validator should not require API keys."""
    monkeypatch.setenv("USE_MOCK_APIS", "true")
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("LOG_PATH", str(tmp_path / "logs"))
    monkeypatch.setenv("BUFFER_CHANNEL_ID", "mock_channel")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("BUFFER_ACCESS_TOKEN", raising=False)
    from security.secrets_validator import validate
    validate()  # Should not raise


def test_audit_log_writes_jsonl(mock_env):
    """AuditLog.log should write valid JSONL entries."""
    from security.audit_log import AuditLog
    log = AuditLog()
    log.log("test_service", "test_endpoint", 100, 200, 0.005, "success")
    log_path = os.path.join(os.getenv("LOG_PATH"), "audit.jsonl")
    assert os.path.exists(log_path)
    with open(log_path) as f:
        entry = json.loads(f.readline())
    assert entry["service"] == "test_service"
    assert entry["tokens_in"] == 100
    assert entry["status"] == "success"


def test_rate_limiter_enforces_delay():
    """RateLimiter.wait should enforce minimum 2.5s between same-domain requests."""
    from security.rate_limiter import RateLimiter
    limiter = RateLimiter()
    domain = "test-domain-rate-limit.example.com"
    start = time.time()
    limiter.wait(domain)
    limiter.wait(domain)
    elapsed = time.time() - start
    assert elapsed >= 2.5, f"Expected >= 2.5s delay, got {elapsed:.2f}s"


def test_no_hardcoded_secrets():
    """No production Python files should contain hardcoded API key patterns."""
    import subprocess
    # Scan only production source dirs — exclude tests (contains the pattern as a string literal)
    # and .venv (third-party code).
    dirs = ["security", "scraper", "intelligence", "generator", "publisher", "storage", "scheduler", "main.py", "config.py"]
    for target in dirs:
        result = subprocess.run(
            ["grep", "-rn", "sk-ant", "--include=*.py", target],
            capture_output=True,
            text=True,
            cwd=".",
        )
        assert result.stdout.strip() == "", f"Hardcoded sk-ant secret in {target}:\n{result.stdout}"
        result2 = subprocess.run(
            ["grep", "-rn", "AIzaSy", "--include=*.py", target],
            capture_output=True,
            text=True,
            cwd=".",
        )
        assert result2.stdout.strip() == "", f"Hardcoded AIzaSy secret in {target}:\n{result2.stdout}"
