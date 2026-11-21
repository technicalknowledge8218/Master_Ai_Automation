"""
GitHub Discovery & Skills Intelligence REST API for Master AI
=============================================================
FastAPI endpoints for repository catalog querying, evaluation scoring,
capability gap analysis, skills lifecycle, and governed integration workflows.
"""

from __future__ import annotations

import importlib
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

disc_mod = importlib.import_module("00_CORE_SYSTEM.discovery_engine")

router = APIRouter(tags=["GitHub Discovery & Skills Intelligence"])

# Shared singletons
_catalog_mgr = disc_mod.RepositoryCatalogManager()
_evaluator = disc_mod.RepositoryEvaluator()
_gap_engine = disc_mod.CapabilityGapEngine()
_skills_engine = disc_mod.SkillsIntelligenceEngine()
_workflow_engine = disc_mod.GovernedIntegrationWorkflow()
_scheduler = disc_mod.DiscoveryScheduler()
_discovery = disc_mod.GitHubDiscoveryEngine()


# Schemas
class SearchRequest(BaseModel):
    query: str
    sort: str = "stars"
    order: str = "desc"
    per_page: int = 10
    page: int = 1


class EvaluateRequest(BaseModel):
    full_name: str
    readme_text: str = ""
    dependency_text: str = ""
    sample_code: str = ""


class ScaffoldSkillRequest(BaseModel):
    skill_id: str
    name: str
    description: str
    domain_id: str = "DOM-01"
    source_repo: str = "custom"
    instructions_body: str = ""


class PromoteSkillRequest(BaseModel):
    skill_id: str
    approval_token: str
    approver: str = "human_operator"


class StartWorkflowRequest(BaseModel):
    repo_full_name: str
    test_script_content: Optional[str] = None


class ApproveWorkflowRequest(BaseModel):
    candidate_id: str
    approval_token: str
    approver: str = "human_operator"
    target_skill_name: Optional[str] = None


# Endpoints
@router.get("/api/v1/discovery/catalog")
def list_catalog(
    category: Optional[str] = Query(None),
    min_stars: int = Query(0),
    language: Optional[str] = Query(None),
    permissive_only: bool = Query(False),
    min_score: int = Query(0),
) -> Dict[str, Any]:
    """Query the 100+ curated repository catalog."""
    repos = _catalog_mgr.list_repositories(
        category=category,
        min_stars=min_stars,
        language=language,
        permissive_only=permissive_only,
        min_score=min_score,
    )
    return {
        "total_catalogued": _catalog_mgr.total_repositories,
        "returned": len(repos),
        "categories": _catalog_mgr.get_categories(),
        "repositories": repos,
    }


@router.post("/api/v1/discovery/search")
def search_repositories(req: SearchRequest) -> Dict[str, Any]:
    """Search repositories online or via offline fallback."""
    return _discovery.search_repositories(
        query=req.query,
        sort=req.sort,
        order=req.order,
        per_page=req.per_page,
        page=req.page,
    )


@router.post("/api/v1/discovery/evaluate")
def evaluate_repository(req: EvaluateRequest) -> Dict[str, Any]:
    """Execute 8-dimensional scoring on repository metadata."""
    meta = _discovery.get_repository_details(req.full_name)
    extracted = _discovery.extract_metadata(meta)
    scorecard = _evaluator.evaluate_repository(
        repo_metadata=extracted,
        readme_text=req.readme_text,
        dependency_text=req.dependency_text,
        sample_code=req.sample_code,
    )
    return scorecard.to_dict()


@router.get("/api/v1/discovery/gaps")
def get_capability_gaps() -> Dict[str, Any]:
    """Retrieve 30-domain capability gap analysis."""
    return _gap_engine.analyze_gaps()


@router.get("/api/v1/discovery/roadmap")
def get_capability_roadmap() -> Dict[str, Any]:
    """Return rendered capability roadmap."""
    md = _gap_engine.generate_roadmap_markdown()
    return {"roadmap_markdown": md}


@router.get("/api/v1/discovery/scheduler/status")
def scheduler_status() -> Dict[str, Any]:
    """Get status of discovery cycle scheduler."""
    return _scheduler.get_status()


@router.post("/api/v1/discovery/scheduler/run")
def run_scheduler_cycle() -> Dict[str, Any]:
    """Manually trigger discovery cycle."""
    return _scheduler.run_discovery_cycle()


@router.get("/api/v1/skills/active")
def list_active_skills() -> Dict[str, Any]:
    """List production active skills."""
    skills = _skills_engine.list_active_skills()
    return {"total_active": len(skills), "skills": skills}


@router.get("/api/v1/skills/candidates")
def list_candidate_skills() -> Dict[str, Any]:
    """List staged candidate skills awaiting evaluation."""
    candidates = _skills_engine.list_candidate_skills()
    return {"total_candidates": len(candidates), "candidates": candidates}


@router.post("/api/v1/skills/scaffold")
def scaffold_skill(req: ScaffoldSkillRequest) -> Dict[str, Any]:
    """Scaffold a new candidate skill in staging."""
    res = _skills_engine.scaffold_candidate_skill(
        skill_id=req.skill_id,
        name=req.name,
        description=req.description,
        domain_id=req.domain_id,
        source_repo=req.source_repo,
        instructions_body=req.instructions_body,
    )
    return res


@router.post("/api/v1/skills/promote")
def promote_skill(req: PromoteSkillRequest) -> Dict[str, Any]:
    """Promote candidate skill to production with valid human approval token."""
    try:
        return _skills_engine.promote_candidate_to_production(
            skill_id=req.skill_id,
            approval_token=req.approval_token,
            approver=req.approver,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/v1/workflow/start")
def start_integration_workflow(req: StartWorkflowRequest) -> Dict[str, Any]:
    """Start 8-stage integration pipeline for candidate repository."""
    state = _workflow_engine.start_pipeline(
        repo_full_name=req.repo_full_name,
        test_script_content=req.test_script_content,
    )
    return state.to_dict()


@router.post("/api/v1/workflow/approve")
def approve_workflow(req: ApproveWorkflowRequest) -> Dict[str, Any]:
    """Approve candidate integration with token and complete integration."""
    try:
        state = _workflow_engine.approve_and_integrate(
            candidate_id=req.candidate_id,
            approval_token=req.approval_token,
            approver=req.approver,
            target_skill_name=req.target_skill_name,
        )
        return state.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/v1/workflow/evaluations")
def list_evaluations() -> Dict[str, Any]:
    """List all integration workflow executions."""
    evals = _workflow_engine.list_evaluations()
    return {"total": len(evals), "evaluations": evals}
