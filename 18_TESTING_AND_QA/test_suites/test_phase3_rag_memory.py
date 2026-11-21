"""
Automated Test Suite for MASTER AI — Phase 3: RAG, Knowledge Base & Long-Term Memory
====================================================================================
Validates all Phase 3 deliverables:
  1. Offline deterministic mock embeddings
  2. Ollama local embedding health checks
  3. Cloud embedding gated by SecurityBoundary (zero-paid API invariant)
  4. Qdrant persistent storage & cross-restart verification
  5. Secret filtering and exclusion of credentials
  6. Semantic chunking with heading awareness
  7. Deduplication manifest & incremental ingestion
  8. Pure-Python Okapi BM25 keyword ranker
  9. Hybrid Search with Reciprocal Rank Fusion (RRF)
  10. Factual RAG Q&A with Hindi/English support & missing info detection
  11. 6-category persistent Agent Memory & authorization enforcement
  12. FastAPI Knowledge & Memory REST endpoints
"""

import sys
import unittest
import importlib
import tempfile
import shutil
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

vdb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.vector_db")
emb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.embeddings")
ing_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.ingestion")
search_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.search")
rag_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.rag_engine")
mem_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.memory")
api_main_mod = importlib.import_module("00_CORE_SYSTEM.api.main")


class TestPhase3RAGAndMemory(unittest.TestCase):
    """Phase 3 Comprehensive Verification Suite."""

    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path(tempfile.mkdtemp(prefix="master_ai_phase3_test_"))

    @classmethod
    def tearDownClass(cls):
        if cls.test_dir.exists():
            shutil.rmtree(cls.test_dir, ignore_errors=True)

    def test_01_offline_mock_embedding_deterministic(self):
        """Verify mock embeddings are repeatable, normalized, and semantically oriented."""
        engine = emb_mod.OfflineMockEmbeddingEngine(dimension=128)
        self.assertEqual(engine.dimension, 128)
        self.assertTrue(engine.is_mock)

        text_a = "Master AI autonomous operating system architecture"
        text_b = "Master AI autonomous system and software architecture"
        text_c = "Delicious Italian pizza recipe with mozzarella and tomato"

        vec_a1 = engine.embed_text(text_a)
        vec_a2 = engine.embed_text(text_a)

        # Exact determinism
        self.assertEqual(vec_a1, vec_a2)
        self.assertEqual(len(vec_a1), 128)

        # L2 normalization (sum of squares == 1.0)
        norm_sq = sum(x * x for x in vec_a1)
        self.assertAlmostEqual(norm_sq, 1.0, places=4)

        # Semantic cosine similarity: related vs unrelated
        vec_b = engine.embed_text(text_b)
        vec_c = engine.embed_text(text_c)

        sim_ab = sum(a * b for a, b in zip(vec_a1, vec_b))
        sim_ac = sum(a * c for a, c in zip(vec_a1, vec_c))

        self.assertGreater(sim_ab, 0.65, "Semantically close texts must have high similarity")
        self.assertGreater(sim_ab, sim_ac, "Related texts must score higher than unrelated texts")

    def test_02_ollama_embedding_engine_health(self):
        """Verify Ollama embedding engine health check and graceful standby reporting."""
        engine = emb_mod.OllamaEmbeddingEngine(model_name="nomic-embed-text")
        health = engine.health_check()
        self.assertIn("status", health)
        self.assertIn("model_name", health)
        self.assertEqual(health["model_name"], "nomic-embed-text")

    def test_03_cloud_embedding_gated_by_security_boundary(self):
        """Verify cloud embeddings raise PermissionError when zero-paid policy is active."""
        cloud_engine = emb_mod.CloudEmbeddingEngine(
            model_name="text-embedding-3-small",
            user_explicit_approval=False,
        )
        health = cloud_engine.health_check()
        self.assertFalse(health["can_invoke"])

        with self.assertRaises(PermissionError):
            cloud_engine.embed_text("This should be blocked by zero-paid policy")

    def test_04_qdrant_persistent_storage_across_restarts(self):
        """Verify Qdrant data persists to disk across independent client instances."""
        db_path = self.test_dir / "qdrant_persist_test"
        qm1 = vdb_mod.QdrantManager(db_path=str(db_path))
        qm1.ensure_collection("persist_test", dimension=128)

        test_points = [
            {
                "id": "persist-doc-001",
                "vector": [0.05] * 128,
                "payload": {"title": "Persistence Record", "text": "Storage validation"},
            }
        ]
        qm1.upsert_points("persist_test", test_points, dimension=128)
        self.assertEqual(qm1.collection_info("persist_test")["points_count"], 1)
        qm1.close()

        # Reopen with fresh client instance pointing to same disk directory
        qm2 = vdb_mod.QdrantManager(db_path=str(db_path))
        results = qm2.search_points("persist_test", [0.05] * 128, limit=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["payload"]["title"], "Persistence Record")
        qm2.close()

    def test_05_secret_filter_exclusion_and_redaction(self):
        """Verify secret file exclusion and pattern redaction."""
        # Excluded paths
        self.assertFalse(ing_mod.SecretFilter.is_path_allowed("F:/Master AI/.env")[0])
        self.assertFalse(ing_mod.SecretFilter.is_path_allowed("F:/Master AI/certs/server.pem")[0])
        self.assertFalse(ing_mod.SecretFilter.is_path_allowed("F:/Master AI/node_modules/pkg/index.js")[0])
        self.assertFalse(ing_mod.SecretFilter.is_path_allowed("F:/Master AI/.git/config")[0])

        # Allowed paths
        self.assertTrue(ing_mod.SecretFilter.is_path_allowed("F:/Master AI/docs/ARCHITECTURE.md")[0])
        self.assertTrue(ing_mod.SecretFilter.is_path_allowed("F:/Master AI/src/pipeline.py")[0])

        # Redaction of secret tokens
        dummy_secret = "sk-" + "abcdef1234567890abcdef123456"
        raw_text = f"The config is set to {dummy_secret} for testing."
        sanitized, was_redacted = ing_mod.SecretFilter.sanitize_content(raw_text)
        self.assertTrue(was_redacted)
        self.assertNotIn(dummy_secret, sanitized)
        self.assertIn("[REDACTED_API_KEY]", sanitized)

    def test_06_semantic_chunker_markdown_and_code(self):
        """Verify markdown heading awareness and code boundary chunking."""
        chunker = ing_mod.DocumentChunker(target_chunk_size=300, chunk_overlap=50)

        # Markdown test
        md_text = (
            "# Main Architecture\n"
            "Overview of the Master AI ecosystem and agent layers.\n\n"
            "## Vector Layer\n"
            "Details about Qdrant vector database and hybrid search mechanics.\n\n"
            "## Model Router\n"
            "Details about fallback hierarchy and provider selection."
        )
        chunks = chunker.chunk_document(md_text, doc_type="markdown")
        self.assertGreaterEqual(len(chunks), 2)
        headings = [c.heading for c in chunks]
        self.assertTrue(any("Vector Layer" in h or "Main Architecture" in h for h in headings))

        # Python test
        py_code = (
            "class AgentRouter:\n"
            "    def route(self, task):\n"
            "        return 'active'\n\n"
            "def helper_function():\n"
            "    return True\n"
        )
        py_chunks = chunker.chunk_document(py_code, doc_type="python")
        self.assertGreaterEqual(len(py_chunks), 1)

    def test_07_deduplicator_manifest_incremental_ingestion(self):
        """Verify incremental ingestion skips unchanged content."""
        manifest_path = self.test_dir / "test_manifest.json"
        manifest = ing_mod.DeduplicationManifest(manifest_path)

        doc_id = "test_doc_01"
        content_hash = ing_mod.compute_sha256("Initial content")

        self.assertFalse(manifest.is_document_unchanged(doc_id, content_hash))
        manifest.record_document_ingested(
            doc_id=doc_id,
            file_path="test_doc.md",
            sha256_hash=content_hash,
            collection_name="test_coll",
            point_ids=["pt-1", "pt-2"],
            chunk_count=2,
        )
        self.assertTrue(manifest.is_document_unchanged(doc_id, content_hash))

        # Changed content
        new_hash = ing_mod.compute_sha256("Updated content")
        self.assertFalse(manifest.is_document_unchanged(doc_id, new_hash))

    def test_08_pure_python_bm25_keyword_search(self):
        """Verify pure-Python Okapi BM25 engine ranking."""
        bm25 = search_mod.BM25Engine()
        bm25.add_document("doc1", "The quick brown fox jumps over the lazy dog", {"title": "Fox Story"})
        bm25.add_document("doc2", "Autonomous multi-agent orchestration and intelligence layer", {"title": "Agent Arch"})
        bm25.add_document("doc3", "Deterministic mock embeddings for offline testing", {"title": "Embeddings"})

        res = bm25.search("autonomous multi-agent", limit=2)
        self.assertGreaterEqual(len(res), 1)
        self.assertEqual(res[0]["id"], "doc2")
        self.assertIn("autonomous", res[0]["matched_terms"])

    def test_09_hybrid_search_rrf_scoring(self):
        """Verify dense and sparse fusion via Reciprocal Rank Fusion."""
        qm = vdb_mod.QdrantManager(in_memory=True)
        embedder = emb_mod.get_embedding_engine("mock", dimension=128)
        dense = search_mod.DenseSearchEngine(qm, embedder)
        bm25 = search_mod.BM25Engine()

        text = "Sovereign intelligence with fail-closed security boundary."
        payload = {"title": "Security Blueprint", "text": text, "custom_id": "sec-01"}
        qm.upsert_points("knowledge_docs", [{"id": "sec-01", "vector": embedder.embed_text(text), "payload": payload}])
        bm25.add_document("sec-01", text, payload)

        hybrid = search_mod.HybridSearchEngine(dense, bm25)
        results = hybrid.search("knowledge_docs", "fail-closed security boundary", limit=3)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "sec-01")
        self.assertGreaterEqual(results[0]["score"], 0.8)

    def test_10_rag_factual_response_and_missing_info_guard(self):
        """Verify factual synthesis, citations, Hindi support, and missing-info guard."""
        qm = vdb_mod.QdrantManager(in_memory=True)
        embedder = emb_mod.get_embedding_engine("mock", dimension=128)
        dense = search_mod.DenseSearchEngine(qm, embedder)
        bm25 = search_mod.BM25Engine()
        hybrid = search_mod.HybridSearchEngine(dense, bm25)

        text = "Master AI utilizes Qdrant for vector storage and BM25 for sparse retrieval."
        payload = {"title": "Hybrid Architecture", "text": text, "custom_id": "arch-100"}
        qm.upsert_points("knowledge_docs", [{"id": "arch-100", "vector": embedder.embed_text(text), "payload": payload}])
        bm25.add_document("arch-100", text, payload)

        rag = rag_mod.RAGResponseEngine(hybrid_search_engine=hybrid)

        # Factual query
        res_en = rag.answer_query("What does Master AI utilize for vector storage and sparse retrieval?")
        self.assertFalse(res_en["missing_information_detected"])
        self.assertGreater(len(res_en["citations"]), 0)
        self.assertIn("Qdrant", res_en["answer"])

        # Hindi query
        res_hi = rag.answer_query("वेक्टर स्टोरेज के लिए मास्टर एआई क्या उपयोग करता है?")
        self.assertEqual(res_hi["language"], "hi")

        # Missing information query
        res_missing = rag.answer_query("How do you bake a sourdough loaf from scratch?")
        self.assertTrue(res_missing["missing_information_detected"])
        self.assertIn("not found", res_missing["answer"].lower())

    def test_11_agent_memory_six_categories_and_authorization(self):
        """Verify all 6 categories, deduplication, and authorization enforcement."""
        ledger_file = self.test_dir / "agent_memory_test_ledger.json"
        qm = vdb_mod.QdrantManager(in_memory=True)
        embedder = emb_mod.get_embedding_engine("mock", dimension=128)
        mgr = mem_mod.AgentMemoryManager(
            qdrant_manager=qm,
            embedding_engine=embedder,
            ledger_path=ledger_file,
        )

        categories = [
            "project_memory",
            "task_history",
            "technical_decisions",
            "reusable_solutions",
            "user_preferences",
            "agent_knowledge",
        ]

        stored_ids = {}
        for cat in categories:
            rec = mgr.store_memory(
                category=cat,
                title=f"Test {cat}",
                content=f"Content for {cat} verification in Master AI.",
                agent_id="software_architect",
                tags=[cat],
            )
            stored_ids[cat] = rec.memory_id
            self.assertEqual(rec.category, cat)

        # Verify stats
        stats = mgr.get_stats()
        self.assertEqual(stats["total_memories"], 6)

        # Authorization: unauthorized agent cannot delete
        target_id = stored_ids["technical_decisions"]
        with self.assertRaises(PermissionError):
            mgr.delete_memory(target_id, caller_agent_id="rogue_agent", is_admin=False)

        # Authorized deletion by creator
        deleted = mgr.delete_memory(target_id, caller_agent_id="software_architect", is_admin=False)
        self.assertTrue(deleted)
        self.assertIsNone(mgr.get_memory_by_id(target_id))

    def test_12_fastapi_knowledge_and_memory_endpoints(self):
        """Verify FastAPI REST endpoints for RAG and Memory."""
        from fastapi.testclient import TestClient

        client = TestClient(api_main_mod.app)

        # RAG Health
        h_resp = client.get("/api/v1/rag/health")
        self.assertEqual(h_resp.status_code, 200)
        self.assertEqual(h_resp.json()["status"], "healthy")

        # Memory Store
        store_resp = client.post(
            "/api/v1/memory/store",
            json={
                "category": "reusable_solutions",
                "title": "API Verification Solution",
                "content": "Verify all REST routes using FastAPI TestClient.",
                "agent_id": "testing_agent",
                "tags": ["api", "testing"],
            },
        )
        self.assertEqual(store_resp.status_code, 200)
        mem_id = store_resp.json()["memory"]["memory_id"]

        # Memory Query
        query_resp = client.post(
            "/api/v1/memory/query",
            json={"query": "TestClient REST verification", "limit": 3},
        )
        self.assertEqual(query_resp.status_code, 200)
        self.assertGreaterEqual(query_resp.json()["total_hits"], 1)

        # Memory Delete
        del_resp = client.delete(f"/api/v1/memory/{mem_id}?caller_agent_id=testing_agent")
        self.assertEqual(del_resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
