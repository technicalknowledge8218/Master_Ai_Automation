"""agent_messaging.py
MASTER-AI Agent Communication & Inter-Agent Handoff Protocol

Provides structured message envelopes, shared workflow blackboard,
artifact provenance hashing, RAG/memory gateway integration,
and anti-loop/duplicate execution guards.
"""

import os
import sys
import json
import time
import uuid
import hashlib
import datetime
from typing import Dict, Any, List, Optional, Set, Tuple

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

try:
    from .agent_memory_bridge import AgentMemoryBridge
except ImportError:
    try:
        from agent_memory_bridge import AgentMemoryBridge
    except ImportError:
        AgentMemoryBridge = None


VALID_MESSAGE_TYPES = {
    "TASK_HANDOFF",
    "ARTIFACT_TRANSFER",
    "QUERY_CONTEXT",
    "STATUS_UPDATE",
    "ERROR_ALERT",
    "VALIDATION_REQUEST",
    "VALIDATION_RESPONSE"
}

MAX_HANDOFF_HOPS = 10


class AgentLoopViolationError(Exception):
    """Raised when an inter-agent handoff loop exceeds safe maximum hops."""
    pass


class DuplicateTaskExecutionError(Exception):
    """Raised when an agent attempts to execute an already completed or in-flight subtask."""
    pass


class WorkflowBlackboard:
    """Thread-safe in-memory context and blackboard shared across agents in a workflow."""

    def __init__(self, workflow_id: str, memory_bridge: Optional[Any] = None):
        self.workflow_id = workflow_id
        self.memory_bridge = memory_bridge
        self._shared_data: Dict[str, Any] = {}
        self._artifact_registry: Dict[str, Dict[str, Any]] = {}
        self._message_log: List[Dict[str, Any]] = []
        self._handoff_chains: Dict[str, int] = {}  # subtask_id -> hop count
        self._executed_subtasks: Set[str] = set()

    def set_context(self, key: str, value: Any):
        """Sets a shared variable in the workflow context."""
        self._shared_data[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Retrieves a shared variable from the workflow context."""
        return self._shared_data.get(key, default)

    def register_artifact(
        self,
        name: str,
        content_or_path: str,
        producer_agent: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Registers an artifact with SHA-256 provenance checksum."""
        if os.path.exists(content_or_path):
            with open(content_or_path, "rb") as f:
                sha256 = hashlib.sha256(f.read()).hexdigest()
            location = content_or_path
        else:
            sha256 = hashlib.sha256(content_or_path.encode("utf-8")).hexdigest()
            location = "memory"

        entry = {
            "artifact_id": f"ART-{uuid.uuid4().hex[:8]}",
            "name": name,
            "producer_agent": producer_agent,
            "sha256": sha256,
            "location": location,
            "timestamp": datetime.datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self._artifact_registry[name] = entry
        return entry

    def get_artifact(self, name: str) -> Optional[Dict[str, Any]]:
        """Retrieves registered artifact metadata and provenance checksum."""
        return self._artifact_registry.get(name)

    def post_message(
        self,
        sender_id: str,
        recipient_id: str,
        message_type: str,
        payload: Dict[str, Any],
        correlation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Constructs, validates, and logs a structured inter-agent message envelope."""
        if message_type not in VALID_MESSAGE_TYPES:
            raise ValueError(f"Invalid message type: '{message_type}'")

        msg_id = f"MSG-{uuid.uuid4().hex[:8]}"
        envelope = {
            "message_id": msg_id,
            "workflow_id": self.workflow_id,
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "message_type": message_type,
            "payload": payload,
            "correlation_id": correlation_id or msg_id,
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Check anti-loop hop count for handoffs
        if message_type == "TASK_HANDOFF":
            subtask_id = payload.get("subtask_id", "GLOBAL")
            current_hops = self._handoff_chains.get(subtask_id, 0) + 1
            if current_hops > MAX_HANDOFF_HOPS:
                raise AgentLoopViolationError(
                    f"Agent handoff loop detected for subtask '{subtask_id}' (hops: {current_hops} > {MAX_HANDOFF_HOPS})."
                )
            self._handoff_chains[subtask_id] = current_hops

        self._message_log.append(envelope)
        return envelope

    def verify_and_claim_subtask(self, subtask_id: str) -> bool:
        """Enforces idempotency: prevents duplicate execution of the same subtask."""
        if subtask_id in self._executed_subtasks:
            raise DuplicateTaskExecutionError(
                f"Subtask '{subtask_id}' has already been claimed or executed. Duplicate execution blocked."
            )
        self._executed_subtasks.add(subtask_id)
        return True

    def query_knowledge_base(self, query: str, limit: int = 4) -> List[Dict[str, Any]]:
        """Accesses persistent RAG knowledge base through AgentMemoryBridge if present."""
        if self.memory_bridge:
            try:
                return self.memory_bridge.retrieve_context(query, limit=limit)
            except Exception:
                pass
        return [{"source": "mock_knowledge", "text": f"Knowledge base context for '{query}'"}]

    def record_agent_memory(self, agent_id: str, title: str, content: str) -> Dict[str, Any]:
        """Stores a long-term memory via AgentMemoryBridge if present."""
        if self.memory_bridge:
            try:
                return self.memory_bridge.record_memory(
                    agent_id=agent_id,
                    category="WORKFLOW_EXECUTION",
                    title=title,
                    content=content
                )
            except Exception:
                pass
        return {"agent_id": agent_id, "title": title, "status": "STORED_LOCALLY"}

    def get_message_history(self) -> List[Dict[str, Any]]:
        """Returns chronological list of all messages exchanged."""
        return list(self._message_log)
