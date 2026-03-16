"""Utility to detect stale or weak secrets and warn on startup."""
import hashlib
import math
import os
import secrets
import string


# Secrets that look like common placeholder / default values
_KNOWN_WEAK_VALUES = frozenset({
    "change-me-in-production",
    "changeme",
    "secret",
    "password",
    "your_secret_here",
    "replace_me",
    "",
})


def _estimate_entropy_bits(value: str) -> float:
    """Rough Shannon-entropy estimate scaled by string length."""
    if not value:
        return 0.0
    freq: dict[str, int] = {}
    for ch in value:
        freq[ch] = freq.get(ch, 0) + 1
    n = len(value)
    entropy_per_char = -sum((c / n) * math.log2(c / n) for c in freq.values())
    return entropy_per_char * n


def check_secret_strength(
    name: str,
    value: str,
    min_entropy_bits: int = 128,
) -> list[str]:
    """Return a list of warning strings if the secret is too weak or a default.

    Parameters
    ----------
    name:
        Environment variable name (used only for messaging).
    value:
        The actual secret value to evaluate.
    min_entropy_bits:
        Minimum acceptable entropy estimate (default 128 bits).
    """
    warnings: list[str] = []

    if not value:
        warnings.append(f"[SECRET] {name} is not set (empty value).")
        return warnings

    if value.lower() in _KNOWN_WEAK_VALUES:
        warnings.append(
            f"[SECRET] {name} appears to be a placeholder/default value. "
            "Set a strong random secret before deploying."
        )

    entropy = _estimate_entropy_bits(value)
    if entropy < min_entropy_bits:
        warnings.append(
            f"[SECRET] {name} has low estimated entropy "
            f"({entropy:.1f} bits < {min_entropy_bits} required). "
            "Use a longer, more random value."
        )

    return warnings


def audit_secrets_on_startup() -> None:
    """Called at app startup. Logs warnings for weak or missing secrets."""
    from security.audit_log import audit_log  # local import to avoid circular deps

    checks = [
        ("DASHBOARD_PASSWORD",      os.getenv("DASHBOARD_PASSWORD", ""),      16, 64),
        ("DASHBOARD_SECRET_KEY",    os.getenv("DASHBOARD_SECRET_KEY", ""),    32, 128),
        ("BUFFER_WEBHOOK_SECRET",   os.getenv("BUFFER_WEBHOOK_SECRET", ""),   20, 80),
        ("IG_WEBHOOK_VERIFY_TOKEN", os.getenv("IG_WEBHOOK_VERIFY_TOKEN", ""), 20, 80),
        ("IG_APP_SECRET",           os.getenv("IG_APP_SECRET", ""),           20, 80),
    ]

    all_warnings: list[str] = []

    for env_name, value, min_len, min_entropy in checks:
        # Length check
        if len(value) < min_len:
            all_warnings.append(
                f"[SECRET] {env_name} is too short "
                f"(length {len(value)} < minimum {min_len} characters)."
            )
        # Entropy / weakness check
        all_warnings.extend(check_secret_strength(env_name, value, min_entropy))

    for warning in all_warnings:
        # Log each warning as a structured audit entry so it appears in audit.jsonl
        audit_log.log(
            service="startup",
            endpoint="secrets_audit",
            tokens_in=0,
            tokens_out=0,
            cost_usd=0.0,
            status="warning",
            error=warning,
        )
        # Also print to stderr so it shows in container/process logs
        import sys
        print(warning, file=sys.stderr)
