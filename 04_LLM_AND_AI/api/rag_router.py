"""
Knowledge Management & RAG REST API for Master AI
=================================================
FastAPI endpoints for document ingestion, hybrid vector/keyword search,
factual multi-lingual Q&A synthesis, and long-term agent memory.
"""

from __future__ import annotations

import importlib
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

# Dynamic imports to preserve folder independence
vdb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.vector_db")
emb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.embeddings")
search_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.search")
ing_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.ingestion")
rag_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.rag_engine")
mem_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.memory")

router = APIRouter(tags=["Knowledge Base & RAG"])

# Shared singleton components
_qdrant_manager = vdb_mod.QdrantManager()
_qdrant_manager.initialize_core_collections(dimension=128)
_embedding_engine = emb_mod.get_embedding_engine("auto", dimension=128)
_dense_search = search_mod.DenseSearchEngine(_qdrant_manager, _embedding_engine)
_bm25_search = search_mod.BM25Engine()
_hybrid_search = search_mod.HybridSearchEngine(_dense_search, _bm25_search)
_ingestion_pipeline = ing_mod.IngestionPipeline(
    qdrant_manager=_qdrant_manager,
    embedding_engine=_embedding_engine,
)
_rag_response_engine = rag_mod.RAGResponseEngine(
    hybrid_search_engine=_hybrid_search,
)
_agent_memory = mem_mod.AgentMemoryManager(
    qdrant_manager=_qdrant_manager,
    embedding_engine=_embedding_engine,
)


# Pydantic Schemas
class FileIngestRequest(BaseModel):
    file_path: str = Field(..., description="Absolute or relative path to file")
    collection_name: str = Field(default="knowledge_docs", description="Target Qdrant collection")
    category: str = Field(default="project_docs", description="Document category")
    force: bool = Field(default=False, description="Force re-indexing even if unchanged")


class RawTextIngestRequest(BaseModel):
    text: str = Field(..., description="Raw text or markdown content")
    title: str = Field(..., description="Document title")
    doc_id: str = Field(..., description="Unique document identifier")
    collection_name: str = Field(default="knowledge_docs")
    category: str = Field(default="adhoc")
    custom_metadata: Dict[str, Any] = Field(default_factory=dict)


class HybridSearchRequest(BaseModel):
    query: str = Field(..., description="Search query string")
    collection_name: str = Field(default="knowledge_docs")
    limit: int = Field(default=5, ge=1, le=50)
    filter_metadata: Optional[Dict[str, Any]] = None


class RAGQueryRequest(BaseModel):
    query: str = Field(..., description="User question (English or Hindi)")
    collection_name: str = Field(default="knowledge_docs")
    limit_chunks: int = Field(default=4, ge=1, le=10)
    target_agent: str = Field(default="research_agent")


class StoreMemoryRequest(BaseModel):
    category: str = Field(..., description="One of the 6 core memory categories")
    title: str = Field(..., description="Short memory title")
    content: str = Field(..., description="Detailed memory content")
    agent_id: str = Field(default="orchestrator", description="Agent author")
    tags: List[str] = Field(default_factory=list)
    custom_metadata: Dict[str, Any] = Field(default_factory=dict)


class QueryMemoryRequest(BaseModel):
    query: str = Field(..., description="Semantic query for memory retrieval")
    category: Optional[str] = None
    agent_id: Optional[str] = None
    limit: int = Field(default=5, ge=1, le=20)


# ==========================================
# RAG & Knowledge Base Endpoints
# ==========================================

@router.get("/api/v1/rag/health")
def rag_health() -> Dict[str, Any]:
    """Retrieve operational status of the Knowledge Base & RAG subsystems."""
    return {
        "status": "healthy",
        "vector_db": _qdrant_manager.health_check(),
        "embedding_engine": _embedding_engine.health_check(),
        "bm25_documents_indexed": _bm25_search.doc_count,
        "manifest_stats": _ingestion_pipeline.manifest.get_stats(),
        "memory_stats": _agent_memory.get_stats(),
    }


@router.get("/api/v1/rag/collections")
def list_collections() -> Dict[str, Any]:
    """List all registered vector collections and metadata."""
    collections = _qdrant_manager.list_collections()
    details = {c: _qdrant_manager.collection_info(c) for c in collections}
    return {
        "total_collections": len(collections),
        "collections": details,
    }


@router.post("/api/v1/rag/ingest/file")
def ingest_file(req: FileIngestRequest) -> Dict[str, Any]:
    """Ingest a file into Qdrant and the BM25 inverted index."""
    try:
        res = _ingestion_pipeline.ingest_file(
            file_path=req.file_path,
            collection_name=req.collection_name,
            category=req.category,
            force=req.force,
        )
        # Also index into BM25 if indexed
        if res.get("status") == "indexed":
            p = res.get("doc_id", req.file_path)
            _bm25_search.add_document(
                doc_id=p,
                text=res.get("title", "") + " " + p,
                metadata={"title": res.get("title", ""), "doc_id": p, "category": req.category},
            )
            _bm25_search.save()
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/rag/ingest/text")
def ingest_text(req: RawTextIngestRequest) -> Dict[str, Any]:
    """Ingest ad-hoc text or research note into the Knowledge Base."""
    try:
        res = _ingestion_pipeline.ingest_raw_text(
            text=req.text,
            title=req.title,
            doc_id=req.doc_id,
            collection_name=req.collection_name,
            category=req.category,
            custom_metadata=req.custom_metadata,
        )
        if res.get("status") == "indexed":
            _bm25_search.add_document(
                doc_id=req.doc_id,
                text=req.title + " " + req.text,
                metadata={"title": req.title, "doc_id": req.doc_id, "category": req.category},
            )
            _bm25_search.save()
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/rag/search/hybrid")
def hybrid_search(req: HybridSearchRequest) -> Dict[str, Any]:
    """Perform hybrid dense/sparse vector search with RRF."""
    try:
        hits = _hybrid_search.search(
            collection_name=req.collection_name,
            query=req.query,
            limit=req.limit,
            filter_metadata=req.filter_metadata,
        )
        return {
            "query": req.query,
            "collection": req.collection_name,
            "total_hits": len(hits),
            "hits": hits,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/rag/query")
def rag_query(req: RAGQueryRequest) -> Dict[str, Any]:
    """Execute factual multi-lingual RAG synthesis with source attribution."""
    try:
        return _rag_response_engine.answer_query(
            query=req.query,
            collection_name=req.collection_name,
            limit_chunks=req.limit_chunks,
            target_agent=req.target_agent,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# Long-Term Agent Memory Endpoints
# ==========================================

@router.post("/api/v1/memory/store")
def store_memory(req: StoreMemoryRequest) -> Dict[str, Any]:
    """Store a verified memory record across one of the 6 categories."""
    try:
        record = _agent_memory.store_memory(
            category=req.category,
            title=req.title,
            content=req.content,
            agent_id=req.agent_id,
            tags=req.tags,
            custom_metadata=req.custom_metadata,
        )
        return {"status": "success", "memory": record.to_dict()}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/memory/query")
def query_memory(req: QueryMemoryRequest) -> Dict[str, Any]:
    """Retrieve memories semantically related to query."""
    try:
        hits = _agent_memory.query_memory(
            query=req.query,
            category=req.category,
            agent_id=req.agent_id,
            limit=req.limit,
        )
        return {"query": req.query, "total_hits": len(hits), "memories": hits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/v1/memory/list")
def list_memories(
    category: Optional[str] = Query(None),
    agent_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
) -> Dict[str, Any]:
    """List chronological memories from the ledger."""
    records = _agent_memory.list_memories(category=category, agent_id=agent_id, limit=limit)
    return {"total": len(records), "memories": [r.to_dict() for r in records]}


@router.delete("/api/v1/memory/{memory_id}")
def delete_memory(
    memory_id: str,
    caller_agent_id: str = Query("orchestrator"),
    is_admin: bool = Query(False),
) -> Dict[str, Any]:
    """Delete a memory record with authorization verification."""
    try:
        deleted = _agent_memory.delete_memory(
            memory_id=memory_id,
            caller_agent_id=caller_agent_id,
            is_admin=is_admin,
        )
        if not deleted:
            raise HTTPException(status_code=404, detail="Memory not found")
        return {"status": "deleted", "memory_id": memory_id}
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/v1/memory/stats")
def memory_stats() -> Dict[str, Any]:
    """Get category distribution of agent memories."""
    return _agent_memory.get_stats()
