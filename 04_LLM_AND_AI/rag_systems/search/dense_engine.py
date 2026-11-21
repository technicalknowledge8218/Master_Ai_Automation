"""
Dense Vector Search Engine for Master AI
========================================
Executes dense semantic similarity search over Qdrant collections.
"""

from typing import List, Dict, Any, Optional


class DenseSearchEngine:
    """Encapsulates embedding generation and Qdrant dense vector query."""

    def __init__(self, qdrant_manager, embedding_engine):
        self.qdrant = qdrant_manager
        self.embedder = embedding_engine

    def search(
        self,
        collection_name: str,
        query: str,
        limit: int = 10,
        filter_payload: Optional[Dict[str, Any]] = None,
        score_threshold: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """Compute query embedding and retrieve nearest neighbors from Qdrant."""
        query_vec = self.embedder.embed_text(query)
        results = self.qdrant.search_points(
            collection_name=collection_name,
            query_vector=query_vec,
            limit=limit,
            filter_payload=filter_payload,
            score_threshold=score_threshold,
        )
        return results
