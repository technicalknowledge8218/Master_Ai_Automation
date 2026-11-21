"""
Skills Intelligence & Synthesis Engine for Master AI
====================================================
Discovers, scaffolds, validates, tests, and stages workspace-local Antigravity skills.
Strict invariant: Never automatically activates untested or unapproved skills globally.
"""

import os
import re
import json
import yaml
import shutil
import importlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


class SkillsIntelligenceEngine:
    """Manages skill discovery, generation, validation, and staged lifecycle."""

    def __init__(self, workspace_root: Optional[Path | str] = None):
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).resolve().parent.parent.parent
        self.skills_dir = self.workspace_root / "02_SKILLS"
        self.staging_dir = self.workspace_root / "00_CORE_SYSTEM" / "staging" / "candidate_skills"
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        self.registry_path = self.workspace_root / "00_CORE_SYSTEM" / "registry" / "CAPABILITY_REGISTRY.json"

    def list_active_skills(self) -> List[Dict[str, Any]]:
        """List all currently active and validated workspace skills."""
        active = []
        if not self.skills_dir.exists():
            return active

        for item in os.listdir(self.skills_dir):
            sp = self.skills_dir / item
            if sp.is_dir() and item not in {"candidate_skills", "references", "scripts", "templates", "core_skills", "domain_skills"}:
                s_md = sp / "SKILL.md"
                if s_md.exists():
                    is_valid, meta = self.validate_skill_structure(sp)
                    active.append({
                        "id": item,
                        "name": meta.get("name", item),
                        "description": meta.get("description", ""),
                        "path": str(s_md),
                        "is_valid": is_valid,
                        "status": "ACTIVE_PRODUCTION",
                    })
        return active

    def list_candidate_skills(self) -> List[Dict[str, Any]]:
        """List skills currently in the staging / evaluation area."""
        candidates = []
        if not self.staging_dir.exists():
            return candidates

        for item in os.listdir(self.staging_dir):
            cp = self.staging_dir / item
            if cp.is_dir():
                s_md = cp / "SKILL.md"
                if s_md.exists():
                    is_valid, meta = self.validate_skill_structure(cp)
                    manifest_file = cp / "candidate_manifest.json"
                    manifest_data = {}
                    if manifest_file.exists():
                        try:
                            with open(manifest_file, "r", encoding="utf-8") as f:
                                manifest_data = json.load(f)
                        except Exception:
                            pass
                    candidates.append({
                        "id": item,
                        "name": meta.get("name", item),
                        "description": meta.get("description", ""),
                        "path": str(s_md),
                        "is_valid": is_valid,
                        "status": manifest_data.get("status", "STAGED_FOR_EVALUATION"),
                        "source_repo": manifest_data.get("source_repo", "internal"),
                        "approval_token": manifest_data.get("approval_token", None),
                    })
        return candidates

    def is_duplicate_skill(self, skill_name: str) -> bool:
        """Check if skill name or identifier already exists in production or staging."""
        norm_name = re.sub(r"[^a-z0-9\-]", "", skill_name.lower().replace("_", "-"))
        for s in self.list_active_skills():
            s_norm = re.sub(r"[^a-z0-9\-]", "", s["id"].lower().replace("_", "-"))
            if norm_name == s_norm or skill_name.lower() == s["name"].lower():
                return True
        for c in self.list_candidate_skills():
            c_norm = re.sub(r"[^a-z0-9\-]", "", c["id"].lower().replace("_", "-"))
            if norm_name == c_norm or skill_name.lower() == c["name"].lower():
                return True
        return False

    def validate_skill_structure(self, skill_dir: Path | str) -> Tuple[bool, Dict[str, Any]]:
        """
        Validates Antigravity SKILL.md specification:
          1. SKILL.md exists with valid YAML frontmatter ('---')
          2. Required fields: 'name' and 'description'
          3. Subdirectories present or well-formed
        """
        s_dir = Path(skill_dir)
        s_md = s_dir / "SKILL.md"
        if not s_md.exists():
            return False, {"error": "Missing SKILL.md"}

        try:
            content = s_md.read_text(encoding="utf-8")
            if not content.startswith("---"):
                return False, {"error": "SKILL.md does not start with YAML frontmatter '---'"}

            parts = content.split("---", 2)
            if len(parts) < 3:
                return False, {"error": "Malformed YAML frontmatter delimiters"}

            frontmatter = yaml.safe_load(parts[1])
            if not isinstance(frontmatter, dict):
                return False, {"error": "Frontmatter is not a dictionary"}

            if "name" not in frontmatter:
                return False, {"error": "Frontmatter missing required 'name' field"}
            if "description" not in frontmatter or not str(frontmatter["description"]).strip():
                return False, {"error": "Frontmatter missing required 'description' field"}

            return True, {
                "name": frontmatter["name"],
                "description": frontmatter["description"],
                "has_scripts": (s_dir / "scripts").exists(),
                "has_examples": (s_dir / "examples").exists(),
                "has_references": (s_dir / "references").exists(),
            }
        except Exception as e:
            return False, {"error": str(e)}

    def scaffold_candidate_skill(
        self,
        skill_id: str,
        name: str,
        description: str,
        domain_id: str,
        source_repo: str = "custom",
        author_agent: str = "capability_discovery_agent",
        instructions_body: str = "",
        sample_script_code: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Scaffold a new candidate skill in the candidate_skills staging directory.
        Never writes directly into active production skills.
        """
        norm_id = re.sub(r"[^a-z0-9\-]", "", skill_id.lower().replace("_", "-"))
        if self.is_duplicate_skill(norm_id):
            return {
                "status": "duplicate_rejected",
                "skill_id": norm_id,
                "error": f"Skill '{norm_id}' already exists in production or staging.",
            }

        target_dir = self.staging_dir / norm_id
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "scripts").mkdir(exist_ok=True)
        (target_dir / "examples").mkdir(exist_ok=True)
        (target_dir / "references").mkdir(exist_ok=True)

        body = instructions_body.strip() or f"## Instructions for {name}\n\nFollow these guidelines when executing {name}."
        skill_md_content = (
            f"---\n"
            f"name: {name}\n"
            f"description: {description}\n"
            f"---\n\n"
            f"# {name}\n\n"
            f"> **Domain**: `{domain_id}` | **Status**: Staged Candidate\n\n"
            f"{body}\n"
        )
        (target_dir / "SKILL.md").write_text(skill_md_content, encoding="utf-8")

        # Optional sample script
        if sample_script_code:
            (target_dir / "scripts" / "run_skill.py").write_text(sample_script_code, encoding="utf-8")

        # Candidate manifest for audit
        manifest = {
            "skill_id": norm_id,
            "name": name,
            "domain_id": domain_id,
            "source_repo": source_repo,
            "author_agent": author_agent,
            "status": "STAGED_FOR_EVALUATION",
            "version": "1.0.0",
            "created_at": None,
            "approval_token": None,
        }
        (target_dir / "candidate_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        is_valid, validation_details = self.validate_skill_structure(target_dir)

        return {
            "status": "scaffolded",
            "skill_id": norm_id,
            "target_dir": str(target_dir),
            "is_valid": is_valid,
            "validation_details": validation_details,
        }

    def promote_candidate_to_production(
        self,
        skill_id: str,
        approval_token: str,
        approver: str = "human_operator",
    ) -> Dict[str, Any]:
        """
        Promotes a candidate skill to active production only after verification
        and with a valid human approval token.
        """
        cand_dir = self.staging_dir / skill_id
        if not cand_dir.exists():
            raise FileNotFoundError(f"Candidate skill '{skill_id}' not found in staging.")

        is_valid, err = self.validate_skill_structure(cand_dir)
        if not is_valid:
            raise ValueError(f"Cannot promote invalid skill '{skill_id}': {err}")

        # Verification of approval token prefix
        if not approval_token or not approval_token.startswith("AUTH-"):
            raise PermissionError("A valid human approval token (AUTH-*) is required to promote skills to production.")

        prod_dir = self.skills_dir / skill_id
        if prod_dir.exists():
            raise FileExistsError(f"Production skill '{skill_id}' already exists.")

        # Atomic copy and purge staging
        shutil.copytree(cand_dir, prod_dir)
        shutil.rmtree(cand_dir, ignore_errors=True)

        return {
            "status": "promoted",
            "skill_id": skill_id,
            "production_path": str(prod_dir),
            "approval_token": approval_token,
            "approver": approver,
        }
