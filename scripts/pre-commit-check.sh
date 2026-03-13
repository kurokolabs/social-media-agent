#!/usr/bin/env bash
# Pre-commit hook: block hardcoded secrets in Python files
set -e

SECRETS_FOUND=$(grep -rn "sk-ant\|AIzaSy\|ya29\." --include="*.py" . 2>/dev/null || true)

if [ -n "$SECRETS_FOUND" ]; then
    echo "BLOCKED: hardcoded secret detected:"
    echo "$SECRETS_FOUND"
    exit 1
fi

echo "Pre-commit check passed: no hardcoded secrets found."
exit 0
