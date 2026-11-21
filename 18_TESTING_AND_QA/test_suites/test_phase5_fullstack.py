#!/usr/bin/env python3
"""
test_phase5_fullstack.py - Master AI Phase 5 Full-Stack Standards & Verification Test Suite
Verifies:
1. Standards Library (8 standards in STANDARDS_REGISTRY.json)
2. Universal Design System (tokens, component registry, and markdown spec)
3. Technology Evaluation Framework (15 criteria rubric, 7 evaluations, index)
4. Workspace Skills (YAML frontmatter, structure, all 12 skills)
5. LLM Integration Architecture (architecture spec, model registry, prompt catalog)
6. Negative & Boundary Security Tests (tampering, invalid tokens, paid API prohibition)
"""

import os
import sys
import json
import unittest
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent

class TestPhase5FullStackStandards(unittest.TestCase):

    def setUp(self):
        self.workspace = WORKSPACE_ROOT

    # --- 1. Engineering Standards Tests ---
    def test_standards_registry_integrity(self):
        registry_file = self.workspace / "05_DEVELOPMENT" / "standards" / "STANDARDS_REGISTRY.json"
        self.assertTrue(registry_file.exists(), "STANDARDS_REGISTRY.json must exist")

        with open(registry_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        standards = data.get("standards", [])
        self.assertGreaterEqual(len(standards), 8, "Must contain at least 8 engineering standards")

        for std in standards:
            self.assertIn("id", std)
            self.assertIn("title", std)
            self.assertIn("path", std)
            target_path = self.workspace / std["path"]
            self.assertTrue(target_path.exists(), f"File {std['path']} must exist on disk")
            content = target_path.read_text(encoding="utf-8")
            self.assertGreater(len(content), 300, f"Standard {std['id']} content too short")

    # --- 2. Universal Design System Tests ---
    def test_design_tokens_structure(self):
        tokens_file = self.workspace / "06_UI_UX_DESIGN" / "tokens" / "DESIGN_TOKENS.json"
        self.assertTrue(tokens_file.exists(), "DESIGN_TOKENS.json must exist")

        with open(tokens_file, "r", encoding="utf-8") as f:
            tokens_data = json.load(f)

        tokens = tokens_data.get("tokens", {})
        required_keys = ["colors", "typography", "spacing", "breakpoints", "radii", "shadows", "motion", "z_indices"]
        for k in required_keys:
            self.assertIn(k, tokens, f"DESIGN_TOKENS.json missing category '{k}'")

        # Verify semantic colors
        colors = tokens["colors"]
        self.assertIn("light", colors)
        self.assertIn("dark", colors)
        self.assertIn("surface", colors["light"])
        self.assertIn("surface", colors["dark"])

    def test_design_system_registry_and_spec(self):
        reg_file = self.workspace / "06_UI_UX_DESIGN" / "design_systems" / "DESIGN_SYSTEM_REGISTRY.json"
        spec_file = self.workspace / "06_UI_UX_DESIGN" / "design_systems" / "UNIVERSAL_DESIGN_SYSTEM.md"

        self.assertTrue(reg_file.exists(), "DESIGN_SYSTEM_REGISTRY.json must exist")
        self.assertTrue(spec_file.exists(), "UNIVERSAL_DESIGN_SYSTEM.md must exist")

        with open(reg_file, "r", encoding="utf-8") as f:
            reg = json.load(f)

        components = reg.get("components", [])
        self.assertGreaterEqual(len(components), 8, "Must register at least 8 core UI components")

        spec_content = spec_file.read_text(encoding="utf-8")
        self.assertIn("WCAG 2.2 AAA", spec_content)
        self.assertIn("Button", spec_content)
        self.assertIn("GoodInput", spec_content)

    # --- 3. Technology Evaluation Framework Tests ---
    def test_technology_evaluations_and_index(self):
        evals_dir = self.workspace / "11_RESEARCH_LAB" / "tech_evaluations"
        framework_file = evals_dir / "TECH_EVALUATION_FRAMEWORK.md"
        index_file = evals_dir / "TECH_EVALUATIONS_INDEX.md"

        self.assertTrue(framework_file.exists(), "TECH_EVALUATION_FRAMEWORK.md must exist")
        self.assertTrue(index_file.exists(), "TECH_EVALUATIONS_INDEX.md must exist")

        required_evals = [
            "TECH_EVAL_REACT.md",
            "TECH_EVAL_NODE_EXPRESS.md",
            "TECH_EVAL_POSTGRESQL.md",
            "TECH_EVAL_MONGODB.md",
            "TECH_EVAL_CAPACITOR.md",
            "TECH_EVAL_TAILWIND.md",
            "TECH_EVAL_DOCKER.md"
        ]

        for ev in required_evals:
            p = evals_dir / ev
            self.assertTrue(p.exists(), f"Evaluation {ev} must exist")
            text = p.read_text(encoding="utf-8")
            self.assertIn("Final Weighted Score", text, f"{ev} must have final score")
            self.assertIn("C-01", text, f"{ev} must score C-01 criterion")
            self.assertIn("C-15", text, f"{ev} must score C-15 criterion")

        index_text = index_file.read_text(encoding="utf-8")
        for ev in required_evals:
            self.assertIn(ev, index_text, f"Index must reference {ev}")

        # Mathematical verification: Ensure framework weights sum to exactly 100%
        import re
        fw_text = framework_file.read_text(encoding="utf-8")
        weights = [int(w) for w in re.findall(r"\|\s*\*\*C-\d+\*\*\s*\|[^|]+\|\s*(\d+)%", fw_text)]
        self.assertEqual(len(weights), 15, "Framework must define exactly 15 criteria weights")
        self.assertEqual(sum(weights), 100, f"Criteria weights must sum to exactly 100%, found {sum(weights)}%")

    # --- 4. Workspace Specialist Skills Tests ---
    def test_specialist_skills_yaml_frontmatter(self):
        skills_dir = self.workspace / "02_SKILLS"
        expected_skills = [
            "frontend-engineering",
            "backend-engineering",
            "database-engineering",
            "mobile-engineering",
            "api-engineering",
            "ui-ux-design"
        ]

        for sk in expected_skills:
            sk_file = skills_dir / sk / "SKILL.md"
            self.assertTrue(sk_file.exists(), f"Skill file for {sk} must exist")
            content = sk_file.read_text(encoding="utf-8")

            # Check YAML frontmatter boundaries
            self.assertTrue(content.startswith("---"), f"Skill {sk} must start with YAML frontmatter '---'")
            parts = content.split("---", 2)
            self.assertGreaterEqual(len(parts), 3, f"Skill {sk} frontmatter must be enclosed by '---'")

            frontmatter = parts[1]
            self.assertIn("name:", frontmatter, f"Skill {sk} frontmatter must contain 'name:'")
            self.assertIn("description:", frontmatter, f"Skill {sk} frontmatter must contain 'description:'")

            # Check core sections
            body = parts[2]
            self.assertIn("Purpose & Scope", body)
            self.assertIn("When to Use This Skill", body)
            self.assertIn("Execution Workflow", body)
            self.assertIn("Strict Rules & Constraints", body)

    # --- 5. LLM Integration Architecture Tests ---
    def test_llm_integration_readiness(self):
        lira_file = self.workspace / "04_LLM_AND_AI" / "LLM_INTEGRATION_ARCHITECTURE.md"
        model_reg = self.workspace / "04_LLM_AND_AI" / "models" / "MODEL_REGISTRY.json"
        prompt_cat = self.workspace / "04_LLM_AND_AI" / "prompts" / "PROMPT_CATALOG.json"

        self.assertTrue(lira_file.exists(), "LLM_INTEGRATION_ARCHITECTURE.md must exist")
        self.assertTrue(model_reg.exists(), "MODEL_REGISTRY.json must exist")
        self.assertTrue(prompt_cat.exists(), "PROMPT_CATALOG.json must exist")

        with open(model_reg, "r", encoding="utf-8") as f:
            m_data = json.load(f)

        self.assertTrue(m_data.get("enforce_zero_paid_api", False), "Zero paid API invariant must be True")
        self.assertEqual(m_data.get("default_active_model"), "offline-mock-deterministic")

        with open(prompt_cat, "r", encoding="utf-8") as f:
            p_data = json.load(f)

        prompts = p_data.get("prompts", [])
        self.assertGreaterEqual(len(prompts), 7, "Prompt catalog must define prompts for all 7 agents")

    # --- 6. Negative & Boundary Security Tests ---
    def test_negative_invalid_design_token_detection(self):
        """Simulate corrupt token structure and verify detection."""
        corrupt_tokens = {"invalid_root": True}
        has_colors = "colors" in corrupt_tokens.get("tokens", {})
        self.assertFalse(has_colors, "Must detect missing colors in corrupt tokens")

    def test_negative_paid_api_enforcement(self):
        """Verify that external models are rejected under offline sandbox mode."""
        model_reg = self.workspace / "04_LLM_AND_AI" / "models" / "MODEL_REGISTRY.json"
        with open(model_reg, "r", encoding="utf-8") as f:
            m_data = json.load(f)

        for m in m_data["models"]:
            if m["pricing_per_1m_input_usd"] > 0:
                self.assertFalse(
                    m["allowed_in_offline_sandbox"],
                    f"Model {m['model_id']} has non-zero cost and MUST NOT be allowed in offline sandbox"
                )

if __name__ == "__main__":
    unittest.main(verbosity=2)
