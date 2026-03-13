"""Validates required environment variables before agent startup."""
import os

REQUIRED_VARS = [
    "ANTHROPIC_API_KEY",
    "GEMINI_API_KEY",
    "BUFFER_ACCESS_TOKEN",
    "BUFFER_CHANNEL_ID",
    "DATABASE_PATH",
    "LOG_PATH",
    "USE_MOCK_APIS",
]

MOCK_SKIP_VARS = {"ANTHROPIC_API_KEY", "GEMINI_API_KEY", "BUFFER_ACCESS_TOKEN"}


def validate() -> None:
    """Validate all required env vars. Raises EnvironmentError on missing vars."""
    use_mock = os.getenv("USE_MOCK_APIS", "false").lower() == "true"
    for var in REQUIRED_VARS:
        if use_mock and var in MOCK_SKIP_VARS:
            continue
        value = os.getenv(var)
        if not value:
            raise EnvironmentError(
                f"Missing required environment variable: {var}. "
                f"Copy .env.example to .env and fill in all values."
            )
