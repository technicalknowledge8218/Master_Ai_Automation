# Master AI — Technology Selection & Installation Manifest

This manifest evaluates, filters, and standardizes the open-source software stack for the **Master AI Autonomous Production Platform** based on the verified Intel Core i5 13th Gen (1245U) CPU-first architecture, 32 GB RAM, and 10.9 GB available disk capacity.

---

## 1. Core Technology Evaluation Matrix

| Technology | Category | License | CPU / RAM Profile | Role & Evaluation Decision | Installation / Integration Method |
|---|---|---|---|---|---|
| **Ollama** | Local LLM Server | MIT | 4 threads, 2–4 GB RAM | **ADOPT (Primary Local Model Runner)**: Already installed v0.40.16. Native Win32 service, supports Q4_K_M GGUF models. | Use existing installation at `<USER_HOME>\AppData\Local\Programs\Ollama\`. |
| **llama.cpp** | Local LLM Engine | MIT | 4–6 threads, AVX2 | **ADOPT (Secondary / Direct Engine)**: Underlying C++ engine for Ollama and direct CLI inference. | Built-in via Ollama backend; direct binary optional. |
| **LiteLLM** | Universal LLM Proxy | MIT | <100 MB RAM | **ADOPT (Primary Gateway)**: Standardizes 100+ local and cloud LLM providers behind OpenAI-compatible endpoint. | Python package (`litellm`), workspace local. |
| **Open WebUI** | Web UI for LLMs | Port of Ollama UI | ~500 MB RAM | **EVALUATED (Alternative)**: Good GUI, but overlaps with custom Master AI Central Dashboard. | Defer in favor of custom unified React Dashboard. |
| **LangGraph** | Multi-Agent State Machine | MIT | Lean Python library | **ADOPT (Orchestration Engine)**: Deterministic cyclic graphs, state persistence, checkpointing, and human-in-the-loop approvals. | Python package (`langgraph`). |
| **CrewAI** | Multi-Agent Roleplay | MIT | Heavy abstractions | **EVALUATED (Conditional)**: Higher boilerplate and tighter coupling than LangGraph. | Keep as reference; use LangGraph for core orchestration. |
| **Agno (Phidata)**| Multi-Modal Agents | MIT | Fast, structured | **EVALUATED (Specialized)**: Excellent for structured tool calling and multimodal memory. | Selected for specialized tool-agent sub-pipelines. |
| **MCP SDK & Servers** | Tool Protocol | MIT | Lean JSON-RPC | **ADOPT (Universal Tool Protocol)**: Connects agents to file systems, databases, devtools, and web search. | Native Antigravity MCP integration. |
| **Playwright MCP** | Browser Automation | Apache 2.0 | ~200 MB headless | **ADOPT (Autonomous Web Interaction)**: Autonomous DOM inspection, scraping, form filling, and web testing. | Standard MCP server (`@playwright/mcp`). |
| **Qdrant** | Vector Search Engine | Apache 2.0 | <300 MB (local mode) | **ADOPT (Primary Vector DB)**: Embedded local directory mode (`qdrant-client[fastembed]`). Zero daemon overhead. | Python package (`qdrant-client`). |
| **LlamaIndex** | RAG Framework | MIT | Modular Python | **ADOPT (Document Indexing & RAG)**: Chunks, indexes, and queries domain knowledge bases. | Python package (`llama-index-core`). |
| **Docling** | Document Parsing | MIT | CPU-based layout OCR | **ADOPT (Document Ingestion)**: High-precision parsing of PDFs, Word docs, tables, and Markdown into clean RAG chunks. | Python package (`docling`). |
| **Crawl4AI** | Web Scraping for LLMs | Apache 2.0 | Headless Playwright | **ADOPT (Web Research Crawler)**: Extracts clean Markdown from arbitrary web pages for agent consumption. | Python package (`crawl4ai`). |
| **PostgreSQL** | Relational DB | PostgreSQL Lic | ~50 MB base | **ADOPT (Transactional Core)**: Master transactional system of record. Uses SQLite embedded fallback for zero-overhead local dev. | SQLite / PostgreSQL adapter (`psycopg2` / `aiosqlite`). |
| **Redis** | In-Memory Cache | BSD / Redis Lic | ~30 MB base | **ADOPT (Caching & Pub/Sub)**: In-memory task queue and message bus. Uses in-process memory queue for zero-dependency mode. | In-memory queue / Redis client. |
| **MinIO** | S3-Compatible Object Store| AGPLv3 | ~100 MB RAM | **CONDITIONAL / OPTIONAL**: S3 storage for video/audio assets. For local workstation, local filesystem asset directory (`16_VIDEO_LIBRARY`) is preferred to conserve disk. | Local filesystem storage abstraction with S3 API parity. |
| **FastAPI** | Backend API Framework | MIT | <40 MB, fast async | **ADOPT (Core Backend Standard)**: High-speed async REST & WebSocket server for dashboard and agent orchestration. | Python package (`fastapi`, `uvicorn`). |
| **React 19 + Vite** | Frontend Dashboard | MIT | Browser client | **ADOPT (Central Dashboard UI)**: Component-driven web interface consuming design tokens and WebSocket feeds. | Node.js / Vite build in `20_CENTRAL_DASHBOARD`. |
| **FFmpeg** | Video/Audio Processing | LGPL / GPL | CPU-based libx264 | **ADOPT (Video Engine Primitive)**: Stitching, video scaling, audio mixing, subtitle hardcoding, format conversion. | Portable static Windows binary (`ffmpeg.exe`, `ffprobe.exe`). |
| **Remotion** | Programmatic Video | Remotion License | Node.js headless Chrome| **ADOPT (Dynamic Motion Graphics)**: React-based video generation for intros, kinetic typography, and motion overlays. | Node.js package in `16_VIDEO_LIBRARY/remotion`. |
| **ComfyUI** | Node-Based Diffusion UI | GPLv3 | Heavy GPU / VRAM | **CONDITIONAL (Cloud / OpenVINO Fallback)**: Due to Intel Iris Xe GPU, run locally via OpenVINO or route heavy generation to cloud API. | Hybrid API adapter with local OpenVINO experimental pipeline. |
| **Kokoro TTS** | Voice Synthesis | Apache 2.0 | 82M params, <1 GB RAM | **ADOPT (Primary Voice Engine)**: Ultra-fast, natural speech synthesis running purely on CPU via ONNX. | Python package (`kokoro-onnx`, `soundfile`). |
| **faster-whisper** | Speech-to-Text | MIT | INT8 CPU, <500 MB RAM| **ADOPT (Subtitles & Transcription)**: Accurate speech recognition and automatic SRT/VTT subtitle generation. | Python package (`faster-whisper`). |
| **Langfuse** | LLM Observability | MIT (Core) | Cloud / Self-hosted | **ADOPT (Observability & Tracing)**: Tracks token usage, latency, cost, and trace spans across agent workflows. | Python SDK (`langfuse`) reporting to local or self-hosted trace collector. |

---

## 2. Phased Installation & Integration Strategy

To respect the **10.9 GB disk constraint** and **CPU-first architecture**, dependencies are introduced in disciplined, functional tiers:

```
[Tier 1: Core Engine & Gateway]
  - Python Virtual Environment (Isolated, no global contamination)
  - LiteLLM + FastAPI + SQLite/Postgres Layer
  - Ollama local connection (LLaMA 3.2 1B/3B Q4_K_M)

[Tier 2: Knowledge, RAG & Vector Engine]
  - Qdrant Embedded (Zero server daemon)
  - FastEmbed ONNX embeddings (bge-small-en)
  - LlamaIndex + Crawl4AI + Docling

[Tier 3: Multi-Agent Orchestration & Tooling]
  - LangGraph stateful execution graphs
  - Playwright MCP browser automation
  - 13 Specialized Agent roles & Human Approval Checkpoints

[Tier 4: Audio & Speech Synthesis Engine]
  - Kokoro-ONNX CPU TTS (82M params)
  - faster-whisper CPU INT8 STT
  - Portable static FFmpeg binaries

[Tier 5: Automated Video Production Engine]
  - Remotion React video templates
  - FFmpeg pipeline (script -> voiceover -> scenes -> subtitles -> export)
  - Shorts & Reels auto-formatting

[Tier 6: Central Management Dashboard]
  - React 19 + Tailwind CSS + Vite
  - 14 integrated management panes
  - Live WebSocket telemetry & Approval Center
```

---

## 3. Commercial Licensing & Security Compliance

- **OSI / Permissive Dominance**: 85%+ of stack is MIT / Apache 2.0 / BSD (React, FastAPI, Ollama, LangGraph, Qdrant, Kokoro, faster-whisper, LiteLLM).
- **GPL / LGPL Boundary Management**: FFmpeg is used as a standalone subprocess binary via CLI execution, preserving architectural license isolation.
- **AGPLv3 Avoidance**: MinIO is replaced by a zero-overhead local S3-compatible filesystem store for local development, eliminating AGPLv3 cloud distribution exposure.
- **Docker Licensing**: Avoids Docker Desktop commercial licensing dependencies by executing lightweight native Win32/Python/Node processes directly in the workspace.
