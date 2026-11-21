"""orchestrator_router.py
MASTER-AI Autonomous Multi-Agent Orchestration REST API Router

Exposes endpoints for goals, DAG planning, workflow execution controls,
checkpoint management, agent health, approval tickets, and live tracing.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

# Ensure workspace root is in sys.path
_current_dir = Path(__file__).resolve().parent
_workspace_root = _current_dir.parents[1]
if str(_workspace_root) not in sys.path:
    sys.path.insert(0, str(_workspace_root))

import importlib

# Dynamic module imports for numbered packages
_orch_pkg = importlib.import_module("03_AI_AGENTS.orchestrator")
MasterOrchestrationCore = _orch_pkg.MasterOrchestrationCore
AgentRegistry = _orch_pkg.AgentRegistry

_appr_pkg = importlib.import_module("03_AI_AGENTS.approval_engine.approval_center")
ApprovalCenter = _appr_pkg.ApprovalCenter

router = APIRouter(prefix="/api/v1/orchestrator", tags=["Multi-Agent Orchestration"])

_core_instance: Optional[MasterOrchestrationCore] = None


def get_core() -> MasterOrchestrationCore:
    global _core_instance
    if _core_instance is None:
        _core_instance = MasterOrchestrationCore()
    return _core_instance


# -------------------------------------------------------------
# Request Models
# -------------------------------------------------------------

class GoalSubmissionRequest(BaseModel):
    goal: str = Field(..., description="Natural language goal to plan and execute")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional extra parameters")


class PlanApprovalRequest(BaseModel):
    auth_token: Optional[str] = Field(None, description="Authorization token if plan requires approval")


class WorkflowActionRequest(BaseModel):
    auth_token: Optional[str] = Field(None, description="Optional authorization token")
    reason: Optional[str] = Field(None, description="Reason for the action (e.g. cancellation)")


class ApprovalDecisionRequest(BaseModel):
    action: str = Field(..., description="Decision action: approve, reject, or revoke")
    actor: str = Field("human_operator", description="Actor taking the action")
    reason: str = Field("Manual human review", description="Reason for the decision")


# -------------------------------------------------------------
# Goals & Planning Endpoints
# -------------------------------------------------------------

@router.post("/goals", summary="Submit natural language goal and generate execution plan")
def submit_goal(req: GoalSubmissionRequest) -> Dict[str, Any]:
    core = get_core()
    try:
        plan = core.submit_goal(req.goal, req.context)
        return {"status": "SUCCESS", "plan": plan}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/plans/{plan_id}", summary="Retrieve execution plan by ID")
def get_plan(plan_id: str) -> Dict[str, Any]:
    core = get_core()
    plan = core.get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail=f"Plan '{plan_id}' not found.")
    return {"status": "SUCCESS", "plan": plan}


@router.post("/plans/{plan_id}/approve", summary="Approve execution plan and initialize workflow")
def approve_plan(plan_id: str, req: PlanApprovalRequest) -> Dict[str, Any]:
    core = get_core()
    try:
        wf = core.approve_plan(plan_id, auth_token=req.auth_token)
        return {"status": "SUCCESS", "workflow": wf}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------------------------------------
# Workflow Execution Controls
# -------------------------------------------------------------

@router.post("/workflows/{workflow_id}/start", summary="Start or run workflow to completion")
def start_workflow(workflow_id: str, req: WorkflowActionRequest) -> Dict[str, Any]:
    core = get_core()
    try:
        wf = core.execute_workflow(workflow_id, auth_token=req.auth_token)
        return {"status": "SUCCESS", "workflow": wf}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflows/{workflow_id}/pause", summary="Pause in-flight workflow")
def pause_workflow(workflow_id: str) -> Dict[str, Any]:
    core = get_core()
    try:
        wf = core.pause_workflow(workflow_id)
        return {"status": "SUCCESS", "workflow": wf}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/workflows/{workflow_id}/resume", summary="Resume paused workflow from last checkpoint")
def resume_workflow(workflow_id: str, req: WorkflowActionRequest) -> Dict[str, Any]:
    core = get_core()
    try:
        wf = core.resume_workflow(workflow_id, auth_token=req.auth_token)
        return {"status": "SUCCESS", "workflow": wf}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflows/{workflow_id}/cancel", summary="Cancel workflow execution")
def cancel_workflow(workflow_id: str, req: WorkflowActionRequest) -> Dict[str, Any]:
    core = get_core()
    try:
        wf = core.cancel_workflow(workflow_id, reason=req.reason or "Cancelled by user")
        return {"status": "SUCCESS", "workflow": wf}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/workflows/{workflow_id}/status", summary="Get workflow execution status and DAG details")
def get_workflow_status(workflow_id: str) -> Dict[str, Any]:
    core = get_core()
    try:
        wf = core.get_workflow_status(workflow_id)
        return {"status": "SUCCESS", "workflow": wf}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/workflows/{workflow_id}/trace", summary="Get live secret-scrubbed execution trace")
def get_execution_trace(workflow_id: str) -> Dict[str, Any]:
    core = get_core()
    try:
        trace = core.get_execution_trace(workflow_id)
        return {"status": "SUCCESS", "trace": trace}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflows", summary="List all indexed workflows")
def list_workflows() -> Dict[str, Any]:
    core = get_core()
    wfs = core.lifecycle.list_workflows()
    return {"status": "SUCCESS", "workflows": wfs, "count": len(wfs)}


# -------------------------------------------------------------
# Agent Registry & Health Endpoints
# -------------------------------------------------------------

@router.get("/agents", summary="List all registered agents and their health")
def list_agents() -> Dict[str, Any]:
    core = get_core()
    agents = core.registry.list_agents()
    return {"status": "SUCCESS", "agents": agents, "count": len(agents)}


@router.get("/agents/{agent_id}/health", summary="Get specific agent health and execution metrics")
def get_agent_health(agent_id: str) -> Dict[str, Any]:
    core = get_core()
    spec = core.registry.get_agent(agent_id)
    if not spec:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found.")
    metrics = core.registry.get_agent_metrics(agent_id)
    return {
        "status": "SUCCESS",
        "agent_id": agent_id,
        "name": spec.get("name"),
        "health_status": spec.get("health_status"),
        "metrics": metrics,
        "history": spec.get("execution_history", [])[-10:]
    }


# -------------------------------------------------------------
# Approval Center Endpoints
# -------------------------------------------------------------

@router.get("/approvals", summary="List all approval tickets")
def list_approval_tickets(status: Optional[str] = Query(None, description="Optional status filter")) -> Dict[str, Any]:
    core = get_core()
    tickets = core.approval_center.list_tickets(status=status)
    return {"status": "SUCCESS", "tickets": tickets, "count": len(tickets)}


@router.post("/approvals/{ticket_id}/action", summary="Approve, reject, or revoke an approval ticket")
def handle_approval_action(ticket_id: str, req: ApprovalDecisionRequest) -> Dict[str, Any]:
    core = get_core()
    try:
        if req.action.lower() == "approve":
            tkt = core.approval_center.approve_ticket(ticket_id, actor=req.actor, reason=req.reason)
        elif req.action.lower() == "reject":
            tkt = core.approval_center.reject_ticket(ticket_id, actor=req.actor, reason=req.reason)
        elif req.action.lower() == "revoke":
            tkt = core.approval_center.revoke_ticket(ticket_id, actor=req.actor, reason=req.reason)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid action '{req.action}'.")
        return {"status": "SUCCESS", "ticket": tkt}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------------------------------------
# Framework Evaluation
# -------------------------------------------------------------

@router.get("/evaluation/langgraph", summary="Get LangGraph compatibility evaluation on Windows 11")
def evaluate_langgraph() -> Dict[str, Any]:
    core = get_core()
    return core.evaluate_langgraph_integration()
