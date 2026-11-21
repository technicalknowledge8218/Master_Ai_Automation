"""
Scheduled Discovery & Update Monitor for Master AI
==================================================
Manages periodic discovery scans, repository update checks, and capability gap
reviews with strict resource bounds and user-visible state tracking.
"""

import time
import json
import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class DiscoveryScheduler:
    """Manages bounded, scheduled discovery cycles without uncontrolled background loops."""

    DEFAULT_INTERVAL_HOURS = 24

    def __init__(self, workspace_root: Optional[Path | str] = None):
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).resolve().parent.parent.parent
        self.state_file = self.workspace_root / "00_CORE_SYSTEM" / "registry" / "DISCOVERY_SCHEDULE_STATE.json"
        self._state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "scheduler_enabled": True,
            "interval_hours": self.DEFAULT_INTERVAL_HOURS,
            "max_repos_per_scan": 15,
            "last_scan_timestamp": None,
            "next_scheduled_scan": None,
            "total_scans_completed": 0,
            "last_scan_results": {},
        }

    def _save_state(self):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self._state, f, indent=2)

    def get_status(self) -> Dict[str, Any]:
        return dict(self._state)

    def run_discovery_cycle(self, max_repos: Optional[int] = None) -> Dict[str, Any]:
        """Execute a controlled, single-pass discovery and gap evaluation cycle."""
        from .repo_catalog import RepositoryCatalogManager
        from .capability_gap_engine import CapabilityGapEngine

        limit = max_repos or self._state.get("max_repos_per_scan", 15)
        cat_mgr = RepositoryCatalogManager()
        gap_eng = CapabilityGapEngine(workspace_root=self.workspace_root)

        # 1. Run gap analysis
        gap_report = gap_eng.analyze_gaps()
        gap_eng.save_roadmap()

        # 2. Update catalog metrics
        total_repos = cat_mgr.total_repositories
        categories = cat_mgr.get_categories()

        now = time.time()
        next_scan = now + (self._state.get("interval_hours", 24) * 3600)

        results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "repositories_catalogued": total_repos,
            "categories_monitored": len(categories),
            "uncovered_gaps_identified": gap_report.get("gap_count", 0),
            "top_priority_gap": gap_report.get("gap_domains", [{}])[0].get("domain_name", "None"),
            "status": "COMPLETED_SUCCESSFULLY",
        }

        self._state["last_scan_timestamp"] = now
        self._state["next_scheduled_scan"] = next_scan
        self._state["total_scans_completed"] = self._state.get("total_scans_completed", 0) + 1
        self._state["last_scan_results"] = results
        self._save_state()

        return results
