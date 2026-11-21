"""
Secret & Excluded Path Filter for Master AI Ingestion
=====================================================
Ensures secrets, private keys, environment variables, and ephemeral directories
are never indexed into vector or search databases.
"""

import os
import re
from pathlib import Path
from typing import Tuple, List

EXCLUDED_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "qdrant_db",
    "dist",
    "build",
    "coverage",
}

EXCLUDED_FILE_PATTERNS = [
    r"^\.env.*$",
    r".*\.pem$",
    r".*\.key$",
    r".*\.p12$",
    r".*\.keystore$",
    r".*\.lock$",
    r".*\.zip$",
    r".*\.tar\.gz$",
]

SECRET_VALUE_PATTERNS = [
    (re.compile(r"sk-[a-zA-Z0-9_\-]{20,}"), "[REDACTED_API_KEY]"),
    (re.compile(r"AIza[0-9A-Za-z\-_]{35}"), "[REDACTED_GOOGLE_KEY]"),
    (re.compile(r"ghp_[a-zA-Z0-9]{36}"), "[REDACTED_GITHUB_TOKEN]"),
    (re.compile(r"-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY-----[\s\S]+?-----END \1 KEY-----"), "[REDACTED_PRIVATE_KEY]"),
    (re.compile(r"(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]([^'\"]{8,})['\"]", re.IGNORECASE), r"\1: [REDACTED]"),
]


class SecretFilter:
    """Filters unsafe paths and redacts credentials before RAG ingestion."""

    @classmethod
    def is_path_allowed(cls, path: str | Path) -> Tuple[bool, str]:
        """Check if file path is permitted for ingestion."""
        p = Path(path)
        parts = [part.lower() for part in p.parts]

        for excluded in EXCLUDED_DIR_NAMES:
            if excluded in parts:
                return False, f"Directory '{excluded}' is excluded from indexing"

        filename = p.name
        for pattern in EXCLUDED_FILE_PATTERNS:
            if re.match(pattern, filename, re.IGNORECASE):
                return False, f"Filename '{filename}' matches excluded pattern '{pattern}'"

        return True, "Path allowed"

    @classmethod
    def sanitize_content(cls, content: str) -> Tuple[str, bool]:
        """Redact secrets from text before embedding or storing in vector DB."""
        redacted = False
        sanitized = content

        for pattern, replacement in SECRET_VALUE_PATTERNS:
            if pattern.search(sanitized):
                redacted = True
                sanitized = pattern.sub(replacement, sanitized)

        return sanitized, redacted
