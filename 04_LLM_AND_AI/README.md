# 04_LLM_AND_AI — Intelligence Layer & LLM Management

## 1. Executive Purpose
The **Intelligence Layer** provides sovereign, production-grade LLM lifecycle management, intelligent task-based model routing, agent-specific model assignments, multi-provider abstraction, empirical benchmarking, and local Ollama model management.

## 2. Directory Architecture
```text
04_LLM_AND_AI/
├── README.md
├── LLM_INTEGRATION_ARCHITECTURE.md
├── api/
│   └── llm_router.py              # FastAPI REST endpoints for intelligence operations
├── llm_manager/
│   ├── __init__.py                # Central package exports
│   ├── model_registry.py          # Model profiles, limits, pricing, validation
│   ├── provider_registry.py       # Multi-provider lifecycle and availability monitoring
│   ├── router.py                  # Intelligent task routing and automatic fallback engine
│   ├── agent_assignment.py        # External agent-to-model configuration manager
│   ├── benchmark_engine.py        # Empirical 7-dimension evaluation harness
│   ├── local_manager.py           # Native Ollama discovery, pull bounds, guarded deletion
│   ├── security.py                # Redaction, budget enforcement ($0.00 zero-paid default)
│   └── adapters/
│       ├── base_adapter.py        # Abstract BaseLLMAdapter protocol
│       ├── offline_mock_adapter.py# High-fidelity deterministic offline mock provider
│       ├── ollama_adapter.py      # Native Win32 Ollama daemon HTTP interface
│       ├── openai_adapter.py      # OpenAI-compatible API standard adapter
│       └── litellm_adapter.py     # LiteLLM multi-cloud gateway adapter
├── models/
│   ├── MODEL_REGISTRY.json        # Persisted catalog of registered models
│   └── AGENT_MODEL_ASSIGNMENTS.json # External agent-to-model mappings
├── benchmarks/
│   └── results/                   # Persisted empirical benchmark JSON reports
├── rag_systems/
│   └── qdrant_db/                 # Embedded vector store (git-ignored)
└── prompts/
    └── PROMPT_CATALOG.json        # Curated system and task prompt templates
```

## 3. Core Architectural Subsystems

### 3.1 Model & Provider Registries
- **Zero-Paid Default**: Defaults to `offline-mock-deterministic` ($0.00/1M tokens) with strict `ENFORCE_ZERO_PAID_API=true` boundary.
- **Provider Adapters**:
  - `OfflineMockProvider`: Deterministic, zero-dependency offline simulation.
  - `OllamaLocal`: Interfaces with `http://127.0.0.1:11434` for CPU-first inference.
  - `LiteLLMGateway`: Multi-cloud gateway with automatic mock fallback.
  - `OpenAI` / `Google`: OpenAI-compatible endpoint standard.

### 3.2 Intelligent Model Router
Routes requests dynamically based on task type (`coding`, `reasoning`, `research`, `structured_json`, `fast_chat`), required intelligence level, latency, and context window.
- **Automatic Fallback**: Primary -> Secondary -> Offline Mock fallback chain.
- **Fail-Closed Policy**: Will NEVER silently switch to a paid model without explicit authorization.

### 3.3 Agent Model Assignment
Each of the 7 specialist agents possesses dedicated configuration without altering agent code:
- `coding_agent`: Preferred `offline-mock-deterministic`, backup `qwen2.5:1.5b` (temp: 0.2, code generation).
- `research_agent`: Preferred `offline-mock-deterministic`, backup `qwen2.5:1.5b` (temp: 0.5, reasoning).
- `software_architect`: Preferred `offline-mock-deterministic`, backup `llama-3.1-8b-instruct-local` (temp: 0.3, json/adr).
- `testing_agent`: Preferred `offline-mock-deterministic`, backup `qwen2.5:1.5b` (temp: 0.2, test suites).
- `documentation_agent`: Preferred `offline-mock-deterministic`, backup `qwen2.5:1.5b` (temp: 0.6, markdown).
- `security_auditor`: Preferred `offline-mock-deterministic`, backup `llama-3.1-8b-instruct-local` (temp: 0.1, audit).
- `capability_discovery_agent`: Preferred `offline-mock-deterministic`, backup `qwen2.5:1.5b` (temp: 0.4, catalog).

### 3.4 Empirical Benchmark Engine
Standardized test suite evaluating models across 7 key dimensions:
1. `BM-01`: General reasoning
2. `BM-02`: Research synthesis
3. `BM-03`: Coding generation (Sieve of Eratosthenes)
4. `BM-04`: Structured JSON output
5. `BM-05`: Strict instruction following
6. `BM-06`: Bilingual Hindi & English comprehension
7. `BM-07`: Long-context needle-in-a-haystack retrieval

### 3.5 Local Model Manager (Ollama)
- Discovers locally installed models on Drive F:.
- Enforces `MAX_LOCAL_MODEL_SIZE_GB` (2.73 GB max).
- Rejects automatic pulls exceeding storage boundaries.
- Strictly guards deletion: requires `explicit_user_approval=True`.

## 4. REST API Endpoints
Served via `00_CORE_SYSTEM/api/main.py`:
- `GET  /api/v1/intelligence/health` — Subsystem health diagnostics
- `GET  /api/v1/intelligence/models` — List registered models & capabilities
- `POST /api/v1/intelligence/models/{model_id}/status` — Activate/deactivate model
- `GET  /api/v1/intelligence/providers` — List provider adapters & reachability
- `POST /api/v1/intelligence/chat/completions` — Intelligent completion routing
- `GET  /api/v1/intelligence/agents/assignments` — View agent model mappings
- `POST /api/v1/intelligence/agents/assignments/{agent_slug}` — Update agent assignment
- `GET  /api/v1/intelligence/benchmarks` — View benchmark reports
- `POST /api/v1/intelligence/benchmarks/run` — Run empirical benchmark suite
- `GET  /api/v1/intelligence/local/models` — List installed Ollama models
- `POST /api/v1/intelligence/local/models/estimate` — Estimate RAM/disk requirements
- `POST /api/v1/intelligence/local/models/delete` — Guarded model deletion
- `GET  /api/v1/intelligence/routing/fallback-history` — Audit fallback log

## 5. Sovereign RAG, Knowledge Base & Agent Memory Subsystem (Phase 3)

### 5.1 Architecture Overview
The Phase 3 subsystem provides a multi-layer persistent RAG and memory architecture:
- **Vector Database**: Embedded Qdrant persistent storage at `04_LLM_AND_AI/rag_systems/qdrant_db`.
- **Sparse Search**: Pure-Python Okapi BM25 engine with zero C-dependencies.
- **Fusion**: Reciprocal Rank Fusion (RRF, k=60) combining dense semantic cosine scores and sparse keyword ranks.
- **Ingestion**: Ingestion pipeline with automated secret filtering, heading-aware semantic chunking, and SHA-256 deduplication.
- **Agent Memory**: 6-category persistent ledger (`project_memory`, `task_history`, `technical_decisions`, `reusable_solutions`, `user_preferences`, `agent_knowledge`) with creator-based access control.
- **Agent Memory Bridge**: Inter-agent gateway (`03_AI_AGENTS/orchestrator/agent_memory_bridge.py`) allowing all 7 specialist agents to store/recall memories and query verified knowledge.

### 5.2 RAG & Memory REST API Endpoints
- `GET  /api/v1/rag/health` — Vector DB, BM25, and memory health metrics
- `GET  /api/v1/rag/collections` — List registered collections and point counts
- `POST /api/v1/rag/ingest/file` — Ingest document file with secret filtering and deduplication
- `POST /api/v1/rag/ingest/text` — Ingest raw text or research note
- `POST /api/v1/rag/search/hybrid` — Dense + BM25 hybrid search with RRF scoring
- `POST /api/v1/rag/query` — Factual multi-lingual Q&A with citations and missing-info guard
- `POST /api/v1/memory/store` — Store memory into one of the 6 categories
- `POST /api/v1/memory/query` — Semantic query over agent memories
- `GET  /api/v1/memory/list` — List memories sorted chronologically
- `DELETE /api/v1/memory/{id}` — Guarded deletion with agent authorization check
- `GET  /api/v1/memory/stats` — Breakdown of memories by category
