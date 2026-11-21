# LEGAL & OPEN-SOURCE LICENSE COMPATIBILITY REPORT
**Target Output**: `F:\Master AI\00_CORE_SYSTEM\research\phase-7\phase-7.12\license_compatibility_report.md`  
**Date**: 2026-11-18  
**Scope**: Legal compliance review of candidate open-source tools and repositories for Master AI.

---

## 1. Candidate Repository License Matrix

| Project | License Identifier | License Category | Direct Code Ingestion Permitted? | Architectural Concepts Permitted? | Commercial Usage Risk |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OpenMontage** | **AGPL-3.0** | Strong Network Copyleft | **NO (Forbidden)** | **YES (Clean-room allowed)** | High (Triggers copyleft over network) |
| **OpenDirector** | **LGPL-3.0** | Weak Copyleft | **NO (Avoid direct code)** | **YES** | Moderate |
| **ComfyUI** | **GPL-3.0** | Strong Copyleft | **NO (Separate process only)**| **YES** | Moderate / High if bundled |
| **OpenBone** | **MIT** | Permissive | **YES (Fully Permitted)** | **YES** | **Zero Risk (Commercial safe)** |
| **OpenToonz** | **Modified BSD** | Permissive | **YES** | **YES** | **Zero Risk** |

---

## 2. Deep Dive: AGPL-3.0 Implications for OpenMontage

The GNU Affero General Public License v3.0 (AGPL-3.0) is designed specifically to prevent software from being run as a cloud service or agent without releasing the entire derivative codebase.
- **Section 13 (Remote Network Interaction)**: If an AGPL-3.0 program or modified work interacts with users remotely through a computer network, the entire source code of the containing software must be provided to all network users under the AGPL-3.0 license.
- **Master AI Policy**:
  1. **Strict Prohibition on Source Copying**: Under no circumstances should source code, scripts, or proprietary skill markdown files from OpenMontage be copied verbatim into the Master AI repository.
  2. **Clean-Room Architectural Implementation**: Copyright protects the specific expression of software (the code), but not underlying ideas, workflow concepts, mathematical structures, or architectural patterns.
  3. Master AI implements its own pipeline manifests, director skills, tool registry, and validation suites from first principles.

---

## 3. Deep Dive: MIT License Benefits for OpenBone

The MIT License is an ultra-permissive open-source license:
- Permits commercial use, modification, distribution, sublicensing, and private use.
- Requires only that the original copyright notice and permission notice be included in copies or substantial portions of the software.
- Master AI can integrate OpenBone runtimes, MCP servers, and skeletal schemas without legal friction or viral licensing obligations.

---

## 4. Operational Guidelines for Master AI Developers & Agents

1. **Clean-Room Authoring**: All new skills, pipeline manifests, and orchestrator scripts must be written originally by Master AI.
2. **Attribution**: Where third-party open-source libraries (e.g. `imageio_ffmpeg`, `fitz / pymupdf`, `opencv-python`, `yt-dlp`) are utilized as runtime dependencies, their respective licenses (LGPL, AGPL, Apache 2.0, Unlicense) are respected via subprocess isolation and dynamic linking.
3. **Subprocess Boundary Isolation**: When calling external CLI utilities (e.g. `ffmpeg`, `yt-dlp`), communication is conducted strictly across operating system process boundaries (stdin/stdout pipe or command line invocation), maintaining legal separation from Master AI's core codebase.
