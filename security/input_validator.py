"""Input sanitization and validation utilities."""
import ipaddress
import re
from urllib.parse import urlparse

_ALLOWED_PLATFORMS = frozenset({"linkedin", "twitter", "instagram", "threads"})

# Control characters: all ASCII control chars except tab (9), newline (10), carriage return (13)
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

# Private / link-local / loopback IP ranges to block for SSRF protection
_BLOCKED_SCHEMES = frozenset({"file", "ftp", "gopher"})

# AWS/GCP/Azure metadata endpoints and similar
_BLOCKED_HOSTS_PATTERN = re.compile(
    r"^(localhost|metadata\.google\.internal|169\.254\.169\.254)$",
    re.IGNORECASE,
)

_PRIVATE_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),       # loopback
    ipaddress.ip_network("10.0.0.0/8"),         # private class A
    ipaddress.ip_network("172.16.0.0/12"),      # private class B
    ipaddress.ip_network("192.168.0.0/16"),     # private class C
    ipaddress.ip_network("169.254.0.0/16"),     # link-local (AWS metadata)
    ipaddress.ip_network("::1/128"),            # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),           # IPv6 unique local
    ipaddress.ip_network("fe80::/10"),          # IPv6 link-local
]


def sanitize_text(text: str, max_len: int = 2000) -> str:
    """Strip control chars, null bytes, leading/trailing whitespace. Truncate to max_len."""
    if not isinstance(text, str):
        text = str(text)
    # Remove null bytes and control characters
    text = text.replace("\x00", "")
    text = _CONTROL_CHAR_RE.sub("", text)
    # Strip surrounding whitespace
    text = text.strip()
    # Truncate
    if len(text) > max_len:
        text = text[:max_len]
    return text


def is_safe_url(url: str) -> bool:
    """Block SSRF: reject private IPs, localhost, file://, metadata endpoints.

    Returns True if the URL is safe to fetch, False if it should be blocked.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    # Block dangerous schemes
    scheme = (parsed.scheme or "").lower()
    if scheme in _BLOCKED_SCHEMES:
        return False

    # Only allow http/https
    if scheme not in ("http", "https"):
        return False

    host = (parsed.hostname or "").lower().strip("[]")  # strip IPv6 brackets

    if not host:
        return False

    # Block known metadata / localhost hostnames
    if _BLOCKED_HOSTS_PATTERN.match(host):
        return False

    # Attempt to resolve host as IP address
    try:
        addr = ipaddress.ip_address(host)
        for network in _PRIVATE_NETWORKS:
            if addr in network:
                return False
    except ValueError:
        # Not an IP literal — hostname; allow (DNS resolution happens at fetch time)
        pass

    return True


def validate_platform(platform: str) -> str:
    """Raise ValueError if not a known platform. Return platform."""
    if platform not in _ALLOWED_PLATFORMS:
        raise ValueError(
            f"Unknown platform {platform!r}. "
            f"Allowed values: {sorted(_ALLOWED_PLATFORMS)}"
        )
    return platform
