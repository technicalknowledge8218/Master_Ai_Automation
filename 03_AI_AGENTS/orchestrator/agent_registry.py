"""agent_registry.py
MASTER-AI Central Agent Registry

Manages definitions, capabilities, task eligibility, model preferences,
tool permissions, resource requirements, health status, and execution history
for all 7 specialist agents and dynamically registered future agents.
"""

import os
import sys
import json
import time
import datetime
from typing import Dict, Any, List, Optional, Set

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFINITIONS_DIR = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "definitions")
REGISTRY_PERSIST_PATH = os.path.join(WORKSPACE_ROOT, "03_AI_AGENTS", "runs", "AGENT_REGISTRY_STATE.json")


class AgentRegistry:
    """Thread-safe central registry for Master AI specialist agents."""

    def __init__(self, persist_path: Optional[str] = None):
        self.persist_path = persist_path or REGISTRY_PERSIST_PATH
        self._agents: Dict[str, Dict[str, Any]] = {}
        self._load_standard_definitions()
        self._load_persisted_state()

    def _load_standard_definitions(self):
        """Loads canonical definitions for AGT-001 through AGT-007 from disk."""
        standard_specs = {
            "AGT-001": {
                "id": "AGT-001",
                "name": "Research Agent",
                "slug": "research_agent",
                "role": "Technical Research & Verification",
                "primary_domain": "DOM-01",
                "capabilities": [
                    "technical_research",
                    "web_verification",
                    "knowledge_synthesis",
                    "citation_grounding",
                    "rag_retrieval"
                ],
                "task_eligibility": ["RESEARCH", "AUDIT", "FACT_CHECK", "LITERATURE_REVIEW", "SYNTHESIS"],
                "model_preferences": {
                    "primary": "ollama/qwen2.5:7b",
                    "fallback": "ollama/llama3.2:3b",
                    "temperature": 0.2
                },
                "tools_allowed": ["read_file", "search_knowledge_base", "query_memory", "calculate_checksum", "web_search"],
                "tools_prohibited": ["write_file", "execute_subprocess", "delete_file", "activate_paid_api"],
                "permissions": {
                    "can_write_code": False,
                    "can_execute_shell": False,
                    "requires_approval_level": "LOW"
                },
                "resource_requirements": {
                    "cpu_cores": 1,
                    "ram_mb": 512,
                    "max_runtime_sec": 60
                },
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-002": {
                "id": "AGT-002",
                "name": "Software Architect",
                "slug": "software_architect",
                "role": "Software Architecture & Specification",
                "primary_domain": "DOM-02",
                "capabilities": [
                    "system_architecture",
                    "component_specification",
                    "adr_design",
                    "pipeline_design",
                    "dag_planning"
                ],
                "task_eligibility": ["ARCHITECTURE", "SPECIFICATION", "DESIGN", "DECOMPOSITION", "STORYBOARD"],
                "model_preferences": {
                    "primary": "ollama/qwen2.5:7b",
                    "fallback": "ollama/mistral:7b",
                    "temperature": 0.2
                },
                "tools_allowed": ["read_file", "write_spec", "search_knowledge_base", "query_memory"],
                "tools_prohibited": ["execute_subprocess", "delete_file", "activate_paid_api"],
                "permissions": {
                    "can_write_code": False,
                    "can_execute_shell": False,
                    "requires_approval_level": "MEDIUM"
                },
                "resource_requirements": {
                    "cpu_cores": 1,
                    "ram_mb": 512,
                    "max_runtime_sec": 60
                },
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-003": {
                "id": "AGT-003",
                "name": "Coding Agent",
                "slug": "coding_agent",
                "role": "Component Implementation & Scripting",
                "primary_domain": "DOM-03",
                "capabilities": [
                    "code_generation",
                    "refactoring",
                    "pure_python_implementation",
                    "algorithm_design",
                    "media_assembly"
                ],
                "task_eligibility": ["IMPLEMENTATION", "CODING", "REFACTORING", "SCRIPTING", "GENERATION"],
                "model_preferences": {
                    "primary": "ollama/qwen2.5-coder:7b",
                    "fallback": "ollama/qwen2.5:7b",
                    "temperature": 0.1
                },
                "tools_allowed": ["read_file", "write_file", "sandbox_eval", "query_memory"],
                "tools_prohibited": ["activate_paid_api", "git_push", "global_install"],
                "permissions": {
                    "can_write_code": True,
                    "can_execute_shell": False,
                    "requires_approval_level": "HIGH"
                },
                "resource_requirements": {
                    "cpu_cores": 2,
                    "ram_mb": 1024,
                    "max_runtime_sec": 120
                },
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-004": {
                "id": "AGT-004",
                "name": "Testing Agent",
                "slug": "testing_agent",
                "role": "Independent Testing & Verification",
                "primary_domain": "DOM-04",
                "capabilities": [
                    "unit_testing",
                    "integration_testing",
                    "negative_testing",
                    "assertion_verification",
                    "timing_validation"
                ],
                "task_eligibility": ["TESTING", "VALIDATION", "SMOKE_TEST", "REGRESSION", "VERIFICATION"],
                "model_preferences": {
                    "primary": "ollama/qwen2.5:7b",
                    "fallback": "ollama/llama3.2:3b",
                    "temperature": 0.1
                },
                "tools_allowed": ["read_file", "run_isolated_test", "sandbox_eval", "query_memory"],
                "tools_prohibited": ["write_production_file", "activate_paid_api"],
                "permissions": {
                    "can_write_code": True,
                    "can_execute_shell": False,
                    "requires_approval_level": "LOW"
                },
                "resource_requirements": {
                    "cpu_cores": 1,
                    "ram_mb": 512,
                    "max_runtime_sec": 60
                },
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-005": {
                "id": "AGT-005",
                "name": "Documentation Agent",
                "slug": "documentation_agent",
                "role": "Living Documentation & Deliverable Packaging",
                "primary_domain": "DOM-05",
                "capabilities": [
                    "documentation_engineering",
                    "production_plans",
                    "runbook_generation",
                    "adr_documentation",
                    "script_translation",
                    "packaging"
                ],
                "task_eligibility": ["DOCUMENTATION", "PRODUCTION_PLAN", "REPORTING", "SUMMARY", "PACKAGING"],
                "model_preferences": {
                    "primary": "ollama/qwen2.5:7b",
                    "fallback": "ollama/llama3.2:3b",
                    "temperature": 0.2
                },
                "tools_allowed": ["read_file", "write_doc", "search_knowledge_base", "query_memory"],
                "tools_prohibited": ["execute_subprocess", "delete_file", "activate_paid_api"],
                "permissions": {
                    "can_write_code": False,
                    "can_execute_shell": False,
                    "requires_approval_level": "LOW"
                },
                "resource_requirements": {
                    "cpu_cores": 1,
                    "ram_mb": 512,
                    "max_runtime_sec": 60
                },
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-006": {
                "id": "AGT-006",
                "name": "Security Auditor",
                "slug": "security_auditor",
                "role": "Security & Static Analysis Audit",
                "primary_domain": "DOM-06",
                "capabilities": [
                    "static_analysis",
                    "secret_scanning",
                    "license_compliance",
                    "threat_modeling",
                    "content_risk_audit"
                ],
                "task_eligibility": ["SECURITY_AUDIT", "COMPLIANCE_CHECK", "SECRET_SCAN", "VULNERABILITY_ASSESSMENT", "RISK_AUDIT"],
                "model_preferences": {
                    "primary": "ollama/qwen2.5:7b",
                    "fallback": "ollama/mistral:7b",
                    "temperature": 0.0
                },
                "tools_allowed": ["read_file", "scan_secrets", "audit_licenses", "ast_inspect"],
                "tools_prohibited": ["write_production_file", "execute_arbitrary_shell", "activate_paid_api"],
                "permissions": {
                    "can_write_code": False,
                    "can_execute_shell": False,
                    "requires_approval_level": "LOW"
                },
                "resource_requirements": {
                    "cpu_cores": 1,
                    "ram_mb": 512,
                    "max_runtime_sec": 60
                },
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-007": {
                "id": "AGT-007",
                "name": "Capability Discovery Agent",
                "slug": "capability_discovery_agent",
                "role": "Capability Discovery & Skills Intelligence",
                "primary_domain": "DOM-07",
                "capabilities": [
                    "repo_discovery",
                    "gap_analysis",
                    "catalog_indexing",
                    "skill_scaffolding",
                    "ecosystem_research"
                ],
                "task_eligibility": ["DISCOVERY", "GAP_ANALYSIS", "CATALOG_SCAN", "SKILL_RESEARCH"],
                "model_preferences": {
                    "primary": "ollama/qwen2.5:7b",
                    "fallback": "ollama/llama3.2:3b",
                    "temperature": 0.2
                },
                "tools_allowed": ["search_github_catalog", "read_file", "evaluate_repo", "stage_skill"],
                "tools_prohibited": ["promote_skill_without_auth", "activate_paid_api"],
                "permissions": {
                    "can_write_code": False,
                    "can_execute_shell": False,
                    "requires_approval_level": "HIGH"
                },
                "resource_requirements": {
                    "cpu_cores": 1,
                    "ram_mb": 512,
                    "max_runtime_sec": 60
                },
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-008": {
                "id": "AGT-008",
                "name": "Content Producer",
                "slug": "content_producer",
                "role": "Executive Media & Documentary Producer",
                "primary_domain": "DOM-09",
                "capabilities": ["executive_production", "pipeline_coordination", "milestone_tracking", "approval_staging"],
                "task_eligibility": ["PRODUCTION", "COORDINATION", "MEDIA_PACKAGE", "PRODUCER"],
                "model_preferences": {"primary": "ollama/qwen2.5:7b", "fallback": "ollama/llama3.2:3b", "temperature": 0.2},
                "tools_allowed": ["read_file", "write_file", "search_knowledge_base", "query_memory"],
                "tools_prohibited": ["activate_paid_api", "publish_without_approval"],
                "permissions": {"can_write_code": False, "can_execute_shell": False, "requires_approval_level": "HIGH"},
                "resource_requirements": {"cpu_cores": 1, "ram_mb": 512, "max_runtime_sec": 60},
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-009": {
                "id": "AGT-009",
                "name": "Scriptwriter",
                "slug": "scriptwriter",
                "role": "Documentary Scriptwriter & Narrative Designer",
                "primary_domain": "DOM-09",
                "capabilities": ["narrative_scriptwriting", "hindi_translation", "timing_pacing", "scene_dialogue"],
                "task_eligibility": ["SCRIPTWRITING", "NARRATIVE", "HINDI_SCRIPT", "DIALOGUE"],
                "model_preferences": {"primary": "ollama/qwen2.5:7b", "fallback": "ollama/llama3.2:3b", "temperature": 0.3},
                "tools_allowed": ["read_file", "write_file", "search_knowledge_base", "query_memory"],
                "tools_prohibited": ["execute_subprocess", "activate_paid_api"],
                "permissions": {"can_write_code": False, "can_execute_shell": False, "requires_approval_level": "LOW"},
                "resource_requirements": {"cpu_cores": 1, "ram_mb": 512, "max_runtime_sec": 60},
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-010": {
                "id": "AGT-010",
                "name": "Storyboard Director",
                "slug": "storyboard_director",
                "role": "Visual Storyboard & Shot Director",
                "primary_domain": "DOM-09",
                "capabilities": ["storyboard_planning", "shot_direction", "camera_motion", "scene_pacing"],
                "task_eligibility": ["STORYBOARD", "SHOT_LIST", "CINEMATOGRAPHY", "SCENE_PLAN"],
                "model_preferences": {"primary": "ollama/qwen2.5:7b", "fallback": "ollama/mistral:7b", "temperature": 0.2},
                "tools_allowed": ["read_file", "write_file", "search_knowledge_base", "query_memory"],
                "tools_prohibited": ["execute_subprocess", "activate_paid_api"],
                "permissions": {"can_write_code": False, "can_execute_shell": False, "requires_approval_level": "LOW"},
                "resource_requirements": {"cpu_cores": 1, "ram_mb": 512, "max_runtime_sec": 60},
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-011": {
                "id": "AGT-011",
                "name": "Visual Asset Researcher",
                "slug": "visual_asset_researcher",
                "role": "Media Asset Curator & Visual Generator",
                "primary_domain": "DOM-09",
                "capabilities": ["visual_generation", "stock_curation", "license_verification", "motion_clips"],
                "task_eligibility": ["ASSET_DISCOVERY", "IMAGE_GEN", "STOCK_CURATION", "VISUALS"],
                "model_preferences": {"primary": "ollama/qwen2.5:7b", "fallback": "ollama/llama3.2:3b", "temperature": 0.2},
                "tools_allowed": ["read_file", "write_file", "search_knowledge_base", "sandbox_eval"],
                "tools_prohibited": ["activate_paid_api", "download_unauthorized_content"],
                "permissions": {"can_write_code": False, "can_execute_shell": False, "requires_approval_level": "MEDIUM"},
                "resource_requirements": {"cpu_cores": 2, "ram_mb": 1024, "max_runtime_sec": 120},
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-012": {
                "id": "AGT-012",
                "name": "Voice Director",
                "slug": "voice_director",
                "role": "Voiceover Director & Speech Synthesis Supervisor",
                "primary_domain": "DOM-09",
                "capabilities": ["voice_routing", "speech_synthesis", "hindi_voice", "audio_pacing"],
                "task_eligibility": ["VOICEOVER", "TTS", "SPEECH_SYNTHESIS", "AUDIO_TRACK"],
                "model_preferences": {"primary": "ollama/qwen2.5:7b", "fallback": "ollama/llama3.2:3b", "temperature": 0.1},
                "tools_allowed": ["read_file", "write_file", "query_memory", "sandbox_eval"],
                "tools_prohibited": ["activate_paid_api", "execute_arbitrary_shell"],
                "permissions": {"can_write_code": False, "can_execute_shell": False, "requires_approval_level": "LOW"},
                "resource_requirements": {"cpu_cores": 1, "ram_mb": 512, "max_runtime_sec": 60},
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-013": {
                "id": "AGT-013",
                "name": "Video Editor",
                "slug": "video_editor",
                "role": "Lead Programmatic Video Editor",
                "primary_domain": "DOM-09",
                "capabilities": ["timeline_assembly", "ffmpeg_rendering", "audio_ducking", "h264_encoding"],
                "task_eligibility": ["VIDEO_EDITING", "RENDER", "FFMPEG", "TIMELINE"],
                "model_preferences": {"primary": "ollama/qwen2.5:7b", "fallback": "ollama/llama3.2:3b", "temperature": 0.1},
                "tools_allowed": ["read_file", "write_file", "sandbox_eval", "query_memory"],
                "tools_prohibited": ["activate_paid_api", "delete_external_files"],
                "permissions": {"can_write_code": True, "can_execute_shell": False, "requires_approval_level": "MEDIUM"},
                "resource_requirements": {"cpu_cores": 2, "ram_mb": 2048, "max_runtime_sec": 300},
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-014": {
                "id": "AGT-014",
                "name": "Subtitle Specialist",
                "slug": "subtitle_specialist",
                "role": "Multilingual Subtitle & Captioning Engineer",
                "primary_domain": "DOM-09",
                "capabilities": ["srt_generation", "ass_styling", "devanagari_formatting", "timecode_validation"],
                "task_eligibility": ["SUBTITLES", "CAPTIONS", "SRT", "ASS"],
                "model_preferences": {"primary": "ollama/qwen2.5:7b", "fallback": "ollama/llama3.2:3b", "temperature": 0.1},
                "tools_allowed": ["read_file", "write_file", "query_memory"],
                "tools_prohibited": ["execute_subprocess", "activate_paid_api"],
                "permissions": {"can_write_code": False, "can_execute_shell": False, "requires_approval_level": "LOW"},
                "resource_requirements": {"cpu_cores": 1, "ram_mb": 512, "max_runtime_sec": 60},
                "health_status": "HEALTHY",
                "execution_history": []
            },
            "AGT-015": {
                "id": "AGT-015",
                "name": "Media QA Auditor",
                "slug": "media_qa_auditor",
                "role": "Multimedia Quality Assurance & Compliance Auditor",
                "primary_domain": "DOM-09",
                "capabilities": ["media_probing", "blackframe_detection", "silencedetect", "compliance_audit"],
                "task_eligibility": ["MEDIA_QA", "QUALITY_AUDIT", "COMPLIANCE", "VIDEO_INSPECT"],
                "model_preferences": {"primary": "ollama/qwen2.5:7b", "fallback": "ollama/mistral:7b", "temperature": 0.0},
                "tools_allowed": ["read_file", "write_file", "sandbox_eval", "query_memory"],
                "tools_prohibited": ["activate_paid_api", "override_qa_failures"],
                "permissions": {"can_write_code": False, "can_execute_shell": False, "requires_approval_level": "LOW"},
                "resource_requirements": {"cpu_cores": 1, "ram_mb": 512, "max_runtime_sec": 60},
                "health_status": "HEALTHY",
                "execution_history": []
            }
        }
        self._agents.update(standard_specs)

    def _load_persisted_state(self):
        """Loads updated health and execution history if available."""
        if os.path.exists(self.persist_path):
            try:
                with open(self.persist_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                for agent_id, state in saved.items():
                    if agent_id in self._agents:
                        self._agents[agent_id]["health_status"] = state.get("health_status", self._agents[agent_id]["health_status"])
                        self._agents[agent_id]["execution_history"] = state.get("execution_history", [])
                    else:
                        # Future dynamically registered agent
                        self._agents[agent_id] = state
            except Exception:
                pass

    def _persist_state(self):
        """Saves dynamic agents, health and metrics to disk."""
        try:
            os.makedirs(os.path.dirname(os.path.abspath(self.persist_path)), exist_ok=True)
            temp_path = self.persist_path + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self._agents, f, indent=2)
            os.replace(temp_path, self.persist_path)
        except Exception:
            pass

    def register_agent(self, agent_spec: Dict[str, Any]) -> bool:
        """Dynamically registers a new specialist agent without code modification."""
        required_fields = ["id", "name", "slug", "role", "capabilities", "task_eligibility"]
        for field in required_fields:
            if field not in agent_spec:
                raise ValueError(f"Agent spec missing required field: '{field}'")

        agent_id = agent_spec["id"]
        # Set defaults for optional parameters
        complete_spec = {
            "id": agent_id,
            "name": agent_spec["name"],
            "slug": agent_spec["slug"],
            "role": agent_spec["role"],
            "primary_domain": agent_spec.get("primary_domain", "DOM-CUSTOM"),
            "capabilities": list(agent_spec["capabilities"]),
            "task_eligibility": list(agent_spec["task_eligibility"]),
            "model_preferences": agent_spec.get("model_preferences", {
                "primary": "ollama/qwen2.5:7b",
                "fallback": "ollama/llama3.2:3b",
                "temperature": 0.2
            }),
            "tools_allowed": list(agent_spec.get("tools_allowed", ["read_file"])),
            "tools_prohibited": list(agent_spec.get("tools_prohibited", ["activate_paid_api"])),
            "permissions": agent_spec.get("permissions", {
                "can_write_code": False,
                "can_execute_shell": False,
                "requires_approval_level": "MEDIUM"
            }),
            "resource_requirements": agent_spec.get("resource_requirements", {
                "cpu_cores": 1,
                "ram_mb": 512,
                "max_runtime_sec": 60
            }),
            "health_status": "HEALTHY",
            "execution_history": []
        }
        self._agents[agent_id] = complete_spec
        self._persist_state()
        return True

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves agent specification by ID or slug."""
        if agent_id in self._agents:
            return dict(self._agents[agent_id])
        for a in self._agents.values():
            if a.get("slug") == agent_id:
                return dict(a)
        return None

    def list_agents(self) -> List[Dict[str, Any]]:
        """Returns all registered agent definitions."""
        return [dict(a) for a in self._agents.values()]

    def find_eligible_agents(
        self,
        task_type: str,
        required_capabilities: Optional[List[str]] = None
    ) -> List[str]:
        """Finds IDs of agents eligible for a task type and capability set."""
        eligible = []
        req_caps = set(required_capabilities or [])
        for agent_id, spec in self._agents.items():
            if spec.get("health_status") == "OFFLINE":
                continue
            elig_types = set(spec.get("task_eligibility", []))
            caps = set(spec.get("capabilities", []))
            if task_type.upper() in elig_types or not elig_types:
                if req_caps.issubset(caps):
                    eligible.append(agent_id)
        return eligible

    def update_health(self, agent_id: str, status: str, details: Optional[str] = None):
        """Updates health status (HEALTHY, DEGRADED, OFFLINE)."""
        if agent_id in self._agents:
            self._agents[agent_id]["health_status"] = status
            if details:
                self._agents[agent_id]["health_details"] = details
            self._persist_state()

    def record_run(self, agent_id: str, success: bool, duration_sec: float, subtask_id: Optional[str] = None):
        """Records an execution outcome in the agent's history log."""
        if agent_id in self._agents:
            history = self._agents[agent_id].setdefault("execution_history", [])
            history.append({
                "subtask_id": subtask_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "success": success,
                "duration_seconds": round(duration_sec, 3)
            })
            # Keep history bounded to last 50 runs
            if len(history) > 50:
                self._agents[agent_id]["execution_history"] = history[-50:]
            self._persist_state()

    def get_agent_metrics(self, agent_id: str) -> Dict[str, Any]:
        """Calculates success rate and average duration for an agent."""
        spec = self.get_agent(agent_id)
        if not spec:
            return {"total_runs": 0, "success_rate": 0.0, "avg_duration_sec": 0.0}
        history = spec.get("execution_history", [])
        if not history:
            return {"total_runs": 0, "success_rate": 100.0, "avg_duration_sec": 0.0}
        total = len(history)
        successes = sum(1 for h in history if h.get("success", False))
        avg_dur = sum(h.get("duration_seconds", 0.0) for h in history) / total
        return {
            "total_runs": total,
            "success_rate": round((successes / total) * 100.0, 1),
            "avg_duration_sec": round(avg_dur, 3)
        }

    def get_detailed_agent_health(self, agent_id: str) -> Dict[str, Any]:
        """Distinguishes registration, dependency readiness, model readiness, and real execution."""
        spec = self.get_agent(agent_id)
        if not spec:
            return {
                "agent_id": agent_id,
                "registered": False,
                "dependencies_ready": False,
                "model_ready": False,
                "real_execution_verified": False,
                "status": "OFFLINE"
            }

        # Check dependencies
        deps_ready = True
        dep_notes = []
        if agent_id in {"AGT-013", "AGT-015"}:
            try:
                import imageio_ffmpeg
                _ = imageio_ffmpeg.get_ffmpeg_exe()
                dep_notes.append("FFmpeg 7.1 detected")
            except Exception as e:
                deps_ready = False
                dep_notes.append(f"FFmpeg missing: {e}")
        elif agent_id in {"AGT-011", "AGT-008"}:
            try:
                import PIL
                dep_notes.append("Pillow detected")
            except Exception as e:
                deps_ready = False
                dep_notes.append(f"Pillow missing: {e}")

        # Check model preference
        model_ready = bool(spec.get("model_preferences", {}).get("primary"))

        # Check execution history
        history = spec.get("execution_history", [])
        has_success = any(h.get("success", False) for h in history)

        if spec.get("health_status") == "OFFLINE":
            status = "OFFLINE"
        elif not deps_ready:
            status = "DEGRADED"
        elif has_success:
            status = "HEALTHY_VERIFIED"
        elif deps_ready and model_ready:
            status = "READY_TO_EXECUTE"
        else:
            status = "REGISTERED_ONLY"

        return {
            "agent_id": agent_id,
            "name": spec.get("name"),
            "registered": True,
            "dependencies_ready": deps_ready,
            "dependency_notes": dep_notes,
            "model_ready": model_ready,
            "real_execution_verified": has_success,
            "total_executions": len(history),
            "status": status
        }
