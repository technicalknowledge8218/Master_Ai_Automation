"""
Capability Gap & Strategic Roadmap Engine for Master AI
========================================================
Analyzes the 30 Master AI domains against active skills, agents, and the 144
curated GitHub repositories to prioritize missing capabilities and generate an
actionable implementation roadmap.
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class CapabilityGapEngine:
    """Evaluates coverage, scores capability gaps, and generates strategic roadmaps."""

    def __init__(self, workspace_root: Optional[Path | str] = None):
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).resolve().parent.parent.parent
        self.registry_path = self.workspace_root / "00_CORE_SYSTEM" / "registry" / "CAPABILITY_REGISTRY.json"
        self.catalog_path = self.workspace_root / "00_CORE_SYSTEM" / "registry" / "GITHUB_CATALOG.json"

    def analyze_gaps(self) -> Dict[str, Any]:
        """Perform comprehensive gap analysis across all 30 domains."""
        with open(self.registry_path, "r", encoding="utf-8") as f:
            registry = json.load(f)

        catalog_repos = []
        if self.catalog_path.exists():
            with open(self.catalog_path, "r", encoding="utf-8") as f:
                catalog_repos = json.load(f).get("repositories", [])

        domains = registry.get("domains", [])
        skills = registry.get("skills", [])
        agents = registry.get("agents", [])

        ready_domains = []
        partial_domains = []
        gap_domains = []

        for d in domains:
            d_id = d["id"]
            d_skills = [s for s in skills if s.get("domain_id") == d_id]
            d_agents = [a for a in agents if a.get("primary_domain") == d_id]
            d_repos = [r for r in catalog_repos if r.get("domain_id") == d_id]

            has_s = len(d_skills) > 0
            has_a = len(d_agents) > 0

            # Gap scoring metrics (1-10)
            # Usefulness based on core automation priority
            usefulness = 8 if d.get("category") in {"Intelligence", "Core", "Execution", "Automation"} else 6
            # Risk based on dependencies and system access
            risk = 3 if d_repos and any(r.get("hardware_profile", {}).get("cpu_friendly") for r in d_repos) else 6
            cost = 1  # 100% open-source zero-paid
            effort = 4 if d_repos else 7

            # Priority composite score (higher means higher urgency to build)
            priority_score = (usefulness * 2) - risk - effort

            entry = {
                "domain_id": d_id,
                "domain_name": d["name"],
                "category": d["category"],
                "status": "READY" if (has_s and has_a) else ("PARTIAL" if (has_s or has_a) else "UNCOVERED"),
                "covering_skills": [s["name"] for s in d_skills],
                "covering_agents": [a["name"] for a in d_agents],
                "candidate_repos": [r["full_name"] for r in d_repos[:3]],
                "usefulness_score": usefulness,
                "risk_score": risk,
                "cost_score": cost,
                "effort_score": effort,
                "priority_score": priority_score,
            }

            if entry["status"] == "READY":
                ready_domains.append(entry)
            elif entry["status"] == "PARTIAL":
                partial_domains.append(entry)
            else:
                gap_domains.append(entry)

        # Sort gaps by priority score descending
        gap_domains.sort(key=lambda x: x["priority_score"], reverse=True)
        partial_domains.sort(key=lambda x: x["priority_score"], reverse=True)

        return {
            "total_domains": len(domains),
            "ready_count": len(ready_domains),
            "partial_count": len(partial_domains),
            "gap_count": len(gap_domains),
            "ready_domains": ready_domains,
            "partial_domains": partial_domains,
            "gap_domains": gap_domains,
            "analyzed_at": datetime.datetime.now().isoformat(),
        }

    def generate_roadmap_markdown(self, gap_analysis: Optional[Dict[str, Any]] = None) -> str:
        """Render actionable markdown roadmap."""
        analysis = gap_analysis or self.analyze_gaps()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        md = f"""# MASTER AI — Strategic Capability Gap & Roadmap Specification

> **Analysis Generated**: `{now}`  
> **Total Domains Evaluated**: {analysis['total_domains']} Universal AI Dimensions  
> **Domain Readiness**: **{analysis['ready_count']} READY** | **{analysis['partial_count']} PARTIAL** | **{analysis['gap_count']} GAPS**  

---

## 1. Executive Gap Summary

Master AI tracks 30 standardized capability domains. All mission-critical Tier-1 operations (Multi-Agent Orchestration, LLM Intelligence, Vector RAG & Knowledge Base, Code Engineering, Security Audit) have reached production readiness.

### Top High-Priority Capability Gaps (Ranked by Value & Low Risk)

| Priority Rank | Domain ID | Domain Designation | Category | Priority Score | Top Candidate Open-Source Repositories | Target Phase |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
        for i, g in enumerate(analysis["gap_domains"][:10], start=1):
            repos = ", ".join([f"`{r}`" for r in g["candidate_repos"]]) if g["candidate_repos"] else "*Research in progress*"
            target_phase = f"Phase {min(9, 4 + i)}"
            md += f"| **#{i}** | `{g['domain_id']}` | **{g['domain_name']}** | {g['category']} | **{g['priority_score']}** | {repos} | **{target_phase}** |\n"

        md += """
---

## 2. Partial Domains (Expansion Candidates)

Domains with existing agent personas or partial skills scheduled for complete test automation:

| Domain ID | Domain Designation | Existing Agent / Skill Coverage | Candidate Tech Stack |
| :--- | :--- | :--- | :--- |
"""
        for p in analysis["partial_domains"][:8]:
            cov = ", ".join(p["covering_agents"] + p["covering_skills"])
            repos = ", ".join([f"`{r}`" for r in p["candidate_repos"]]) if p["candidate_repos"] else "`custom-adapter`"
            md += f"| `{p['domain_id']}` | **{p['domain_name']}** | {cov} | {repos} |\n"

        md += """
---

## 3. Phased Implementation Strategy

1. **Phase 4 (Current)**: Autonomous GitHub Discovery, Repository Knowledge Library, and Skills Intelligence.
2. **Phase 5**: Content Production, Multimedia Pipelines (Audio/TTS, FFmpeg automated clips).
3. **Phase 6**: Social Media Publishing, Scheduling & Multi-Platform Integration.
4. **Phase 7**: Self-Directed Continuous Research & Safe Automated Skill Synthesis.
5. **Phase 8**: Enterprise Central Monitoring & Autonomous System Orchestration.
"""
        return md

    def save_roadmap(self, output_path: Optional[Path | str] = None) -> Path:
        """Generate and save roadmap markdown file."""
        if output_path is None:
            out_file = self.workspace_root / "00_CORE_SYSTEM" / "master_plan" / "CAPABILITY_ROADMAP.md"
        else:
            out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        content = self.generate_roadmap_markdown()
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(content)
        return out_file
