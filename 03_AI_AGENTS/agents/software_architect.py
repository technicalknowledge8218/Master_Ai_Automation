"""
software_architect.py
MASTER-AI Software Architecture Specialist (AGT-002)

Designs modular system architectures, decouples presentation/application/domain/infrastructure,
and outputs verified system specifications validated against validate_system_spec.py.
"""

import os
import json
from typing import Dict, Any, List
from .base_agent import BaseSpecialistAgent, TaskSandbox

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SPEC_VALIDATOR = os.path.join(
    WORKSPACE_ROOT, "02_SKILLS", "software-architecture", "scripts", "validate_system_spec.py"
)


class SoftwareArchitect(BaseSpecialistAgent):
    def __init__(self, approval_engine=None):
        super().__init__("software_architect.json", approval_engine)

    def execute_task(self, request: Dict[str, Any], sandbox: TaskSandbox) -> Dict[str, Any]:
        params = request.get("parameters", {})
        system_name = params.get("system_name", "DisposableModule")
        pattern = params.get("pattern", "Modular Three-Tier")

        spec_content = {
            "system_name": system_name,
            "pattern": pattern,
            "layers": [
                {
                    "name": "presentation",
                    "modules": [f"{system_name.lower()}_api", "cli_router"],
                    "responsibilities": "HTTP routing, input serialization, status code mapping"
                },
                {
                    "name": "domain",
                    "modules": [f"{system_name.lower()}_service", "entity_validator"],
                    "responsibilities": "Pure business logic, state machine enforcement, calculation"
                },
                {
                    "name": "infrastructure",
                    "modules": [f"{system_name.lower()}_repo", "file_storage"],
                    "responsibilities": "Persistence, database interaction, filesystem caching"
                }
            ]
        }

        spec_filename = "system_architecture_spec.json"
        sandbox.write_file(spec_filename, json.dumps(spec_content, indent=2))
        sha = sandbox.compute_file_sha256(spec_filename)

        # Validate spec using existing companion validator
        val_code, val_out, val_err = sandbox.run_subprocess([
            "python", SPEC_VALIDATOR, "--spec", os.path.join(sandbox.sandbox_dir, spec_filename)
        ])

        spec_passed = (val_code == 0)

        artifacts = [{
            "artifact_id": "ART-ARCH-001",
            "artifact_type": "json",
            "path": spec_filename,
            "sha256": sha
        }]

        evidence = {
            "system_name": system_name,
            "pattern": pattern,
            "layers_count": len(spec_content["layers"]),
            "spec_validator_exit_code": val_code
        }

        tests_executed = [{
            "test_name": "SystemSpecValidator",
            "passed": spec_passed,
            "output": val_out or val_err
        }]

        status = "SUCCESS" if spec_passed else "FAILURE"

        return self._build_success_response(
            task_id=request["task_id"],
            subtask_id=request["subtask_id"],
            work_performed=f"Designed {pattern} architecture for {system_name} and validated against architectural constraints.",
            files_changed=[spec_filename],
            evidence=evidence,
            tests_executed=tests_executed,
            remaining_limitations=[],
            artifacts=artifacts
        ) if spec_passed else self._build_failure_response(
            task_id=request["task_id"],
            subtask_id=request["subtask_id"],
            reason=f"Specification validation failed: {val_err}"
        )
