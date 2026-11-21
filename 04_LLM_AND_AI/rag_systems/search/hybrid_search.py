"""
Hybrid Search Engine with Reciprocal Rank Fusion (RRF) for Master AI
====================================================================
Fuses Dense Semantic Similarity and Sparse BM25 Keyword Search results
to produce resilient, high-precision document and code retrieval.
"""

from typing import List, Dict, Any, Optional
from .bm25_engine import BM25Engine
from .dense_engine import DenseSearchEngine


class HybridSearchEngine:
    """Combines dense vector retrieval and sparse BM25 retrieval using RRF."""

    def __init__(
        self,
        dense_engine: DenseSearchEngine,
        bm25_engine: BM25Engine,
        rrf_k: int = 60,
        dense_weight: float = 0.5,
        bm25_weight: float = 0.5,
        dense_score_threshold: float = 0.20,
    ):
        self.dense = dense_engine
        self.bm25 = bm25_engine
        self.rrf_k = rrf_k
        self.dense_weight = dense_weight
        self.bm25_weight = bm25_weight
        self.dense_score_threshold = dense_score_threshold

    def search(
        self,
        collection_name: str,
        query: str,
        limit: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None,
        candidate_multiplier: int = 4,
    ) -> List[Dict[str, Any]]:
        """
        Execute hybrid search over the designated collection.
        Fetches candidates from dense and BM25 systems and merges via RRF.
        """
        fetch_k = max(limit * candidate_multiplier, 20)

        # 1. Fetch dense candidates
        raw_dense = self.dense.search(
            collection_name=collection_name,
            query=query,
            limit=fetch_k,
            filter_payload=filter_metadata,
        )
        dense_candidates = [
            d for d in raw_dense if d.get("score", 0.0) >= self.dense_score_threshold
        ]

        # 2. Fetch BM25 candidates
        bm25_candidates = self.bm25.search(
            query=query,
            limit=fetch_k,
            filter_metadata=filter_metadata,
        )

        # 3. Fuse via Reciprocal Rank Fusion (RRF)
        # RRF_Score = sum(weight / (k + rank))
        scores: Dict[str, float] = {}
        dense_ranks: Dict[str, int] = {}
        dense_scores: Dict[str, float] = {}
        bm25_ranks: Dict[str, int] = {}
        bm25_scores: Dict[str, float] = {}
        doc_payloads: Dict[str, Dict[str, Any]] = {}
        matched_keywords: Dict[str, List[str]] = {}

        for rank, item in enumerate(dense_candidates, start=1):
            doc_id = str(item.get("payload", {}).get("custom_id", item["id"]))
            dense_ranks[doc_id] = rank
            dense_scores[doc_id] = item["score"]
            doc_payloads[doc_id] = item.get("payload", {})
            contribution = self.dense_weight / (self.rrf_k + rank)
            scores[doc_id] = scores.get(doc_id, 0.0) + contribution

        for rank, item in enumerate(bm25_candidates, start=1):
            doc_id = str(item.get("payload", {}).get("custom_id", item["id"]))
            bm25_ranks[doc_id] = rank
            bm25_scores[doc_id] = item["score"]
            matched_keywords[doc_id] = item.get("matched_terms", [])
            if doc_id not in doc_payloads:
                doc_payloads[doc_id] = item.get("payload", {})
            contribution = self.bm25_weight / (self.rrf_k + rank)
            scores[doc_id] = scores.get(doc_id, 0.0) + contribution

        # Sort by composite RRF score
        sorted_hits = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]

        # Normalize RRF scores relative to max possible single-item score
        max_possible_rrf = (self.dense_weight / (self.rrf_k + 1)) + (self.bm25_weight / (self.rrf_k + 1))

        results = []
        for doc_id, rrf_score in sorted_hits:
            payload = doc_payloads.get(doc_id, {})
            norm_score = min(1.0, rrf_score / max_possible_rrf) if max_possible_rrf > 0 else 0.0

            results.append({
                "id": doc_id,
                "score": round(norm_score, 4),
                "rrf_raw": round(rrf_score, 6),
                "dense_score": dense_scores.get(doc_id),
                "dense_rank": dense_ranks.get(doc_id),
                "bm25_score": bm25_scores.get(doc_id),
                "bm25_rank": bm25_ranks.get(doc_id),
                "matched_keywords": matched_keywords.get(doc_id, []),
                "title": payload.get("title", ""),
                "heading": payload.get("heading", ""),
                "text": payload.get("text", ""),
                "source_path": payload.get("source_path", ""),
                "category": payload.get("category", ""),
                "chunk_index": payload.get("chunk_index", 0),
                "payload": payload,
            })

        return results
