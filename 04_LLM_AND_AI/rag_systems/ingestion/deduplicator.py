"""
Deduplicator & Manifest Tracking for Master AI RAG
===================================================
Tracks document hashes, chunk signatures, and Qdrant point IDs to support
incremental ingestion and eliminate redundant vector calculations.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List


def compute_sha256(content: str | bytes) -> str:
    """Compute SHA-256 hash of text or bytes."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


class DeduplicationManifest:
    """Persistent ledger of ingested files, SHA-256 hashes, and vector IDs."""

    def __init__(self, manifest_path: Optional[Path | str] = None):
        if manifest_path is None:
            self.manifest_path = Path(__file__).resolve().parent / "INGESTION_MANIFEST.json"
        else:
            self.manifest_path = Path(manifest_path)

        self._data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {"documents": {}, "chunks": {}}
        return {"documents": {}, "chunks": {}}

    def save(self):
        """Persist manifest atomically."""
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.manifest_path.with_suffix(".tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)
        temp_path.replace(self.manifest_path)

    def is_document_unchanged(self, doc_id: str, current_hash: str) -> bool:
        """Return True if doc has already been ingested with the same content hash."""
        entry = self._data.get("documents", {}).get(doc_id)
        if not entry:
            return False
        return entry.get("sha256") == current_hash

    def get_document_point_ids(self, doc_id: str) -> List[str]:
        """Return point IDs associated with previously ingested document."""
        entry = self._data.get("documents", {}).get(doc_id)
        if entry:
            return entry.get("point_ids", [])
        return []

    def record_document_ingested(
        self,
        doc_id: str,
        file_path: str,
        sha256_hash: str,
        collection_name: str,
        point_ids: List[str],
        chunk_count: int,
    ):
        """Record newly or updated indexed document."""
        if "documents" not in self._data:
            self._data["documents"] = {}

        self._data["documents"][doc_id] = {
            "file_path": file_path,
            "sha256": sha256_hash,
            "collection_name": collection_name,
            "point_ids": point_ids,
            "chunk_count": chunk_count,
            "updated_at": None,
        }
        self.save()

    def is_chunk_duplicate(self, chunk_hash: str) -> bool:
        """Check if identical chunk text has already been registered."""
        return chunk_hash in self._data.get("chunks", {})

    def register_chunk(self, chunk_hash: str, point_id: str):
        """Record chunk hash to point ID mapping."""
        if "chunks" not in self._data:
            self._data["chunks"] = {}
        self._data["chunks"][chunk_hash] = point_id

    def remove_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Remove document record from manifest and return previous metadata."""
        if doc_id in self._data.get("documents", {}):
            doc = self._data["documents"].pop(doc_id)
            self.save()
            return doc
        return None

    def get_stats(self) -> Dict[str, Any]:
        """Summary metrics."""
        return {
            "total_documents_indexed": len(self._data.get("documents", {})),
            "total_unique_chunks": len(self._data.get("chunks", {})),
            "manifest_file": str(self.manifest_path),
        }
