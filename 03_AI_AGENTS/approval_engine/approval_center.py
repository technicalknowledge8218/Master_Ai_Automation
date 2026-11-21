"""approval_center.py
MASTER-AI Centralized Approval Center & Governance Gateway

Enforces approval governance for:
- PAID_API_CALL
- EXTERNAL_SERVICE
- DEPENDENCY_INSTALL
- REPO_INTEGRATION
- DESTRUCTIVE_OPERATION
- PRODUCTION_CHANGE
- EXTERNAL_PUBLISH
- SENSITIVE_ACCOUNT

Provides ticket issuance, approval tokens, state transitions, TTL expiration,
and integration with HumanApprovalEngine.
"""

import os
import sys
import json
import time
import uuid
import datetime
from typing import Dict, Any, List, Optional, Set, Tuple

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

try:
    from approval_engine.approval_engine import HumanApprovalEngine, ApprovalViolation
except ImportError:
    from .approval_engine import HumanApprovalEngine, ApprovalViolation


VALID_APPROVAL_CATEGORIES = {
    "PAID_API_CALL",
    "EXTERNAL_SERVICE",
    "DEPENDENCY_INSTALL",
    "REPO_INTEGRATION",
    "DESTRUCTIVE_OPERATION",
    "PRODUCTION_CHANGE",
    "EXTERNAL_PUBLISH",
    "SENSITIVE_ACCOUNT"
}

APPROVAL_CENTER_LEDGER = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "runs", "APPROVAL_CENTER_TICKETS.json")


class ApprovalCenter:
    """Central manager for sensitive operation approval tickets and policies."""

    def __init__(self, ledger_path: Optional[str] = None):
        self.ledger_path = ledger_path or APPROVAL_CENTER_LEDGER
        self.engine = HumanApprovalEngine()
        os.makedirs(os.path.dirname(os.path.abspath(self.ledger_path)), exist_ok=True)
        self._tickets: Dict[str, Dict[str, Any]] = self._load_tickets()

    def _load_tickets(self) -> Dict[str, Dict[str, Any]]:
        if os.path.exists(self.ledger_path):
            try:
                with open(self.ledger_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_tickets(self):
        try:
            tmp = self.ledger_path + f".{uuid.uuid4().hex[:6]}.tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self._tickets, f, indent=2)
            os.replace(tmp, self.ledger_path)
        except Exception:
            pass

    def request_approval(
        self,
        category: str,
        title: str,
        description: str,
        requesting_agent: str,
        target_resource: str,
        ttl_seconds: int = 3600,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Creates an approval request ticket requiring human authorization."""
        if category not in VALID_APPROVAL_CATEGORIES:
            raise ValueError(f"Invalid approval category: '{category}'")

        ticket_id = f"TKT-{uuid.uuid4().hex[:8]}"
        now = datetime.datetime.now()
        expires_at = now + datetime.timedelta(seconds=ttl_seconds)

        ticket = {
            "ticket_id": ticket_id,
            "category": category,
            "title": title,
            "description": description,
            "requesting_agent": requesting_agent,
            "target_resource": target_resource,
            "status": "PENDING",  # PENDING, APPROVED, REJECTED, REVOKED, EXPIRED
            "auth_token": None,
            "requested_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
            "ttl_seconds": ttl_seconds,
            "decided_at": None,
            "decided_by": None,
            "decision_reason": None,
            "metadata": metadata or {}
        }

        self._tickets[ticket_id] = ticket
        self._save_tickets()
        return ticket

    def approve_ticket(
        self,
        ticket_id: str,
        actor: str = "human_operator",
        reason: str = "Approved by human operator"
    ) -> Dict[str, Any]:
        """Approves a ticket and generates an AUTH token."""
        ticket = self._tickets.get(ticket_id)
        if not ticket:
            raise KeyError(f"Ticket '{ticket_id}' not found.")

        if self.is_expired(ticket_id):
            ticket["status"] = "EXPIRED"
            self._save_tickets()
            raise ValueError(f"Ticket '{ticket_id}' has expired.")

        if ticket["status"] != "PENDING":
            raise ValueError(f"Ticket '{ticket_id}' is in status '{ticket['status']}' and cannot be approved.")

        # Issue authorization token with prefix
        token = "AUTH-" + f"{uuid.uuid4().hex[:12].upper()}"
        ticket["status"] = "APPROVED"
        ticket["auth_token"] = token
        ticket["decided_at"] = datetime.datetime.now().isoformat()
        ticket["decided_by"] = actor
        ticket["decision_reason"] = reason

        self._save_tickets()
        return ticket

    def reject_ticket(
        self,
        ticket_id: str,
        actor: str = "human_operator",
        reason: str = "Rejected by human operator"
    ) -> Dict[str, Any]:
        """Rejects an approval request."""
        ticket = self._tickets.get(ticket_id)
        if not ticket:
            raise KeyError(f"Ticket '{ticket_id}' not found.")

        ticket["status"] = "REJECTED"
        ticket["decided_at"] = datetime.datetime.now().isoformat()
        ticket["decided_by"] = actor
        ticket["decision_reason"] = reason
        ticket["auth_token"] = None

        self._save_tickets()
        return ticket

    def revoke_ticket(
        self,
        ticket_id: str,
        actor: str = "human_operator",
        reason: str = "Revoked by human operator"
    ) -> Dict[str, Any]:
        """Revokes a previously approved ticket."""
        ticket = self._tickets.get(ticket_id)
        if not ticket:
            raise KeyError(f"Ticket '{ticket_id}' not found.")

        ticket["status"] = "REVOKED"
        ticket["decided_at"] = datetime.datetime.now().isoformat()
        ticket["decided_by"] = actor
        ticket["decision_reason"] = reason
        ticket["auth_token"] = None

        self._save_tickets()
        return ticket

    def is_expired(self, ticket_id: str) -> bool:
        """Checks if a ticket has exceeded its TTL."""
        ticket = self._tickets.get(ticket_id)
        if not ticket:
            return True
        expires_at_str = ticket.get("expires_at")
        if not expires_at_str:
            return False
        try:
            expires_at = datetime.datetime.fromisoformat(expires_at_str)
            return datetime.datetime.now() > expires_at
        except Exception:
            return False

    def verify_token(self, ticket_id: str, token: Optional[str]) -> bool:
        """Verifies an authorization token against an active approved ticket."""
        if not token or not ticket_id:
            return False
        ticket = self._tickets.get(ticket_id)
        if not ticket:
            return False
        if ticket["status"] != "APPROVED":
            return False
        if self.is_expired(ticket_id):
            return False
        return ticket.get("auth_token") == token

    def list_tickets(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists tickets optionally filtered by status."""
        tickets = list(self._tickets.values())
        if status:
            return [t for t in tickets if t.get("status") == status]
        return tickets

    def get_ticket(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves ticket by ID."""
        return self._tickets.get(ticket_id)
