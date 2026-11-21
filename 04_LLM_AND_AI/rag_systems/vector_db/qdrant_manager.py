"""
Persistent Qdrant Vector Database Manager for Master AI
=======================================================
Manages local embedded Qdrant database collections, upserts, vector searches,
and persistence verification across process restarts.
"""

import os
import sys
import uuid
import atexit
import importlib
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import (
        VectorParams,
        Distance,
        PointStruct,
        Filter,
        FieldCondition,
        MatchValue,
    )
except ImportError:
    QdrantClient = None


def _ensure_valid_point_id(raw_id: Any) -> str:
    """Ensure point ID conforms to Qdrant requirements (integer or valid UUID)."""
    if raw_id is None:
        return str(uuid.uuid4())
    if isinstance(raw_id, int):
        return raw_id
    id_str = str(raw_id)
    try:
        # Check if already a valid UUID
        uuid.UUID(id_str)
        return id_str
    except (ValueError, AttributeError):
        # Convert arbitrary string to deterministic UUIDv5
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, id_str))


def _get_default_db_path() -> Path:
    """Resolve default persistent storage directory for Qdrant."""
    try:
        path_mod = importlib.import_module("00_CORE_SYSTEM.config.path_config")
        root = path_mod.get_project_root()
    except Exception:
        root = Path(__file__).resolve().parent.parent.parent.parent
    db_dir = root / "04_LLM_AND_AI" / "rag_systems" / "qdrant_db"
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir


class QdrantManager:
    """
    Manages embedded Qdrant vector database storage.
    Supports file-backed persistence or in-memory mode.
    """

    CORE_COLLECTIONS = [
        "knowledge_docs",
        "skills_registry",
        "agent_memory",
        "codebase_index",
        "github_research",
    ]

    _CLIENT_CACHE: Dict[str, Any] = {}

    def __init__(self, db_path: Optional[str] = None, in_memory: bool = False):
        if QdrantClient is None:
            raise RuntimeError("qdrant-client package is required but not installed.")

        self._in_memory = in_memory
        if in_memory:
            self._storage_path = None
            self._client = QdrantClient(":memory:")
        else:
            if db_path:
                self._storage_path = Path(db_path)
            else:
                self._storage_path = _get_default_db_path()
            self._storage_path.mkdir(parents=True, exist_ok=True)
            self._client = self._init_persistent_client(self._storage_path)

        atexit.register(self.close)

    def _init_persistent_client(self, path: Path) -> QdrantClient:
        """Initialize client with lock protection and process-level handle reuse."""
        cache_key = str(path.resolve())
        if cache_key in self._CLIENT_CACHE:
            return self._CLIENT_CACHE[cache_key]

        try:
            client = QdrantClient(path=str(path))
            self._CLIENT_CACHE[cache_key] = client
            return client
        except Exception as e:
            # Check for stale lock if previous process crashed
            lock_file = path / ".lock"
            if lock_file.exists() and "lock" in str(e).lower():
                try:
                    lock_file.unlink()
                    client = QdrantClient(path=str(path))
                    self._CLIENT_CACHE[cache_key] = client
                    return client
                except Exception:
                    pass
            raise RuntimeError(f"Failed to open Qdrant database at {path}: {e}")

    @property
    def storage_path(self) -> Optional[Path]:
        return self._storage_path

    @property
    def is_in_memory(self) -> bool:
        return self._in_memory

    def ensure_collection(
        self,
        collection_name: str,
        dimension: int = 128,
        distance: str = "Cosine",
    ) -> bool:
        """Create collection if it does not exist."""
        existing = [c.name for c in self._client.get_collections().collections]
        if collection_name in existing:
            return False

        dist_enum = Distance.COSINE
        if distance.upper() == "EUCLID":
            dist_enum = Distance.EUCLID
        elif distance.upper() == "DOT":
            dist_enum = Distance.DOT

        self._client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dimension, distance=dist_enum),
        )
        return True

    def initialize_core_collections(self, dimension: int = 128) -> Dict[str, str]:
        """Ensure all standard Master AI collections exist."""
        results = {}
        for coll in self.CORE_COLLECTIONS:
            created = self.ensure_collection(coll, dimension=dimension)
            results[coll] = "created" if created else "already_exists"
        return results

    def list_collections(self) -> List[str]:
        """List all collection names."""
        return [c.name for c in self._client.get_collections().collections]

    def collection_info(self, collection_name: str) -> Dict[str, Any]:
        """Get collection metrics and vector count."""
        info = self._client.get_collection(collection_name=collection_name)
        return {
            "name": collection_name,
            "points_count": getattr(info, "points_count", 0),
            "status": getattr(info, "status", "unknown"),
            "vectors_count": getattr(info, "vectors_count", 0),
        }

    def upsert_points(
        self,
        collection_name: str,
        points: List[Dict[str, Any]],
        dimension: int = 128,
    ) -> int:
        """
        Upsert a list of dict points.
        Each item must contain:
          - 'vector': list of floats
          - 'payload': dict of metadata
          - 'id': (optional int or UUID string)
        """
        if not points:
            return 0

        self.ensure_collection(collection_name, dimension=dimension)

        structs = []
        for p in points:
            raw_id = p.get("id")
            norm_id = _ensure_valid_point_id(raw_id)
            payload = dict(p.get("payload", {}))
            if raw_id is not None and "custom_id" not in payload:
                payload["custom_id"] = str(raw_id)

            structs.append(
                PointStruct(
                    id=norm_id,
                    vector=p["vector"],
                    payload=payload,
                )
            )

        self._client.upsert(collection_name=collection_name, points=structs)
        return len(structs)

    def search_points(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 5,
        filter_payload: Optional[Dict[str, Any]] = None,
        score_threshold: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """Dense cosine similarity vector search."""
        if collection_name not in self.list_collections():
            return []

        q_filter = None
        if filter_payload:
            must_clauses = [
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in filter_payload.items()
            ]
            q_filter = Filter(must=must_clauses)

        results = self._client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            query_filter=q_filter,
            score_threshold=score_threshold,
        )

        formatted = []
        for r in results.points:
            formatted.append({
                "id": r.id,
                "score": float(r.score),
                "payload": r.payload or {},
            })
        return formatted

    def delete_points(self, collection_name: str, point_ids: List[Any]) -> bool:
        """Delete specific points from a collection."""
        if collection_name not in self.list_collections():
            return False
        from qdrant_client.models import PointIdsList
        norm_ids = [_ensure_valid_point_id(pid) for pid in point_ids]
        self._client.delete(
            collection_name=collection_name,
            points_selector=PointIdsList(points=norm_ids),
        )
        return True

    def delete_collection(self, collection_name: str) -> bool:
        """Delete an entire collection."""
        if collection_name in self.list_collections():
            self._client.delete_collection(collection_name=collection_name)
            return True
        return False

    def health_check(self) -> Dict[str, Any]:
        """Verify vector database connectivity and collection stats."""
        try:
            collections = self.list_collections()
            stats = {c: self.collection_info(c) for c in collections}
            return {
                "status": "healthy",
                "in_memory": self._in_memory,
                "storage_path": str(self._storage_path) if self._storage_path else ":memory:",
                "total_collections": len(collections),
                "collections": stats,
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "storage_path": str(self._storage_path) if self._storage_path else ":memory:",
            }

    def close(self):
        """Cleanly close database client handle."""
        if self._storage_path:
            cache_key = str(self._storage_path.resolve())
            if cache_key in self._CLIENT_CACHE:
                del self._CLIENT_CACHE[cache_key]

        if self._client is not None:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None
