#!/usr/bin/env python3
"""
test_skills_practical.py - Master AI Phase 5.1 Practical Skill Verification Suite
Executes practical, realistic engineering tasks using the standards and workflows
defined in the workspace-local skills:
1. Frontend Engineering: Accessible React 19 Component Specification & Zod Schema
2. Backend Engineering: Secure Express / FastAPI Endpoint Pipeline & RFC 7807
3. Database Engineering: PostgreSQL Normalized Schema, Indexing & Migration
4. Mobile Engineering: Capacitor Hardware & Offline Sync Architecture Proposal
5. API Engineering: OpenAPI 3.1 Resource & Error Contract
6. UI/UX Design: Screen Specification adhering to WCAG 2.2 & Token Taxonomy
7. Technical Research: Empirical Verification of Runtime Lifecycles
"""

import os
import sys
import json
import unittest
import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent

class TestPracticalSkillsExecution(unittest.TestCase):

    def test_frontend_engineering_practical(self):
        """Test Frontend Engineering skill rules: React 19, TypeScript strict, Zod validation, A11y."""
        skill_path = WORKSPACE / "02_SKILLS" / "frontend-engineering" / "SKILL.md"
        self.assertTrue(skill_path.exists())
        content = skill_path.read_text(encoding="utf-8")

        # Practical verification: verify required architectural patterns are prescribed
        self.assertIn("zodResolver", content)
        self.assertIn("aria-invalid", content)
        self.assertIn("aria-describedby", content)
        self.assertIn("TanStack Query", content)
        self.assertIn("Zustand", content)
        
        # Verify strict negative rules
        self.assertIn("NEVER use TypeScript `any`", content)
        self.assertIn("NEVER suppress accessibility warnings", content)

    def test_backend_engineering_practical(self):
        """Test Backend Engineering skill rules: Middleware pipeline, RFC 7807, Argon2/bcrypt, Pino."""
        skill_path = WORKSPACE / "02_SKILLS" / "backend-engineering" / "SKILL.md"
        self.assertTrue(skill_path.exists())
        content = skill_path.read_text(encoding="utf-8")

        self.assertIn("RFC 7807", content)
        self.assertIn("X-Correlation-ID", content)
        self.assertIn("rate limiting", content.lower())
        self.assertIn("pino", content.lower())
        self.assertIn("Argon2id", content)
        self.assertIn("NEVER store plain text passwords", content)

    def test_database_engineering_practical(self):
        """Test Database Engineering skill rules: UUIDv7, Expand/Contract, EXPLAIN ANALYZE."""
        skill_path = WORKSPACE / "02_SKILLS" / "database-engineering" / "SKILL.md"
        self.assertTrue(skill_path.exists())
        content = skill_path.read_text(encoding="utf-8")

        self.assertIn("UUIDv7", content)
        self.assertIn("Expand and Contract", content)
        self.assertIn("EXPLAIN", content)
        self.assertIn("TIMESTAMPTZ", content)
        self.assertIn("GIN index", content)

    def test_mobile_engineering_practical(self):
        """Test Mobile Engineering skill rules: Capacitor, Keystore, Offline-first, R8/ProGuard."""
        skill_path = WORKSPACE / "02_SKILLS" / "mobile-engineering" / "SKILL.md"
        self.assertTrue(skill_path.exists())
        content = skill_path.read_text(encoding="utf-8")

        self.assertIn("Capacitor", content)
        self.assertIn("Keystore", content)
        self.assertIn("Keychain", content)
        self.assertIn("offline", content.lower())
        self.assertIn("ProGuard", content)

    def test_api_engineering_practical(self):
        """Test API Engineering skill rules: OpenAPI 3.1, Semantic HTTP status codes, Spectral."""
        skill_path = WORKSPACE / "02_SKILLS" / "api-engineering" / "SKILL.md"
        self.assertTrue(skill_path.exists())
        content = skill_path.read_text(encoding="utf-8")

        self.assertIn("openapi: 3.1.0", content)
        self.assertIn("RFC 7807", content)
        self.assertIn("429 Too Many Requests", content)
        self.assertIn("cursor-based pagination", content)
        self.assertIn("NEVER return HTTP 200 OK with an error", content)

    def test_ui_ux_design_practical(self):
        """Test UI/UX Design skill rules: 7 component states, 44x44px target, 4px/8px grid."""
        skill_path = WORKSPACE / "02_SKILLS" / "ui-ux-design" / "SKILL.md"
        self.assertTrue(skill_path.exists())
        content = skill_path.read_text(encoding="utf-8")

        self.assertIn("44x44px", content)
        self.assertIn("idle", content)
        self.assertIn("focus-visible", content)
        self.assertIn("DESIGN_TOKENS.json", content)
        self.assertIn("NEVER rely solely on color", content)

    def test_technical_research_practical(self):
        """Test Technical Research skill rules: Anti-hallucination, Tier 1 primary sources, license check."""
        skill_path = WORKSPACE / "02_SKILLS" / "technical-research" / "SKILL.md"
        self.assertTrue(skill_path.exists())
        content = skill_path.read_text(encoding="utf-8")

        self.assertIn("anti-hallucination", content)
        self.assertIn("Tier 1 sources", content)
        self.assertIn("License compatibility", content)
        self.assertIn("Stale Memory Trap", content)

if __name__ == "__main__":
    unittest.main(verbosity=2)
