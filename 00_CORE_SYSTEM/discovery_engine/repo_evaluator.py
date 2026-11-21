"""
Repository Evaluation & Risk Scoring Engine for Master AI
=========================================================
Scores candidate open-source repositories across 8 dimensions (0-100 total)
and identifies security, licensing, architectural, and compatibility risk flags.
"""

import re
import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class EvaluationScorecard:
    """Standard evaluation scorecard for a discovered repository."""
    full_name: str
    total_score: int
    grade: str  # 'A', 'B', 'C', 'D', 'F'
    scores: Dict[str, int]
    risk_flags: List[str]
    compatibility_status: str  # 'COMPATIBLE', 'PARTIAL_WORKAROUND', 'INCOMPATIBLE'
    commercial_suitability: str  # 'COMMERCIAL_APPROVED', 'RESTRICTED', 'PROHIBITED'
    hardware_profile: Dict[str, Any]
    recommendation: str
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RepositoryEvaluator:
    """Evaluates repositories for safety, viability, and system fit."""

    PERMISSIVE_LICENSES = {"MIT", "Apache-2.0", "BSD-3-Clause", "BSD-2-Clause", "ISC", "CC0-1.0", "Unlicense"}
    COPYLEFT_LICENSES = {"GPL-3.0", "GPL-2.0", "LGPL-3.0", "LGPL-2.1", "MPL-2.0"}
    RESTRICTIVE_LICENSES = {"AGPL-3.0", "SSPL-1.0", "CC-BY-NC-4.0", "BSL-1.1", "NONE", "UNKNOWN"}

    SUSPICIOUS_PATTERNS = [
        re.compile(r"base64\.b64decode\(", re.IGNORECASE),
        re.compile(r"exec\(eval\(", re.IGNORECASE),
        re.compile(r"curl\s+.*\s*\|\s*(ba)?sh", re.IGNORECASE),
        re.compile(r"subprocess\.call\(.*curl", re.IGNORECASE),
        re.compile(r"urllib\.request\.urlretrieve\(.*\.exe", re.IGNORECASE),
        re.compile(r"os\.system\(.*rm\s+-rf\s+/", re.IGNORECASE),
    ]

    LINUX_ONLY_MODULES = {"fcntl", "termios", "pty", "pwd", "grp", "resource", "syslog"}

    def evaluate_repository(
        self,
        repo_metadata: Dict[str, Any],
        readme_text: str = "",
        dependency_text: str = "",
        sample_code: str = "",
    ) -> EvaluationScorecard:
        """Execute full 8-dimensional evaluation of a repository."""
        scores = {}
        flags = []

        # 1. Functionality (0-15)
        # Assessed by description clarity, topics, and problem alignment
        desc = repo_metadata.get("description", "")
        topics = repo_metadata.get("topics", [])
        f_score = 10
        if len(desc) > 50:
            f_score += 2
        if len(topics) >= 3:
            f_score += 3
        scores["functionality"] = min(15, f_score)

        # 2. Maintenance & Recency (0-15)
        m_score = 15
        archived = repo_metadata.get("archived", False)
        if archived:
            m_score = 0
            flags.append("ARCHIVED_PROJECT")
        else:
            pushed_at = repo_metadata.get("pushed_at") or repo_metadata.get("updated_at")
            if pushed_at:
                try:
                    # Parse ISO timestamp
                    p_date = datetime.datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
                    days_idle = (datetime.datetime.now(datetime.timezone.utc) - p_date).days
                    if days_idle > 540:  # > 18 months
                        m_score = max(0, m_score - 12)
                        flags.append("ABANDONED_PROJECT")
                    elif days_idle > 270:  # > 9 months
                        m_score = max(5, m_score - 6)
                        flags.append("STALE_MAINTENANCE")
                    elif days_idle < 60:
                        m_score = 15
                except Exception:
                    m_score = 10
        scores["maintenance"] = m_score

        # 3. Security & Safety (0-15)
        s_score = 15
        combined_text = f"{readme_text}\n{dependency_text}\n{sample_code}"
        for pat in self.SUSPICIOUS_PATTERNS:
            if pat.search(combined_text):
                s_score = max(0, s_score - 8)
                flags.append("SUSPICIOUS_INSTALLATION_OR_PAYLOAD")

        open_issues = repo_metadata.get("open_issues", 0)
        stars = repo_metadata.get("stars", 1)
        # Extremely high ratio of issues to stars might indicate instability
        if stars > 100 and (open_issues / stars) > 0.4:
            s_score = max(5, s_score - 3)
            flags.append("HIGH_ISSUE_RATIO")
        scores["security"] = s_score

        # 4. License Compatibility (0-15)
        lic = repo_metadata.get("license") or {}
        spdx = lic.get("spdx_id", "UNKNOWN").upper()
        l_score = 5
        commercial = "PROHIBITED"

        if spdx in self.PERMISSIVE_LICENSES:
            l_score = 15
            commercial = "COMMERCIAL_APPROVED"
        elif spdx in self.COPYLEFT_LICENSES:
            l_score = 10
            commercial = "RESTRICTED_COPYLEFT"
            flags.append("COPYLEFT_LICENSE")
        else:
            l_score = 2
            flags.append("RESTRICTIVE_OR_UNKNOWN_LICENSE")
        scores["license"] = l_score

        # 5. Documentation Quality (0-10)
        d_score = 6
        if len(readme_text) > 3000:
            d_score = 10
        elif len(readme_text) > 1000:
            d_score = 8
        elif len(readme_text) < 200:
            d_score = 3
            flags.append("POOR_DOCUMENTATION")
        scores["documentation"] = d_score

        # 6. Community Adoption (0-10)
        stars_cnt = repo_metadata.get("stars", 0)
        forks_cnt = repo_metadata.get("forks", 0)
        if stars_cnt >= 5000 or forks_cnt >= 500:
            c_score = 10
        elif stars_cnt >= 1000 or forks_cnt >= 100:
            c_score = 8
        elif stars_cnt >= 200:
            c_score = 6
        elif stars_cnt >= 50:
            c_score = 4
        else:
            c_score = 2
        scores["community"] = c_score

        # 7. Resource Requirements (CPU, RAM, GPU) (0-10)
        # CPU-first friendly vs Heavy multi-GPU requirement
        r_score = 10
        gpu_heavy = any(kw in combined_text.lower() for kw in ["cuda 12", "vram 24gb", "multi-gpu", "a100", "h100"])
        cloud_paid = any(kw in combined_text.lower() for kw in ["openai_api_key required", "pinecone", "paid api required"])
        if gpu_heavy:
            r_score = max(2, r_score - 5)
            flags.append("HEAVY_GPU_REQUIREMENT")
        if cloud_paid:
            r_score = max(2, r_score - 4)
            flags.append("PAID_CLOUD_DEPENDENCY")
        scores["resources"] = r_score

        # 8. Integration Complexity & Windows 11 / Python 3.14 (0-10)
        i_score = 10
        linux_only = any(mod in combined_text.lower() for mod in self.LINUX_ONLY_MODULES)
        if linux_only:
            i_score = max(1, i_score - 7)
            flags.append("LINUX_SYSTEM_CALLS_DETECTED")
        if "c++" in repo_metadata.get("primary_language", "").lower():
            i_score = max(4, i_score - 3)
            flags.append("REQUIRES_NATIVE_C_COMPILER")
        scores["integration"] = i_score

        # Calculate Total Score & Grade
        total = sum(scores.values())
        if total >= 85:
            grade = "A"
            recommendation = "RECOMMENDED: High quality, permissive license, ready for sandbox evaluation."
        elif total >= 70:
            grade = "B"
            recommendation = "VIABLE: Strong utility, review dependencies and licensing details."
        elif total >= 55:
            grade = "C"
            recommendation = "CAUTION: Moderate complexity or constraints; evaluate capability gap before adopting."
        elif total >= 40:
            grade = "D"
            recommendation = "HIGH_RISK: Substantial resource, compatibility, or licensing challenges."
        else:
            grade = "F"
            recommendation = "REJECTED: Severe safety, maintenance, or licensing risks detected."

        compat = "COMPATIBLE"
        if "LINUX_SYSTEM_CALLS_DETECTED" in flags or "ARCHIVED_PROJECT" in flags:
            compat = "INCOMPATIBLE"
        elif "HEAVY_GPU_REQUIREMENT" in flags or "REQUIRES_NATIVE_C_COMPILER" in flags:
            compat = "PARTIAL_WORKAROUND"

        hardware_profile = {
            "cpu_friendly": not gpu_heavy,
            "estimated_ram_mb": 1024 if not gpu_heavy else 8192,
            "requires_gpu": gpu_heavy,
            "requires_paid_api": cloud_paid,
            "windows_supported": not linux_only,
            "python_version_support": ">=3.10",
        }

        return EvaluationScorecard(
            full_name=repo_metadata.get("full_name", "unknown"),
            total_score=total,
            grade=grade,
            scores=scores,
            risk_flags=flags,
            compatibility_status=compat,
            commercial_suitability=commercial,
            hardware_profile=hardware_profile,
            recommendation=recommendation,
        )
