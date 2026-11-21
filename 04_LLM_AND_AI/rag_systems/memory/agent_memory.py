"""
Persistent Long-Term Agent Memory for Master AI
===============================================
Maintains episodic and semantic memory across 6 core categories with authorization,
vector indexing, deduplication, and JSON ledger persistence.
"""

import time
import json
import uuid
import hashlib
import importlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict


MEMORY_CATEGORIES = {
    "project_memory",
    "task_history",
    "technical_decisions",
    "reusable_solutions",
    "user_preferences",
    "agent_knowledge",
}


@dataclass
class MemoryRecord:
    """Represents an atomic stored memory."""
    memory_id: str
    category: str
    title: str
    content: str
    agent_id: str
    tags: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    content_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryRecord":
        return cls(
            memory_id=data["memory_id"],
            category=data["category"],
            title=data.get("title", ""),
            content=data["content"],
            agent_id=data.get("agent_id", "orchestrator"),
            tags=data.get("tags", []),
            timestamp=data.get("timestamp", time.time()),
            metadata=data.get("metadata", {}),
            content_hash=data.get("content_hash", ""),
        )


class AgentMemoryManager:
    """Manages creation, vectorization, retrieval, and ledger tracking of agent memories."""

    COLLECTION_NAME = "agent_memory"

    def __init__(
        self,
        qdrant_manager=None,
        embedding_engine=None,
        ledger_path: Optional[Path | str] = None,
    ):
        if ledger_path is None:
            self.ledger_path = Path(__file__).resolve().parent / "AGENT_MEMORY_LEDGER.json"
        else:
            self.ledger_path = Path(ledger_path)

        # Resolve Qdrant
        if qdrant_manager is None:
            vdb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.vector_db")
            self.qdrant = vdb_mod.QdrantManager()
        else:
            self.qdrant = qdrant_manager

        # Resolve Embedding
        if embedding_engine is None:
            emb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.embeddings")
            self.embedder = emb_mod.get_embedding_engine("auto")
        else:
            self.embedder = embedding_engine

        # Ensure collection exists
        self.qdrant.ensure_collection(
            collection_name=self.COLLECTION_NAME,
            dimension=self.embedder.dimension,
        )

        self._ledger: Dict[str, Dict[str, Any]] = self._load_ledger()

    def _load_ledger(self) -> Dict[str, Dict[str, Any]]:
        if self.ledger_path.exists():
            try:
                with open(self.ledger_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_ledger(self):
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        temp_file = self.ledger_path.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(self._ledger, f, indent=2)
        temp_file.replace(self.ledger_path)

    def store_memory(
        self,
        category: str,
        content: str,
        title: str,
        agent_id: str = "orchestrator",
        tags: Optional[List[str]] = None,
        custom_metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryRecord:
        """Store a verified memory with deduplication and vector indexing."""
        if category not in MEMORY_CATEGORIES:
            raise ValueError(f"Invalid category '{category}'. Must be one of {sorted(MEMORY_CATEGORIES)}")

        content_clean = content.strip()
        c_hash = hashlib.sha256(f"{category}:{content_clean}".encode("utf-8")).hexdigest()

        # Deduplication check
        for m_id, entry in self._ledger.items():
            if entry.get("content_hash") == c_hash:
                # Return existing record to avoid redundant indexing
                return MemoryRecord.from_dict(entry)

        mem_id = f"mem-{uuid.uuid4().hex[:12]}"
        record = MemoryRecord(
            memory_id=mem_id,
            category=category,
            title=title,
            content=content_clean,
            agent_id=agent_id,
            tags=tags or [],
            timestamp=time.time(),
            metadata=custom_metadata or {},
            content_hash=c_hash,
        )

        # Generate embedding
        vec = self.embedder.embed_text(f"{title}\n{content_clean}")

        # Upsert into Qdrant
        payload = record.to_dict()
        payload["text"] = content_clean
        self.qdrant.upsert_points(
            collection_name=self.COLLECTION_NAME,
            points=[{"id": mem_id, "vector": vec, "payload": payload}],
            dimension=self.embedder.dimension,
        )

        # Update ledger
        self._ledger[mem_id] = record.to_dict()
        self._save_ledger()

        return record

    def query_memory(
        self,
        query: str,
        category: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 5,
        min_score: float = 0.20,
    ) -> List[Dict[str, Any]]:
        """Retrieve memories relevant to the query."""
        filter_payload = {}
        if category:
            filter_payload["category"] = category
        if agent_id:
            filter_payload["agent_id"] = agent_id

        query_vec = self.embedder.embed_text(query)
        results = self.qdrant.search_points(
            collection_name=self.COLLECTION_NAME,
            query_vector=query_vec,
            limit=limit,
            filter_payload=filter_payload if filter_payload else None,
            score_threshold=min_score,
        )

        formatted = []
        for r in results:
            payload = r.get("payload", {})
            formatted.append({
                "memory_id": payload.get("memory_id", r["id"]),
                "score": round(r["score"], 4),
                "category": payload.get("category", ""),
                "title": payload.get("title", ""),
                "content": payload.get("content", payload.get("text", "")),
                "agent_id": payload.get("agent_id", ""),
                "tags": payload.get("tags", []),
                "timestamp": payload.get("timestamp", 0),
            })
        return formatted

    def get_memory_by_id(self, memory_id: str) -> Optional[MemoryRecord]:
        """Fetch memory directly from ledger."""
        entry = self._ledger.get(memory_id)
        if entry:
            return MemoryRecord.from_dict(entry)
        return None

    def list_memories(
        self,
        category: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[MemoryRecord]:
        """List stored memories sorted newest first."""
        records = []
        for entry in self._ledger.values():
            if category and entry.get("category") != category:
                continue
            if agent_id and entry.get("agent_id") != agent_id:
                continue
            records.append(MemoryRecord.from_dict(entry))

        records.sort(key=lambda m: m.timestamp, reverse=True)
        return records[:limit]

    def delete_memory(
        self,
        memory_id: str,
        caller_agent_id: str = "orchestrator",
        is_admin: bool = False,
    ) -> bool:
        """Delete memory with authorization validation."""
        entry = self._ledger.get(memory_id)
        if not entry:
            return False

        owner = entry.get("agent_id", "")
        if not is_admin and caller_agent_id != owner and caller_agent_id != "orchestrator":
            raise PermissionError(
                f"Agent '{caller_agent_id}' is not authorized to delete memory owned by '{owner}'."
            )

        # Delete from Qdrant
        self.qdrant.delete_points(self.COLLECTION_NAME, [memory_id])

        # Delete from ledger
        del self._ledger[memory_id]
        self._save_ledger()
        return True

    def get_stats(self) -> Dict[str, Any]:
        """Return memory breakdown across all categories."""
        category_counts = {cat: 0 for cat in MEMORY_CATEGORIES}
        for entry in self._ledger.values():
            cat = entry.get("category")
            if cat in category_counts:
                category_counts[cat] += 1

        return {
            "total_memories": len(self._ledger),
            "by_category": category_counts,
            "ledger_path": str(self.ledger_path),
        }
