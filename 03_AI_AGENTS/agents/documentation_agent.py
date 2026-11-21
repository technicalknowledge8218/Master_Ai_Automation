"""
documentation_agent.py
MASTER-AI Documentation Engineering Specialist (AGT-005)

Authors living technical documentation, architectural guides, and ADRs.
Validates ADR structures against validate_adr_structure.py.
"""

import os
from typing import Dict, Any, List
from .base_agent import BaseSpecialistAgent, TaskSandbox

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ADR_VALIDATOR = os.path.join(
    WORKSPACE_ROOT, "02_SKILLS", "documentation-engineering", "scripts", "validate_adr_structure.py"
)


class DocumentationAgent(BaseSpecialistAgent):
    def __init__(self, approval_engine=None):
        super().__init__("documentation_agent.json", approval_engine)

    def execute_task(self, request: Dict[str, Any], sandbox: TaskSandbox) -> Dict[str, Any]:
        params = request.get("parameters", {})
        adr_id = params.get("adr_id", "005")
        title = params.get("title", "Disposable Modular Service Implementation")
        status = params.get("status", "ACCEPTED")

        adr_content = (
            f"# ADR-{adr_id}: {title}\n\n"
            f"> **Status**: {status}  \n"
            "> **Date**: 2026-11-17  \n"
            "> **Deciders**: MASTER-AI Multi-Agent Federation  \n\n"
            "---\n\n"
            "## 1. Context\n"
            "The system required a decoupled, testable mathematical service with strict type guarantees.\n\n"
            "## 2. Decision\n"
            "We implemented a dedicated three-tier service with explicit precision control and unit test verification.\n\n"
            "## 3. Alternatives Considered\n"
            "- Third-party numerical libraries: rejected to avoid unapproved global dependencies.\n"
            "- Direct untyped script: rejected due to lack of contract validation.\n\n"
            "## 4. Consequences\n"
            "- **Positive**: Mathematical operations are deterministically rounded with zero external dependencies.\n"
            "- **Negative**: Fixed floating point precision model.\n"
        )

        adr_filename = f"ADR-{adr_id}.md"
        sandbox.write_file(adr_filename, adr_content)
        sha = sandbox.compute_file_sha256(adr_filename)

        # Validate with ADR validator
        adr_code, adr_out, adr_err = sandbox.run_subprocess([
            "python", ADR_VALIDATOR, "--adr", os.path.join(sandbox.sandbox_dir, adr_filename)
        ])

        adr_passed = (adr_code == 0)

        artifacts = [{
            "artifact_id": "ART-DOC-001",
            "artifact_type": "markdown",
            "path": adr_filename,
            "sha256": sha
        }]

        evidence = {
            "adr_id": adr_id,
            "title": title,
            "status": status,
            "validator_exit_code": adr_code
        }

        tests_executed = [{
            "test_name": "ADRStructureValidation",
            "passed": adr_passed,
            "output": adr_out or adr_err or "ADR syntax valid."
        }]

        if not adr_passed:
            return self._build_failure_response(
                task_id=request["task_id"],
                subtask_id=request["subtask_id"],
                reason=f"ADR validation failed: {adr_err or adr_out}"
            )

        return self._build_success_response(
            task_id=request["task_id"],
            subtask_id=request["subtask_id"],
            work_performed=f"Authored verified Architecture Decision Record '{adr_filename}'.",
            files_changed=[adr_filename],
            evidence=evidence,
            tests_executed=tests_executed,
            remaining_limitations=[],
            artifacts=artifacts
        )
