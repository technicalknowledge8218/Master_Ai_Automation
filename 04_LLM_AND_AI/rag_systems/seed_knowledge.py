"""
Seed Initial Knowledge Base & Agent Memory for Master AI
========================================================
Populates initial foundational documentation, ADRs, solutions, and project
milestones into Qdrant vector database and JSON ledgers.
"""

import sys
import importlib
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

vdb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.vector_db")
emb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.embeddings")
ing_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.ingestion")
mem_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.memory")
search_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.search")

def seed():
    print("--- Starting Master AI Knowledge & Memory Seeding ---")
    qm = vdb_mod.QdrantManager()
    qm.initialize_core_collections(dimension=128)
    embedder = emb_mod.get_embedding_engine("auto", dimension=128)
    pipeline = ing_mod.IngestionPipeline(qdrant_manager=qm, embedding_engine=embedder)
    mem_mgr = mem_mod.AgentMemoryManager(qdrant_manager=qm, embedding_engine=embedder)
    bm25 = search_mod.BM25Engine()

    # 1. Ingest Core Documentation
    docs_to_index = [
        ("04_LLM_AND_AI/README.md", "Sovereign Intelligence & LLM Architecture", "architecture"),
        ("03_AI_AGENTS/README.md", "Autonomous Agent Collaboration Guide", "agents"),
        ("00_CORE_SYSTEM/master_plan/MASTER_DEVELOPMENT_INSTRUCTIONS.md", "Master Development Instructions", "project_docs"),
        ("00_CORE_SYSTEM/master_plan/AUTONOMOUS_OPERATING_SYSTEM_BLUEPRINT.md", "Autonomous Operating System Blueprint", "project_docs"),
    ]

    for rel_path, title, cat in docs_to_index:
        full_path = root_dir / rel_path
        if full_path.exists():
            res = pipeline.ingest_file(full_path, collection_name="knowledge_docs", category=cat, force=True)
            print(f"Indexed file '{rel_path}': {res.get('status')} ({res.get('chunks_indexed', 0)} chunks)")
            # Register in BM25
            content = full_path.read_text(encoding="utf-8", errors="replace")
            bm25.add_document(doc_id=rel_path, text=title + " " + content, metadata={"title": title, "category": cat})

    bm25.save()

    # 2. Seed Long-Term Memories across 6 categories
    memories = [
        # 1. Project Memory
        (
            "project_memory",
            "Master AI Workspace & Environment Specification",
            "Master AI official root is relocated to F:\\Master AI. Environment: Windows 11, Intel Core i5 13th Gen, 32 GB RAM, Python 3.14.5 virtual environment. Docker and WSL2 are disabled by default. Strict fail-closed zero-paid budget enforced.",
            "orchestrator",
            ["root", "environment", "budget", "windows11"],
        ),
        # 2. Task History
        (
            "task_history",
            "Phase 1 & Phase 2 Completion Milestones",
            "Phase 1 (Infrastructure) verified with 7/7 smoke tests. Phase 1.1 (Path Correction) created dynamic path_config.py. Phase 2 (Intelligence Layer) delivered Model Registry, Provider Adapters, Router, and Benchmarks with 11/11 tests passing.",
            "testing_agent",
            ["milestone", "phase1", "phase2", "qa"],
        ),
        # 3. Technical Decisions
        (
            "technical_decisions",
            "ADR-001: Centralized Dynamic Path Configuration",
            "Context: Relocation from C: to F: broke hardcoded absolute paths. Decision: Implement 00_CORE_SYSTEM/config/path_config.py with dynamic anchor search and MASTER_AI_ROOT override. Forbids hardcoded absolute paths in scripts.",
            "software_architect",
            ["adr", "paths", "architecture"],
        ),
        (
            "technical_decisions",
            "ADR-002: Dual-Model Hierarchy and Fail-Closed Security Boundary",
            "Context: Prevent unauthorized API charges while enabling agent workflows. Decision: Default to offline-mock-deterministic and local Ollama. Cloud models are strictly gated by SecurityBoundary requiring explicit user approval.",
            "software_architect",
            ["adr", "security", "llm"],
        ),
        (
            "technical_decisions",
            "ADR-003: Pure-Python BM25 and Embedded Qdrant Vector Storage",
            "Context: Windows 11 WDAC blocks untrusted C extensions. Decision: Use pure-Python Okapi BM25 for sparse keyword search combined with embedded Qdrant for dense semantic vectors via Reciprocal Rank Fusion (RRF).",
            "software_architect",
            ["adr", "rag", "bm25", "qdrant"],
        ),
        # 4. Reusable Solutions
        (
            "reusable_solutions",
            "Dynamic Module Import for Leading Digit Directories",
            "Problem: Python grammar syntax forbids 'import 00_CORE_SYSTEM'. Solution: Use importlib.import_module('00_CORE_SYSTEM.config.path_config') to cleanly load modules with numeric folder prefixes.",
            "coding_agent",
            ["python", "importlib", "solution"],
        ),
        (
            "reusable_solutions",
            "Deterministic Offline Mock Embeddings",
            "Problem: Tests must run offline without downloading multi-gigabyte models. Solution: Use SHA-256 token projection with L2 normalization to generate reproducible 128-dim vectors preserving semantic similarity.",
            "coding_agent",
            ["embeddings", "offline", "testing"],
        ),
        # 5. User Preferences
        (
            "user_preferences",
            "User Operating Preferences and Constraints",
            "User demands strict zero-hallucination answers with explicit citations. Hindi and English multi-lingual support must be maintained. Nothing goes global without explicit user approval. All test results must be factual.",
            "documentation_agent",
            ["preferences", "governance", "hindi", "citations"],
        ),
        # 6. Agent Knowledge
        (
            "agent_knowledge",
            "Specialist Agent Capabilities & Security Tokens",
            "Master AI operates 7 specialist agents: software_architect (ADRs, design), coding_agent (implementation), testing_agent (QA, benchmarks), documentation_agent (guides, dashboard), security_auditor (policy gates), capability_discovery_agent (domain tracking), research_agent (deep research).",
            "capability_discovery_agent",
            ["agents", "specialists", "capabilities"],
        ),
    ]

    for cat, title, content, agent_id, tags in memories:
        rec = mem_mgr.store_memory(
            category=cat,
            title=title,
            content=content,
            agent_id=agent_id,
            tags=tags,
        )
        print(f"Stored Memory [{cat}]: {rec.memory_id} - '{title}'")

    print("\n--- Seeding Complete ---")
    print(mem_mgr.get_stats())
    qm.close()

if __name__ == "__main__":
    seed()
