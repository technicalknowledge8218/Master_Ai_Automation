"""Master AI - Phase 2 Intelligence & LLM Management Test Suite.

Automated verification covering:
1. Model Registry & Capabilities Validation
2. Provider Adapters (OfflineMock, Ollama, LiteLLM, OpenAI)
3. Offline Mock Completion & Token Streaming
4. Intelligent Routing Decisions by Task Type
5. Zero-Paid-Model Invariant & Security Budget Boundary
6. Provider Failure Simulation & Automatic Fallback Chain
7. Agent Model Assignments & Task Overrides
8. Empirical Benchmark Suite Execution & Persistence
9. Local Ollama Management & Deletion Approval Guard
10. Security Secret Redaction & Audit Logging
11. FastAPI Intelligence Endpoints via TestClient
"""

from __future__ import annotations

import importlib
import json
import os
import sys
import unittest
from pathlib import Path

# Ensure workspace root is in sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

# Import Intelligence Layer modules dynamically
_llm_pkg = importlib.import_module("04_LLM_AND_AI.llm_manager")
ModelRegistry = _llm_pkg.ModelRegistry
ModelProfile = _llm_pkg.ModelProfile
ProviderRegistry = _llm_pkg.ProviderRegistry
IntelligentModelRouter = _llm_pkg.IntelligentModelRouter
RoutingRequest = _llm_pkg.RoutingRequest
AgentModelAssignmentManager = _llm_pkg.AgentModelAssignmentManager
AgentModelConfig = _llm_pkg.AgentModelConfig
BenchmarkEngine = _llm_pkg.BenchmarkEngine
LocalModelManager = _llm_pkg.LocalModelManager
SecurityBoundary = _llm_pkg.SecurityBoundary
redact_secrets = _llm_pkg.redact_secrets
sanitize_dict = _llm_pkg.sanitize_dict


class TestPhase2Intelligence(unittest.TestCase):
    """Rigorous verification suite for Phase 2 Intelligence Layer."""

    def setUp(self) -> None:
        self.model_registry = ModelRegistry()
        self.provider_registry = ProviderRegistry()
        self.security = SecurityBoundary()
        self.router = IntelligentModelRouter(
            self.model_registry, self.provider_registry, self.security
        )
        self.agent_manager = AgentModelAssignmentManager()
        self.benchmark_engine = BenchmarkEngine(
            self.provider_registry, self.model_registry
        )
        self.local_manager = LocalModelManager()

    def test_01_model_registry_profiles_and_validation(self) -> None:
        """Verify model registration, capability flags, and validation rules."""
        models = self.model_registry.list_models()
        self.assertGreaterEqual(len(models), 4)

        mock_model = self.model_registry.get_model("offline-mock-deterministic")
        self.assertIsNotNone(mock_model)
        self.assertEqual(mock_model.pricing_per_1m_input_usd, 0.0)
        self.assertTrue(mock_model.has_capability("structured_json"))
        self.assertTrue(mock_model.has_capability("code_generation"))

        # Validation assertions
        with self.assertRaises(ValueError):
            bad_profile = ModelProfile(
                model_id="", display_name="Bad", provider="Mock"
            )
            bad_profile.validate()

        with self.assertRaises(ValueError):
            bad_pricing = ModelProfile(
                model_id="test-neg",
                display_name="Negative Pricing",
                provider="Mock",
                pricing_per_1m_input_usd=-1.0,
            )
            bad_pricing.validate()

        print("[PASS] Test 01: Model registry profiles, constraints, and validation verified.")

    def test_02_provider_adapters_and_availability(self) -> None:
        """Verify provider adapters instantiate and report correct availability."""
        mock_adapter = self.provider_registry.get_adapter("OfflineMockProvider")
        self.assertIsNotNone(mock_adapter)
        avail, msg = mock_adapter.is_available()
        self.assertTrue(avail)
        self.assertIn("permanently available", msg)

        ollama_adapter = self.provider_registry.get_adapter("OllamaLocal")
        self.assertIsNotNone(ollama_adapter)
        health = ollama_adapter.health_check()
        self.assertIn("status", health)

        litellm_adapter = self.provider_registry.get_adapter("LiteLLMGateway")
        self.assertIsNotNone(litellm_adapter)
        self.assertTrue(litellm_adapter.is_available()[0])

        print("[PASS] Test 02: Provider adapter availability and health reporting verified.")

    def test_03_offline_mock_completion_and_streaming(self) -> None:
        """Verify deterministic responses for general, code, JSON, Hindi, and streaming."""
        adapter = self.provider_registry.get_adapter("OfflineMockProvider")
        self.assertIsNotNone(adapter)

        # Code prompt
        code_res = adapter.generate(
            messages=[{"role": "user", "content": "Write a python function"}],
            model="offline-mock-deterministic",
        )
        code_content = code_res["choices"][0]["message"]["content"]
        self.assertIn("```python", code_content)
        self.assertIn("def ", code_content)

        # Structured JSON prompt
        json_res = adapter.generate(
            messages=[{"role": "user", "content": "Return structured json data"}],
            model="offline-mock-deterministic",
        )
        json_content = json_res["choices"][0]["message"]["content"]
        parsed = json.loads(json_content)
        self.assertEqual(parsed.get("status"), "success")

        # Bilingual Hindi prompt
        hindi_res = adapter.generate(
            messages=[{"role": "user", "content": "नमस्ते, क्या आप हिंदी समझते हैं?"}],
            model="offline-mock-deterministic",
        )
        hindi_content = hindi_res["choices"][0]["message"]["content"]
        self.assertIn("नमस्ते", hindi_content)

        # Streaming check
        stream_chunks = list(
            adapter.generate_stream(
                messages=[{"role": "user", "content": "Stream test"}],
                model="offline-mock-deterministic",
            )
        )
        self.assertGreater(len(stream_chunks), 1)
        self.assertIn("Master AI", "".join(stream_chunks))

        print("[PASS] Test 03: Offline mock deterministic output and streaming verified.")

    def test_04_intelligent_routing_and_task_selection(self) -> None:
        """Verify routing selection matches requested task type and constraints."""
        # Coding request
        code_req = RoutingRequest(task_type="coding", intelligence_level="medium")
        primary_code, _ = self.router.select_model(code_req)
        self.assertIsNotNone(primary_code)

        # General reasoning request
        reason_req = RoutingRequest(task_type="reasoning", intelligence_level="high")
        primary_reason, _ = self.router.select_model(reason_req)
        self.assertIsNotNone(primary_reason)

        # Execution via router
        res = self.router.execute_completion(
            messages=[{"role": "user", "content": "Analyze system requirements"}],
            routing_request=reason_req,
        )
        self.assertIn("choices", res)
        self.assertIn("routing_metadata", res)
        self.assertFalse(res["routing_metadata"]["fallback_triggered"])

        print("[PASS] Test 04: Intelligent task-based routing and selection verified.")

    def test_05_zero_paid_model_invariant(self) -> None:
        """Verify fail-closed zero-paid-model invariant: never silently switch to paid."""
        # When allow_paid_models=False, paid models must NEVER be selected
        req = RoutingRequest(
            task_type="creative",
            intelligence_level="frontier",
            allow_paid_models=False,
        )
        primary, backups = self.router.select_model(req)
        self.assertEqual(primary.pricing_per_1m_input_usd, 0.0)
        for b in backups:
            self.assertEqual(b.pricing_per_1m_input_usd, 0.0)

        # Security boundary rejection
        can_run, reason = self.security.can_invoke_model(
            model_id="gpt-4o",
            estimated_cost_usd=0.05,
            is_local_or_mock=False,
        )
        self.assertFalse(can_run)
        self.assertIn("blocked", reason.lower())

        print("[PASS] Test 05: Zero-paid-model invariant and security boundary verified.")

    def test_06_provider_failure_and_automatic_fallback(self) -> None:
        """Verify automatic fallback when primary model provider fails."""
        # Request with preferred nonexistent or broken provider
        req = RoutingRequest(
            task_type="general",
            preferred_model_id="gemini-1.5-pro",  # Requires unconfigured API key
            allow_paid_models=False,              # Will be blocked by security
            max_retries=1,
        )
        res = self.router.execute_completion(
            messages=[{"role": "user", "content": "Fallback test"}],
            routing_request=req,
        )
        self.assertIn("routing_metadata", res)
        # Verify fallback resolved to offline mock
        resolved = res["routing_metadata"]["resolved_model"]
        self.assertEqual(resolved, "offline-mock-deterministic")
        self.assertGreater(len(self.router.fallback_history), 0)

        last_record = self.router.fallback_history[-1]
        self.assertTrue(last_record.success)
        self.assertEqual(last_record.resolved_model, "offline-mock-deterministic")

        print("[PASS] Test 06: Provider failure simulation and fallback logging verified.")

    def test_07_agent_model_assignments(self) -> None:
        """Verify external agent model configuration without modifying agent source code."""
        agents_expected = [
            "coding_agent",
            "research_agent",
            "software_architect",
            "testing_agent",
            "documentation_agent",
            "security_auditor",
            "capability_discovery_agent",
        ]
        assignments = self.agent_manager.list_assignments()
        self.assertEqual(len(assignments), 7)
        found_slugs = [a["agent_slug"] for a in assignments]
        for slug in agents_expected:
            self.assertIn(slug, found_slugs)

        # Update assignment dynamically
        updated = self.agent_manager.update_assignment(
            agent_slug="coding_agent",
            temperature=0.15,
            task_specific_overrides={"unit_testing": "offline-mock-deterministic"},
        )
        self.assertEqual(updated.temperature, 0.15)
        self.assertEqual(updated.task_specific_overrides.get("unit_testing"), "offline-mock-deterministic")

        # Resolve model for task
        pref, backup = self.agent_manager.resolve_model_for_task("coding_agent", "unit_testing")
        self.assertEqual(pref, "offline-mock-deterministic")

        print("[PASS] Test 07: External agent model assignment and task overrides verified.")

    def test_08_benchmark_engine_execution(self) -> None:
        """Verify standardized benchmark suite execution and result persistence."""
        report = self.benchmark_engine.run_benchmark_for_model("offline-mock-deterministic")
        self.assertIsNotNone(report)
        self.assertEqual(report.model_id, "offline-mock-deterministic")
        self.assertEqual(report.total_tasks, 7)
        self.assertGreaterEqual(report.tasks_passed, 5)
        self.assertIn(report.overall_rating, ["EXCELLENT", "PROFICIENT"])

        # Check report saved to disk
        saved = self.benchmark_engine.list_saved_reports()
        self.assertGreater(len(saved), 0)
        top = saved[0]
        self.assertEqual(top["model_id"], "offline-mock-deterministic")
        self.assertTrue(Path(top["file_path"]).is_file())

        print(f"[PASS] Test 08: Benchmark engine passed {report.tasks_passed}/7 tasks ({report.overall_rating}).")

    def test_09_local_ollama_manager_and_safety(self) -> None:
        """Verify Ollama discovery, estimation, and deletion approval guard."""
        available, msg = self.local_manager.check_daemon()
        self.assertTrue(available)

        # Test estimation
        estimate = self.local_manager.estimate_model_resource_needs(param_billions=1.5, quant="Q4")
        self.assertIn("estimated_disk_gb", estimate)
        self.assertLessEqual(estimate["estimated_disk_gb"], self.local_manager.max_model_size_gb)

        # Oversized model rejection
        oversized = self.local_manager.pull_model(
            model_name="deepseek-671b:latest", estimated_size_gb=400.0
        )
        self.assertFalse(oversized["success"])
        self.assertIn("exceeds safe maximum", oversized["error"])

        # Guarded deletion rejection without explicit approval
        del_fail = self.local_manager.delete_model("qwen2.5:1.5b", explicit_user_approval=False)
        self.assertFalse(del_fail["success"])
        self.assertIn("explicit_user_approval=True is strictly required", del_fail["error"])

        print("[PASS] Test 09: Local Ollama manager discovery and safety boundaries verified.")

    def test_10_security_secret_redaction_and_audit(self) -> None:
        """Verify API key masking in logs and security audit event tracking."""
        # Construct test token via concatenation to avoid static scanner false positives
        test_key = "sk-" + "dummykey1234567890123456789012345678"
        sample_log = f"Error connecting with {test_key} to host."
        redacted = redact_secrets(sample_log)
        self.assertNotIn("sk-abcdef", redacted)
        self.assertIn("[REDACTED_SECRET]", redacted)

        dict_data = {
            "api_key": "secret-token-12345",
            "config": {"auth_token": "token-999", "model": "qwen2.5:1.5b"},
        }
        sanitized = sanitize_dict(dict_data)
        self.assertEqual(sanitized["api_key"], "[REDACTED_KEY_VALUE]")
        self.assertEqual(sanitized["config"]["auth_token"], "[REDACTED_KEY_VALUE]")
        self.assertEqual(sanitized["config"]["model"], "qwen2.5:1.5b")

        # Security event logging
        self.security.log_security_event(
            "TEST_EVENT", {"action": "verify_redaction", "token": "test-sec-token"}
        )
        self.assertTrue(self.security.audit_log_path.is_file())

        print("[PASS] Test 10: Secret redaction in strings/dictionaries and audit trails verified.")

    def test_11_fastapi_intelligence_endpoints(self) -> None:
        """Verify FastAPI REST endpoints via starlette TestClient."""
        from starlette.testclient import TestClient

        main_mod = importlib.import_module("00_CORE_SYSTEM.api.main")
        client = TestClient(main_mod.app)

        # Root Health
        r_root = client.get("/health")
        self.assertEqual(r_root.status_code, 200)

        # Intelligence Health
        r_intel = client.get("/api/v1/intelligence/health")
        self.assertEqual(r_intel.status_code, 200)
        self.assertEqual(r_intel.json().get("status"), "healthy")

        # Models List
        r_models = client.get("/api/v1/intelligence/models")
        self.assertEqual(r_models.status_code, 200)
        self.assertGreaterEqual(r_models.json().get("count", 0), 4)

        # Chat Completion
        r_chat = client.post(
            "/api/v1/intelligence/chat/completions",
            json={
                "messages": [{"role": "user", "content": "Ping API"}],
                "task_type": "general",
            },
        )
        self.assertEqual(r_chat.status_code, 200)
        data = r_chat.json()
        self.assertIn("choices", data)
        self.assertIn("routing_metadata", data)

        # Agent Assignments
        r_assign = client.get("/api/v1/intelligence/agents/assignments")
        self.assertEqual(r_assign.status_code, 200)
        self.assertEqual(len(r_assign.json().get("assignments", [])), 7)

        print("[PASS] Test 11: FastAPI intelligence endpoints verified with TestClient.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
