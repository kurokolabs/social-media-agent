"""Dashboard session authentication.

Single-operator password model:
  - Set DASHBOARD_PASSWORD in .env (required in production).
  - Session = HMAC-signed cookie valid for SESSION_LIFETIME seconds.
  - CSRF token = HMAC(secret_key, session_token[:64]), stored in a
    JS-readable cookie so HTMX can inject it as X-CSRF-Token on every
    non-GET request.

Usage in middleware:
    from security.auth import check_auth, make_session_token, make_csrf_token, verify_csrf_token
"""
import base64
import hashlib
import hmac
import os
import time

_SESSION_LIFETIME = 86_400   # 24 hours
_SESSION_COOKIE   = "kuroko_session"
_CSRF_COOKIE      = "csrf_token"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _secret() -> bytes:
    return os.getenv("DASHBOARD_SECRET_KEY", "dev-key-change-in-production").encode()


def _password_hash() -> str:
    pw = os.getenv("DASHBOARD_PASSWORD", "")
    return hashlib.sha256(pw.encode()).hexdigest()


def _sign(payload: str) -> str:
    return hmac.new(_secret(), payload.encode(), hashlib.sha256).hexdigest()


# ---------------------------------------------------------------------------
# Session management
# ---------------------------------------------------------------------------

def make_session_token() -> str:
    """Return a signed session token encoding the current timestamp and password hash."""
    ts = str(int(time.time()))
    ph = _password_hash()
    payload = f"{ts}:{ph}"
    sig = _sign(payload)
    raw = f"{payload}:{sig}"
    return base64.urlsafe_b64encode(raw.encode()).decode()


def verify_session_token(token: str) -> bool:
    """Return True iff the token is valid, unexpired, and matches current password."""
    if not token:
        return False
    try:
        raw = base64.urlsafe_b64decode(token.encode()).decode()
        # Format: "<ts>:<password_hash>:<sig>"
        # Split from right so we get exactly 3 parts even if sha256 hex has colons (it won't)
        parts = raw.rsplit(":", 2)
        if len(parts) != 3:
            return False
        ts_str, ph, sig = parts

        # 1. Verify HMAC signature (constant-time)
        if not hmac.compare_digest(sig, _sign(f"{ts_str}:{ph}")):
            return False

        # 2. Check session expiry
        if time.time() - float(ts_str) > _SESSION_LIFETIME:
            return False

        # 3. Verify password hash still matches (invalidates sessions after password change)
        if not hmac.compare_digest(ph, _password_hash()):
            return False

        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# CSRF token (derived from session token — stable per session)
# ---------------------------------------------------------------------------

def make_csrf_token(session_token: str) -> str:
    """Return a CSRF token derived from the session token (not secret-key alone)."""
    seed = (session_token[:64] + "csrf").encode()
    return hmac.new(_secret(), seed, hashlib.sha256).hexdigest()


def verify_csrf_token(session_token: str, csrf_token: str) -> bool:
    """Return True iff csrf_token is the valid token for this session."""
    if not session_token or not csrf_token:
        return False
    expected = make_csrf_token(session_token)
    return hmac.compare_digest(expected, csrf_token)


# ---------------------------------------------------------------------------
# Request-level helpers
# ---------------------------------------------------------------------------

def check_auth(request) -> bool:
    """Return True if the request carries a valid session cookie."""
    token = request.cookies.get(_SESSION_COOKIE, "")
    return verify_session_token(token)


def is_password_configured() -> bool:
    """Return True if DASHBOARD_PASSWORD is set to a non-empty value."""
    return bool(os.getenv("DASHBOARD_PASSWORD", ""))


def verify_password(candidate: str) -> bool:
    """Constant-time password check against DASHBOARD_PASSWORD."""
    expected = os.getenv("DASHBOARD_PASSWORD", "")
    if not expected:
        return False
    return hmac.compare_digest(candidate, expected)
