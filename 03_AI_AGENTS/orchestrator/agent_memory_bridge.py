"""
Agent Knowledge & Memory Bridge for Master AI
=============================================
Provides a unified interface for all 7 specialist agents to query the persistent
Knowledge Base, search code/architecture docs, and store/recall long-term memories.
"""

from __future__ import annotations

import importlib
from typing import List, Dict, Any, Optional


class AgentMemoryBridge:
    """Inter-agent memory and knowledge retrieval gateway."""

    def __init__(self, in_memory: bool = False):
        vdb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.vector_db")
        emb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.embeddings")
        search_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.search")
        rag_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.rag_engine")
        mem_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.memory")

        self.qdrant = vdb_mod.QdrantManager(in_memory=in_memory)
        self.qdrant.initialize_core_collections(dimension=128)
        self.embedder = emb_mod.get_embedding_engine("auto", dimension=128)
        self.dense = search_mod.DenseSearchEngine(self.qdrant, self.embedder)
        self.bm25 = search_mod.BM25Engine()
        self.hybrid = search_mod.HybridSearchEngine(self.dense, self.bm25)
        self.rag = rag_mod.RAGResponseEngine(hybrid_search_engine=self.hybrid)
        self.memory = mem_mod.AgentMemoryManager(
            qdrant_manager=self.qdrant,
            embedding_engine=self.embedder,
        )

    # -------------------------------------------------------------
    # General Knowledge & RAG Operations
    # -------------------------------------------------------------

    def retrieve_context(
        self,
        query: str,
        collection_name: str = "knowledge_docs",
        limit: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Hybrid search across Master AI knowledge collections."""
        return self.hybrid.search(
            collection_name=collection_name,
            query=query,
            limit=limit,
            filter_metadata=filter_metadata,
        )

    def ask_knowledge_base(
        self,
        query: str,
        agent_id: str = "research_agent",
        limit_chunks: int = 4,
    ) -> Dict[str, Any]:
        """Perform verified, citation-backed factual question answering."""
        return self.rag.answer_query(
            query=query,
            target_agent=agent_id,
            limit_chunks=limit_chunks,
        )

    # -------------------------------------------------------------
    # Long-Term Memory Operations
    # -------------------------------------------------------------

    def record_memory(
        self,
        agent_id: str,
        category: str,
        title: str,
        content: str,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Persist a discrete memory into long-term memory."""
        record = self.memory.store_memory(
            category=category,
            title=title,
            content=content,
            agent_id=agent_id,
            tags=tags or [],
            custom_metadata=metadata or {},
        )
        return record.to_dict()

    def recall_memories(
        self,
        query: str,
        category: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """Retrieve memories matching query and optional category/agent filter."""
        return self.memory.query_memory(
            query=query,
            category=category,
            agent_id=agent_id,
            limit=limit,
        )

    # -------------------------------------------------------------
    # Role-Specific Convenience Methods
    # -------------------------------------------------------------

    def record_technical_decision(
        self,
        title: str,
        decision_content: str,
        agent_id: str = "software_architect",
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Record an Architecture Decision Record (ADR)."""
        tags = list(set((tags or []) + ["adr", "architecture"]))
        return self.record_memory(
            agent_id=agent_id,
            category="technical_decisions",
            title=title,
            content=decision_content,
            tags=tags,
        )

    def record_reusable_solution(
        self,
        title: str,
        solution_code_or_fix: str,
        agent_id: str = "coding_agent",
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Record an engineering solution or bug fix pattern."""
        tags = list(set((tags or []) + ["solution", "code_fix"]))
        return self.record_memory(
            agent_id=agent_id,
            category="reusable_solutions",
            title=title,
            content=solution_code_or_fix,
            tags=tags,
        )

    def record_task_history(
        self,
        task_id: str,
        summary: str,
        agent_id: str,
        status: str = "completed",
    ) -> Dict[str, Any]:
        """Record execution outcome into task history."""
        return self.record_memory(
            agent_id=agent_id,
            category="task_history",
            title=f"Task: {task_id} ({status})",
            content=summary,
            tags=["task_run", status],
            metadata={"task_id": task_id, "status": status},
        )
