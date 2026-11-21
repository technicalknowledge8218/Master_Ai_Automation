# Master AI — Hardware & Environment Audit Report

- **Date**: 2026-11-17
- **Target Host**: Windows 11 Workstation
- **Audit Tool**: Native WMI, Python runtime, and PowerShell environment probes

---

## 1. Executive Hardware Profile

| Subsystem | Specification Detected | Operational Implication for Master AI |
|---|---|---|
| **Operating System** | Windows 11 Enterprise (Build 10.0.26300, 64-bit AMD64) | Full Win32 and PowerShell runtime support; WSL2 available for Linux containers. |
| **Processor (CPU)** | Intel Core i5-1245U (12th Gen, 10 cores: 2 P-cores, 8 E-cores, 12 logical threads) | High multithread efficiency, low thermal envelope (15W base, 55W turbo). **CPU-First design mandatory**. |
| **Physical Memory (RAM)** | **31.69 GB Total (~32 GB)** (Free: ~12-14 GB dynamic) | Sufficient RAM for running 3B–8B quantized LLMs concurrently with embedded vector databases. |
| **Graphics (GPU)** | **Intel Iris Xe Graphics** (Adapter RAM: 2.15 GB shared dynamic VRAM, Driver 32.0.101.7088) | **NO DEDICATED NVIDIA / AMD GPU**. CUDA is NOT supported. Acceleration restricted to OpenVINO, DirectML, and CPU vector extensions (AVX2). |
| **Primary Storage (C:)** | Total: 280.5 GB \| Used: 269.6 GB \| **Available: 10.9 GB** | **CRITICAL CONSTRAINT**: Disk headroom is low (10.9 GB). Must prevent uncontrolled multi-gigabyte model downloads or duplicate Docker layers. |

---

## 2. Toolchain & Runtime Environment

| Binary | Status | Version / Path | Readiness Assessment |
|---|:---:|---|---|
| **Python** | **READY** | Python 3.14.5 (`C:\Python314\python.exe`) | Active modern Python runtime; isolated venv management recommended. |
| **Git** | **READY** | git version 2.55.0.windows.4 (`C:\Program Files\Git\cmd\git.EXE`) | Local git version control fully functional. |
| **Node.js** | **READY** | v24.16.0 (`C:\Program Files\nodejs\node.EXE`) | Active LTS runtime for frontend tooling, React, and Remotion. |
| **npm** | **READY** | npm CLI (`C:\Program Files\nodejs\npm.CMD`) | Package manager available for React & Vite dependencies. |
| **Ollama** | **READY** | v0.40.16 (`C:\Users\Sangam\AppData\Local\Programs\Ollama\ollama.EXE`) | Daemon installed and responsive. Currently 0 models pulled. |
| **Docker** | **INSTALLED** | Docker CLI v29.8.1 | CLI installed; Docker Desktop daemon not running. |
| **FFmpeg** | **NOT ON PATH** | Missing from system PATH | Required for video/audio pipeline; must be staged or packaged portably. |
| **Rust / Cargo** | **NOT INSTALLED**| Missing | Native compilation requires pre-built wheels or binaries. |

---

## 3. CPU-First & Low-VRAM Optimization Strategy

Given the **Intel Iris Xe Graphics** (no CUDA) and **10.9 GB free disk space**, the following operational strategies are enforced across Master AI:

### 3.1 Local LLM Execution
- **Architecture**: Ollama / `llama.cpp` using CPU inference with AVX2 acceleration.
- **Model Selection & Quantization**:
  - Primary Local Lightweight Model: **LLaMA 3.2 3B Instruct (Q4_K_M)** (~2.0 GB disk, ~3.5 GB RAM) or **Qwen 2.5 3B (Q4_K_M)** (~2.0 GB disk).
  - Micro Reasoning & Routing Model: **LLaMA 3.2 1B Instruct (Q4_K_M)** (~1.1 GB disk, ~1.8 GB RAM).
  - Heavy 8B models (e.g. LLaMA 3.1 8B Q4) are kept optional and requires ~4.7 GB disk headroom.
- **Thread Allocation**: Bound to 4–6 threads to prevent starving host background tasks and E-cores.

### 3.2 Audio & Speech Synthesis
- **Text-to-Speech (TTS)**: **Kokoro-82M** via `kokoro-onnx` on CPU (~82M parameters, ~350MB disk). Sub-second synthesis on Intel Core i5 with natural voice quality, zero GPU dependency.
- **Speech-to-Text (STT)**: **faster-whisper** using `model_size="base"` or `"small"` with `compute_type="int8"` on CPU (~150MB–500MB disk).

### 3.3 Vector Database & Embeddings
- **Vector DB**: **Qdrant** embedded / local mode (using local directory storage via `qdrant-client[fastembed]`) or SQLite with `sqlite-vec`. Avoids memory-heavy separate server daemons.
- **Embeddings**: `BAAI/bge-small-en-v1.5` or `all-MiniLM-L6-v2` via ONNX/FastEmbed (~130MB, running on CPU in <15ms per chunk).

### 3.4 Video Production & Rendering
- **Video Assembly**: **FFmpeg** (portable static build) for stitching, trimming, audio mixing, and subtitle burning via CPU encoding (`libx264` with `-preset fast -crf 22`).
- **Programmatic Motion Graphics**: **Remotion** via React/Node.js, configured with headless Chrome frame rendering.
- **Complex Generative AI Imagery / Video**:
  - Image generation: Local lightweight SD-1.5 / LCM on OpenVINO, or hybrid API integration (with explicit human approval gate) for cloud-accelerated generation when high resolution is required.

---

## 4. Disk Space Conservation Protocols

Because the C: drive has **10.9 GB free space**:
1. **Model Cache Cap**: Total cached model weights across Ollama, HuggingFace, and Kokoro must not exceed **5.0 GB**.
2. **Artifact Retention**: Video renders and intermediate audio clips must be purged or archived after export.
3. **Docker Strategy**: Prefer lightweight workspace-local Node/Python processes over running heavy multi-gigabyte Docker images until disk space is expanded.
