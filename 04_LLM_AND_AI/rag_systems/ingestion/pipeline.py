"""
Master Ingestion Pipeline for Master AI RAG
===========================================
Orchestrates loading, secret exclusion, semantic chunking, deduplication,
embedding generation, and vector database upsert.
"""

import os
import time
import importlib
from pathlib import Path
from typing import Dict, Any, List, Optional

from .secret_filter import SecretFilter
from .document_loader import DocumentLoader, LoadedDocument
from .chunker import DocumentChunker, DocumentChunk
from .deduplicator import DeduplicationManifest, compute_sha256


class IngestionPipeline:
    """Comprehensive pipeline for indexing knowledge into Master AI RAG."""

    def __init__(
        self,
        qdrant_manager=None,
        embedding_engine=None,
        manifest_path: Optional[str] = None,
        target_chunk_size: int = 800,
        chunk_overlap: int = 100,
    ):
        # Resolve dependencies lazily if not injected
        if qdrant_manager is None:
            vdb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.vector_db")
            self.qdrant = vdb_mod.QdrantManager()
        else:
            self.qdrant = qdrant_manager

        if embedding_engine is None:
            emb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.embeddings")
            self.embedder = emb_mod.get_embedding_engine("auto")
        else:
            self.embedder = embedding_engine

        self.manifest = DeduplicationManifest(manifest_path)
        self.chunker = DocumentChunker(
            target_chunk_size=target_chunk_size, chunk_overlap=chunk_overlap
        )

    def ingest_file(
        self,
        file_path: str | Path,
        collection_name: str = "knowledge_docs",
        category: str = "project_docs",
        force: bool = False,
        base_dir: Optional[str | Path] = None,
    ) -> Dict[str, Any]:
        """Ingest a single file through the pipeline."""
        p = Path(file_path).resolve()
        allowed, reason = SecretFilter.is_path_allowed(p)
        if not allowed:
            return {
                "status": "excluded",
                "file_path": str(p),
                "reason": reason,
                "chunks_indexed": 0,
            }

        if not DocumentLoader.can_load(p):
            return {
                "status": "unsupported_format",
                "file_path": str(p),
                "chunks_indexed": 0,
            }

        loaded_doc = DocumentLoader.load_file(p, base_dir=base_dir)
        sanitized_content, was_redacted = SecretFilter.sanitize_content(loaded_doc.content)
        content_hash = compute_sha256(sanitized_content)

        if not force and self.manifest.is_document_unchanged(loaded_doc.doc_id, content_hash):
            return {
                "status": "unchanged",
                "doc_id": loaded_doc.doc_id,
                "file_path": str(p),
                "sha256": content_hash,
                "chunks_indexed": 0,
            }

        # Purge previous points if updating
        old_point_ids = self.manifest.get_document_point_ids(loaded_doc.doc_id)
        if old_point_ids:
            self.qdrant.delete_points(collection_name, old_point_ids)

        # Chunk document
        base_meta = dict(loaded_doc.metadata)
        base_meta.update({
            "doc_id": loaded_doc.doc_id,
            "title": loaded_doc.title,
            "category": category,
            "source_path": str(p),
            "was_redacted": was_redacted,
            "ingested_at": time.time(),
        })

        chunks = self.chunker.chunk_document(
            content=sanitized_content,
            doc_type=loaded_doc.doc_type,
            base_metadata=base_meta,
        )

        if not chunks:
            return {
                "status": "empty",
                "doc_id": loaded_doc.doc_id,
                "file_path": str(p),
                "chunks_indexed": 0,
            }

        # Embed all chunks
        chunk_texts = [c.text for c in chunks]
        vectors = self.embedder.embed_batch(chunk_texts)

        # Build points
        points = []
        point_ids = []
        for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
            c_hash = compute_sha256(chunk.text)
            pt_id = f"{loaded_doc.doc_id}#chunk-{i}"
            point_ids.append(pt_id)
            payload = dict(chunk.metadata)
            payload.update({
                "text": chunk.text,
                "chunk_index": chunk.chunk_index,
                "total_chunks": chunk.total_chunks,
                "heading": chunk.heading,
                "chunk_hash": c_hash,
            })
            points.append({
                "id": pt_id,
                "vector": vec,
                "payload": payload,
            })
            self.manifest.register_chunk(c_hash, pt_id)

        # Upsert into Qdrant
        self.qdrant.upsert_points(
            collection_name=collection_name,
            points=points,
            dimension=self.embedder.dimension,
        )

        # Update manifest
        self.manifest.record_document_ingested(
            doc_id=loaded_doc.doc_id,
            file_path=str(p),
            sha256_hash=content_hash,
            collection_name=collection_name,
            point_ids=point_ids,
            chunk_count=len(points),
        )

        return {
            "status": "indexed",
            "doc_id": loaded_doc.doc_id,
            "title": loaded_doc.title,
            "chunks_indexed": len(points),
            "sha256": content_hash,
            "collection": collection_name,
            "was_redacted": was_redacted,
        }

    def ingest_directory(
        self,
        dir_path: str | Path,
        collection_name: str = "knowledge_docs",
        category: str = "project_docs",
        glob_pattern: str = "*",
        recursive: bool = True,
        force: bool = False,
    ) -> Dict[str, Any]:
        """Ingest all matching documents in a directory tree."""
        target_dir = Path(dir_path).resolve()
        if not target_dir.is_dir():
            raise NotADirectoryError(f"Directory not found: {target_dir}")

        files = (
            target_dir.rglob(glob_pattern)
            if recursive
            else target_dir.glob(glob_pattern)
        )

        summary = {
            "directory": str(target_dir),
            "indexed": 0,
            "unchanged": 0,
            "excluded": 0,
            "unsupported": 0,
            "errors": 0,
            "total_chunks": 0,
            "details": [],
        }

        for f in files:
            if not f.is_file():
                continue
            try:
                res = self.ingest_file(
                    file_path=f,
                    collection_name=collection_name,
                    category=category,
                    force=force,
                    base_dir=target_dir,
                )
                status = res.get("status")
                if status == "indexed":
                    summary["indexed"] += 1
                    summary["total_chunks"] += res.get("chunks_indexed", 0)
                elif status == "unchanged":
                    summary["unchanged"] += 1
                elif status == "excluded":
                    summary["excluded"] += 1
                elif status == "unsupported_format":
                    summary["unsupported"] += 1
                summary["details"].append(res)
            except Exception as e:
                summary["errors"] += 1
                summary["details"].append({
                    "status": "error",
                    "file_path": str(f),
                    "error": str(e),
                })

        return summary

    def ingest_raw_text(
        self,
        text: str,
        title: str,
        doc_id: str,
        collection_name: str = "knowledge_docs",
        category: str = "adhoc",
        custom_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Ingest an ad-hoc text snippet directly without a backing file."""
        sanitized_content, was_redacted = SecretFilter.sanitize_content(text)
        content_hash = compute_sha256(sanitized_content)

        base_meta = dict(custom_metadata or {})
        base_meta.update({
            "doc_id": doc_id,
            "title": title,
            "category": category,
            "source_path": f"memory://{doc_id}",
            "was_redacted": was_redacted,
            "ingested_at": time.time(),
        })

        chunks = self.chunker.chunk_document(
            content=sanitized_content,
            doc_type="markdown",
            base_metadata=base_meta,
        )

        if not chunks:
            return {"status": "empty", "doc_id": doc_id, "chunks_indexed": 0}

        chunk_texts = [c.text for c in chunks]
        vectors = self.embedder.embed_batch(chunk_texts)

        points = []
        point_ids = []
        for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
            c_hash = compute_sha256(chunk.text)
            pt_id = f"{doc_id}#chunk-{i}"
            point_ids.append(pt_id)
            payload = dict(chunk.metadata)
            payload.update({
                "text": chunk.text,
                "chunk_index": chunk.chunk_index,
                "total_chunks": chunk.total_chunks,
                "heading": chunk.heading,
                "chunk_hash": c_hash,
            })
            points.append({
                "id": pt_id,
                "vector": vec,
                "payload": payload,
            })

        self.qdrant.upsert_points(
            collection_name=collection_name,
            points=points,
            dimension=self.embedder.dimension,
        )

        return {
            "status": "indexed",
            "doc_id": doc_id,
            "title": title,
            "chunks_indexed": len(points),
            "sha256": content_hash,
            "collection": collection_name,
            "was_redacted": was_redacted,
        }
