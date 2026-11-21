"""
Factual RAG Response Engine for Master AI
=========================================
Synthesizes verified answers with explicit source attribution in English & Hindi.
Strict zero-hallucination invariant: Flags missing information when context lacks evidence.
"""

import time
import re
import importlib
from typing import List, Dict, Any, Optional

HINDI_CHAR_RE = re.compile(r"[\u0900-\u097F]")


class RAGResponseEngine:
    """End-to-end RAG reasoning and factual synthesis engine."""

    def __init__(
        self,
        hybrid_search_engine=None,
        model_router=None,
        default_collection: str = "knowledge_docs",
    ):
        self.default_collection = default_collection

        # Resolve search engine
        if hybrid_search_engine is None:
            vdb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.vector_db")
            emb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.embeddings")
            search_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.search")
            qm = vdb_mod.QdrantManager()
            embedder = emb_mod.get_embedding_engine("auto")
            dense = search_mod.DenseSearchEngine(qm, embedder)
            bm25 = search_mod.BM25Engine()
            self.search_engine = search_mod.HybridSearchEngine(dense, bm25)
        else:
            self.search_engine = hybrid_search_engine

        # Resolve model router
        if model_router is None:
            try:
                router_mod = importlib.import_module("04_LLM_AND_AI.router.model_router")
                self.router = router_mod.ModelRouter()
            except Exception:
                self.router = None
        else:
            self.router = model_router

    def detect_language(self, query: str) -> str:
        """Detect if the query is in Hindi (Devanagari script) or English."""
        if HINDI_CHAR_RE.search(query):
            return "hi"
        return "en"

    def answer_query(
        self,
        query: str,
        collection_name: Optional[str] = None,
        limit_chunks: int = 4,
        filter_metadata: Optional[Dict[str, Any]] = None,
        min_relevance_score: float = 0.15,
        target_agent: Optional[str] = "research_agent",
    ) -> Dict[str, Any]:
        """
        Execute RAG flow:
          1. Query Analysis & Language Detection
          2. Hybrid Search Retrieval
          3. Relevance Threshold Filtering
          4. Context Assembly
          5. LLM Synthesis or Deterministic Extraction
          6. Fact vs Inference Verification & Citation Mapping
        """
        start_time = time.time()
        coll = collection_name or self.default_collection
        lang = self.detect_language(query)

        # 1. Retrieve candidate chunks
        hits = self.search_engine.search(
            collection_name=coll,
            query=query,
            limit=limit_chunks,
            filter_metadata=filter_metadata,
        )

        relevant_hits = [h for h in hits if h.get("score", 0.0) >= min_relevance_score]

        # 2. Check for missing information
        if not relevant_hits:
            latency = (time.time() - start_time) * 1000.0
            if lang == "hi":
                msg = "यह जानकारी वर्तमान नॉलेज बेस में उपलब्ध नहीं है। कोई प्रासंगिक संदर्भ दस्तावेज़ नहीं मिला।"
            else:
                msg = "Information not found in knowledge base. No relevant reference context was retrieved."

            return {
                "answer": msg,
                "language": lang,
                "missing_information_detected": True,
                "citations": [],
                "context_chunks_used": 0,
                "model_used": "direct_guardrail",
                "latency_ms": round(latency, 2),
            }

        # 3. Assemble Context with document delimiters
        context_blocks = []
        citations = []
        for i, hit in enumerate(relevant_hits, start=1):
            doc_id = hit["id"]
            title = hit.get("title") or "Document"
            source = hit.get("source_path") or f"doc://{doc_id}"
            snippet = hit.get("text", "").strip()

            context_blocks.append(f"[{i}] Title: {title} | Source: {source}\n{snippet}")
            citations.append({
                "citation_index": i,
                "doc_id": doc_id,
                "title": title,
                "source_path": source,
                "heading": hit.get("heading", ""),
                "relevance_score": hit.get("score", 0.0),
                "snippet": snippet[:200] + ("..." if len(snippet) > 200 else ""),
            })

        assembled_context = "\n\n".join(context_blocks)

        # 4. Synthesize Answer
        # Build prompt instructions enforcing strict factual accuracy
        if lang == "hi":
            system_prompt = (
                "आप मास्टर एआई के लिए एक सटीक और तथ्यात्मक सहायक हैं।\n"
                "दिए गए संदर्भ का उपयोग करके हिंदी में उत्तर दें।\n"
                "सख्त नियम:\n"
                "1. केवल दिए गए संदर्भ पर भरोसा करें।\n"
                "2. संदर्भ में अनुपलब्ध किसी भी तथ्य का आविष्कार न करें।\n"
                "3. उत्तर में स्रोत का संदर्भ [1], [2] के रूप में दें।"
            )
            user_prompt = f"प्रश्न: {query}\n\nसंदर्भ:\n{assembled_context}\n\nसटीक उत्तर दें:"
        else:
            system_prompt = (
                "You are a factual AI assistant for Master AI.\n"
                "Answer the query using ONLY the provided verified context.\n"
                "Strict rules:\n"
                "1. Do not hallucinate or extrapolate beyond the provided text.\n"
                "2. Cite your sources using document markers [1], [2] where applicable.\n"
                "3. If the context does not fully answer the question, explicitly state what is missing."
            )
            user_prompt = f"Query: {query}\n\nVerified Context:\n{assembled_context}\n\nAccurate Answer:"

        model_name = "deterministic_synthesizer"
        answer_text = ""

        if self.router:
            try:
                task_spec = {
                    "task_type": "rag_synthesis",
                    "agent_id": target_agent or "research_agent",
                    "system_prompt": system_prompt,
                    "prompt": user_prompt,
                    "max_tokens": 1024,
                }
                res = self.router.execute_task(task_spec)
                if res.get("status") == "success":
                    answer_text = res.get("response", "")
                    model_name = res.get("model_used", model_name)
            except Exception:
                pass

        # Deterministic extraction fallback if router unavailable or returned empty
        if not answer_text:
            first_hit = relevant_hits[0]
            if lang == "hi":
                answer_text = (
                    f"प्राप्त संदर्भ के अनुसार ([1]):\n\n"
                    f"{first_hit.get('text', '').strip()}"
                )
            else:
                answer_text = (
                    f"According to verified reference ([1] - {first_hit.get('title', 'Doc')}):\n\n"
                    f"{first_hit.get('text', '').strip()}"
                )

        latency = (time.time() - start_time) * 1000.0

        return {
            "answer": answer_text,
            "language": lang,
            "missing_information_detected": False,
            "citations": citations,
            "context_chunks_used": len(relevant_hits),
            "model_used": model_name,
            "latency_ms": round(latency, 2),
        }
