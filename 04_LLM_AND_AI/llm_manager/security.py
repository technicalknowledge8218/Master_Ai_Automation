"""Master AI - Security & Secret Protection for Intelligence Layer.

Enforces zero hardcoded credentials, redaction in logs/responses,
permission boundaries, cost caps, and audit trails for LLM configurations.
"""

from __future__ import annotations

import datetime
import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict

# Regex patterns for sensitive tokens and API keys
SENSITIVE_KEY_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}", re.IGNORECASE),
    re.compile(r"ghp_[A-Za-z0-9]{30,}", re.IGNORECASE),
    re.compile(r"AIza[0-9A-Za-z-_]{35}", re.IGNORECASE),
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]+['\"]"),
]

logger = logging.getLogger("master_ai.security")


def redact_secrets(text: str) -> str:
    """Mask any discovered API keys or tokens in text."""
    if not isinstance(text, str):
        return text

    sanitized = text
    for pattern in SENSITIVE_KEY_PATTERNS:
        sanitized = pattern.sub("[REDACTED_SECRET]", sanitized)
    return sanitized


def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively redact dictionary keys and values containing sensitive terms."""
    clean: Dict[str, Any] = {}
    sensitive_keys = {"api_key", "secret", "password", "token", "authorization", "auth"}

    for k, v in data.items():
        if any(s in k.lower() for s in sensitive_keys):
            clean[k] = "[REDACTED_KEY_VALUE]"
        elif isinstance(v, dict):
            clean[k] = sanitize_dict(v)
        elif isinstance(v, list):
            clean[k] = [
                sanitize_dict(item) if isinstance(item, dict) else redact_secrets(str(item))
                for item in v
            ]
        elif isinstance(v, str):
            clean[k] = redact_secrets(v)
        else:
            clean[k] = v
    return clean


class SecurityBoundary:
    """Enforces cost constraints, offline rules, and access permissions."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.workspace_root = workspace_root or Path(__file__).resolve().parents[2]
        self.enforce_zero_paid_api = os.getenv("ENFORCE_ZERO_PAID_API", "true").lower() in ("true", "1")
        self.max_daily_budget_usd = float(os.getenv("MAX_DAILY_BUDGET_USD", "0.00"))
        self.current_spent_usd = 0.0
        self.audit_log_path = self.workspace_root / "00_CORE_SYSTEM" / "registry" / "LLM_SECURITY_AUDIT.jsonl"

    def can_invoke_model(self, model_id: str, estimated_cost_usd: float = 0.0, is_local_or_mock: bool = True) -> tuple[bool, str]:
        """Validate whether a model invocation is authorized under current policy."""
        if is_local_or_mock:
            return True, "Authorized (Local/Mock Zero-Cost Engine)"

        if self.enforce_zero_paid_api and estimated_cost_usd > 0.0:
            msg = f"Invocation blocked: Model '{model_id}' incurs cost (${estimated_cost_usd:.4f}) and ENFORCE_ZERO_PAID_API is active."
            self.log_security_event("BLOCKED_PAID_MODEL", {"model_id": model_id, "estimated_cost": estimated_cost_usd, "reason": msg})
            return False, msg

        if (self.current_spent_usd + estimated_cost_usd) > self.max_daily_budget_usd:
            msg = f"Invocation blocked: Cost exceeds daily budget limit of ${self.max_daily_budget_usd:.2f}."
            self.log_security_event("BUDGET_EXCEEDED", {"model_id": model_id, "estimated_cost": estimated_cost_usd, "reason": msg})
            return False, msg

        return True, "Authorized"

    def record_cost(self, cost_usd: float) -> None:
        """Record realized expenditure."""
        self.current_spent_usd += max(0.0, cost_usd)

    def log_security_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Append security event to audit trail with redacted details."""
        try:
            self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
            entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "event_type": event_type,
                "details": sanitize_dict(details),
            }
            with open(self.audit_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.error("Failed to write to LLM security audit log: %s", e)
