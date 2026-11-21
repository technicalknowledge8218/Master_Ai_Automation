"""
testing_agent.py
MASTER-AI Testing & QA Specialist (AGT-004)

Authors and executes independent positive and negative unit test suites in the sandbox.
Enforces test isolation, assertions, and execution reporting.
"""

import os
from typing import Dict, Any, List
from .base_agent import BaseSpecialistAgent, TaskSandbox


class TestingAgent(BaseSpecialistAgent):
    def __init__(self, approval_engine=None):
        super().__init__("testing_agent.json", approval_engine)

    def execute_task(self, request: Dict[str, Any], sandbox: TaskSandbox) -> Dict[str, Any]:
        params = request.get("parameters", {})
        target_module = params.get("target_module", "sample_service")

        test_code = (
            '"""\n'
            f"test_{target_module}.py\n"
            f"Unit test suite for {target_module}.\n"
            '"""\n\n'
            "import unittest\n"
            f"from {target_module} import CalculatorService\n\n\n"
            "class TestCalculatorService(unittest.TestCase):\n"
            "    def setUp(self):\n"
            "        self.calc = CalculatorService()\n\n"
            "    def test_add_positive(self):\n"
            "        self.assertEqual(self.calc.add(2.5, 3.5), 6.0)\n\n"
            "    def test_multiply_positive(self):\n"
            "        self.assertEqual(self.calc.multiply(4, 5), 20.0)\n\n"
            "    def test_safe_divide_valid(self):\n"
            "        self.assertEqual(self.calc.safe_divide(10, 2), 5.0)\n\n"
            "    def test_safe_divide_zero_negative(self):\n"
            "        with self.assertRaises(ValueError):\n"
            "            self.calc.safe_divide(10, 0)\n\n"
            "    def test_sum_all_empty(self):\n"
            "        self.assertEqual(self.calc.sum_all([]), 0.0)\n\n\n"
            "if __name__ == '__main__':\n"
            "    unittest.main()\n"
        )

        test_filename = f"test_{target_module}.py"
        sandbox.write_file(test_filename, test_code)
        sha = sandbox.compute_file_sha256(test_filename)

        # Execute test suite inside sandbox
        test_code_ret, test_out, test_err = sandbox.run_subprocess([
            "python", "-m", "unittest", test_filename
        ])

        tests_passed = (test_code_ret == 0)

        artifacts = [{
            "artifact_id": "ART-TEST-001",
            "artifact_type": "python",
            "path": test_filename,
            "sha256": sha
        }]

        evidence = {
            "target_module": target_module,
            "unittest_exit_code": test_code_ret,
            "stdout": test_out,
            "stderr": test_err
        }

        tests_executed = [
            {
                "test_name": f"UnitTestSuite_{target_module}",
                "passed": tests_passed,
                "output": test_err or test_out
            }
        ]

        if not tests_passed:
            return self._build_failure_response(
                task_id=request["task_id"],
                subtask_id=request["subtask_id"],
                reason=f"Unit tests failed on {target_module}: {test_err or test_out}"
            )

        return self._build_success_response(
            task_id=request["task_id"],
            subtask_id=request["subtask_id"],
            work_performed=f"Authored and executed 5 unit tests for {target_module} (all assertions passed).",
            files_changed=[test_filename],
            evidence=evidence,
            tests_executed=tests_executed,
            remaining_limitations=[],
            artifacts=artifacts
        )
