"""Master AI - Intelligence & LLM Management REST API Router.

Exposes production endpoints for Model Registry, Provider Management,
Intelligent Routing, Agent Model Assignments, Benchmarking, and Local Ollama Management.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

# Ensure workspace root is in sys.path
_current_dir = Path(__file__).resolve().parent
_workspace_root = _current_dir.parents[1]
if str(_workspace_root) not in sys.path:
    sys.path.insert(0, str(_workspace_root))

import importlib

_llm_pkg = importlib.import_module("04_LLM_AND_AI.llm_manager")
AgentModelAssignmentManager = _llm_pkg.AgentModelAssignmentManager
BenchmarkEngine = _llm_pkg.BenchmarkEngine
LocalModelManager = _llm_pkg.LocalModelManager
ModelProfile = _llm_pkg.ModelProfile
ModelRegistry = _llm_pkg.ModelRegistry
ProviderRegistry = _llm_pkg.ProviderRegistry
IntelligentModelRouter = _llm_pkg.IntelligentModelRouter
RoutingRequest = _llm_pkg.RoutingRequest
SecurityBoundary = _llm_pkg.SecurityBoundary
sanitize_dict = _llm_pkg.sanitize_dict

router = APIRouter(prefix="/api/v1/intelligence", tags=["Intelligence Layer"])

# Singleton manager instances
_model_registry = ModelRegistry()
_provider_registry = ProviderRegistry()
_security = SecurityBoundary()
_router_engine = IntelligentModelRouter(_model_registry, _provider_registry, _security)
_agent_manager = AgentModelAssignmentManager()
_benchmark_engine = BenchmarkEngine(_provider_registry, _model_registry)
_local_manager = LocalModelManager()


# --- Pydantic Request / Response Models ---
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    messages: List[ChatMessage]
    task_type: str = "general"
    intelligence_level: str = "medium"
    preferred_model_id: Optional[str] = None
    backup_model_id: Optional[str] = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=1, le=32768)
    allow_paid_models: bool = False


class ModelStatusUpdateRequest(BaseModel):
    status: str
    make_default: bool = False


class AgentAssignmentUpdateRequest(BaseModel):
    preferred_model_id: Optional[str] = None
    backup_model_id: Optional[str] = None
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = None
    task_specific_overrides: Optional[Dict[str, str]] = None


class BenchmarkRunRequest(BaseModel):
    model_id: str


class LocalModelEstimateRequest(BaseModel):
    parameter_billions: float
    quantization: str = "Q4"


class LocalModelDeleteRequest(BaseModel):
    model_name: str
    explicit_user_approval: bool


# --- API Route Implementations ---

@router.get("/health")
def get_intelligence_health() -> Dict[str, Any]:
    """Diagnostic health summary of all intelligence components."""
    providers_health = _provider_registry.check_health_all()
    models = _model_registry.list_models()
    return sanitize_dict({
        "status": "healthy",
        "default_active_model": _model_registry.default_active_model,
        "enforce_zero_paid_api": _model_registry.enforce_zero_paid_api,
        "total_registered_models": len(models),
        "active_models_count": len([m for m in models if "ACTIVE" in m.status]),
        "providers_health": providers_health,
        "fallback_events_logged": len(_router_engine.fallback_history),
    })


@router.get("/models")
def list_models(
    tier: Optional[str] = None,
    capability: Optional[str] = None,
    active_only: bool = False,
) -> Dict[str, Any]:
    """List registered models with optional capability/tier filtering."""
    models = _model_registry.list_models(tier=tier, capability=capability, active_only=active_only)
    return {
        "count": len(models),
        "models": [m.__dict__ for m in models],
    }


@router.get("/models/{model_id}")
def get_model_profile(model_id: str) -> Dict[str, Any]:
    """Get full profile and constraints for a specific model."""
    profile = _model_registry.get_model(model_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found in registry.")
    return profile.__dict__


@router.post("/models/{model_id}/status")
def update_model_status(model_id: str, req: ModelStatusUpdateRequest) -> Dict[str, Any]:
    """Update activation state of a model or assign it as default."""
    if req.make_default:
        success = _model_registry.set_default_active_model(model_id)
    else:
        success = _model_registry.set_model_status(model_id, req.status)

    if not success:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found.")
    return {"success": True, "model_id": model_id, "status": req.status}


@router.get("/providers")
def list_providers() -> Dict[str, Any]:
    """List all registered providers and availability status."""
    return {"providers": _provider_registry.list_providers()}


@router.get("/providers/health")
def check_all_providers_health() -> Dict[str, Any]:
    """Run real-time reachability checks across all registered providers."""
    return _provider_registry.check_health_all()


@router.post("/chat/completions")
def chat_completion(req: ChatCompletionRequest) -> Dict[str, Any]:
    """Intelligently route and execute chat completion across models."""
    routing_spec = RoutingRequest(
        task_type=req.task_type,
        intelligence_level=req.intelligence_level,
        preferred_model_id=req.preferred_model_id,
        backup_model_id=req.backup_model_id,
        allow_paid_models=req.allow_paid_models,
    )
    raw_messages = [m.model_dump() for m in req.messages]
    try:
        response = _router_engine.execute_completion(
            messages=raw_messages,
            routing_request=routing_spec,
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )
        return sanitize_dict(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/assignments")
def list_agent_model_assignments() -> Dict[str, Any]:
    """List model assignments and generation settings for all agents."""
    return {"assignments": _agent_manager.list_assignments()}


@router.post("/agents/assignments/{agent_slug}")
def update_agent_assignment(agent_slug: str, req: AgentAssignmentUpdateRequest) -> Dict[str, Any]:
    """Update model assignment or generation settings for an agent."""
    updated = _agent_manager.update_assignment(
        agent_slug=agent_slug,
        preferred_model_id=req.preferred_model_id,
        backup_model_id=req.backup_model_id,
        temperature=req.temperature,
        max_output_tokens=req.max_output_tokens,
        task_specific_overrides=req.task_specific_overrides,
    )
    return {"success": True, "assignment": updated.__dict__}


@router.get("/benchmarks")
def list_benchmarks() -> Dict[str, Any]:
    """List all persisted benchmark test reports."""
    reports = _benchmark_engine.list_saved_reports()
    return {"count": len(reports), "reports": reports}


@router.post("/benchmarks/run")
def run_benchmark(req: BenchmarkRunRequest) -> Dict[str, Any]:
    """Run standardized empirical benchmark suite on target model."""
    try:
        report = _benchmark_engine.run_benchmark_for_model(req.model_id)
        return report.__dict__
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/local/models")
def list_local_ollama_models() -> Dict[str, Any]:
    """Discover installed models directly on the local Ollama daemon."""
    models = _local_manager.list_installed_models()
    return {"count": len(models), "installed_models": [m.__dict__ for m in models]}


@router.post("/local/models/estimate")
def estimate_local_model_resources(req: LocalModelEstimateRequest) -> Dict[str, Any]:
    """Estimate RAM and disk requirement before downloading an Ollama model."""
    return _local_manager.estimate_model_resource_needs(
        param_billions=req.parameter_billions,
        quant=req.quantization,
    )


@router.post("/local/models/delete")
def delete_local_ollama_model(req: LocalModelDeleteRequest) -> Dict[str, Any]:
    """Delete an installed model from Ollama only after explicit confirmation."""
    result = _local_manager.delete_model(
        model_name=req.model_name,
        explicit_user_approval=req.explicit_user_approval,
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result


@router.get("/routing/fallback-history")
def get_fallback_history() -> Dict[str, Any]:
    """Retrieve audit history of model fallbacks and routing events."""
    return {"count": len(_router_engine.fallback_history), "history": _router_engine.get_fallback_history()}
