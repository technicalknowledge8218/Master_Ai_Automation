"""Master AI - Master FastAPI Application.

Serves the Central Intelligence API, Health Diagnostics, System Information,
and Dashboard Backend Endpoints.
"""

from __future__ import annotations

import importlib
import os
import platform
import sys
from pathlib import Path
from typing import Any, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure workspace root is in sys.path
_current_dir = Path(__file__).resolve().parent
_workspace_root = _current_dir.parents[1]
if str(_workspace_root) not in sys.path:
    sys.path.insert(0, str(_workspace_root))

try:
    _path_config = importlib.import_module("00_CORE_SYSTEM.config.path_config")
    WORKSPACE_ROOT = _path_config.WORKSPACE_ROOT
except Exception:
    WORKSPACE_ROOT = Path(os.getenv("MASTER_AI_ROOT", str(_workspace_root)))

# Import Intelligence, RAG, Discovery, and Orchestrator Routers dynamically
_llm_api_mod = importlib.import_module("04_LLM_AND_AI.api.llm_router")
intelligence_router = _llm_api_mod.router

_rag_api_mod = importlib.import_module("04_LLM_AND_AI.api.rag_router")
rag_router = _rag_api_mod.router

_disc_api_mod = importlib.import_module("00_CORE_SYSTEM.api.discovery_router")
discovery_router = _disc_api_mod.router

_orch_api_mod = importlib.import_module("00_CORE_SYSTEM.api.orchestrator_router")
orchestrator_router = _orch_api_mod.router

_studio_api_mod = importlib.import_module("00_CORE_SYSTEM.api.content_studio_router")
content_studio_router = _studio_api_mod.router

app = FastAPI(
    title="Master AI Sovereign Intelligence API",
    description="Autonomous multi-agent orchestration, model routing, and local AI management API.",
    version="2.0.0",
)

# CORS configuration for local dashboard access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Intelligence, RAG, Discovery, Orchestrator, and Content Studio routers
app.include_router(intelligence_router)
app.include_router(rag_router)
app.include_router(discovery_router)
app.include_router(orchestrator_router)
app.include_router(content_studio_router)


@app.get("/health")
def root_health() -> Dict[str, Any]:
    """Root health check endpoint."""
    return {
        "status": "healthy",
        "service": "master-ai-core",
        "workspace_root": str(WORKSPACE_ROOT),
        "architecture": "cpu-first-win32",
    }


@app.get("/api/v1/system/info")
def system_info() -> Dict[str, Any]:
    """Retrieve runtime host and storage metrics."""
    return {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python_version": sys.version.split()[0],
        "workspace_root": str(WORKSPACE_ROOT),
        "virtual_environment": str(WORKSPACE_ROOT / ".venv"),
        "docker_disabled": True,
        "wsl2_disabled": True,
    }


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
