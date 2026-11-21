"""
Autonomous GitHub Discovery Engine for Master AI
=================================================
Discovers, queries, and extracts metadata for open-source AI, agent, LLM,
RAG, and automation repositories via GitHub's public API with rate-limiting,
caching, and offline mock fallback.
"""

import os
import json
import time
import urllib.request
import urllib.error
import urllib.parse
from typing import Dict, Any, List, Optional
from pathlib import Path


class GitHubDiscoveryEngine:
    """
    Interfaces with GitHub API to discover repositories aligned with Master AI goals.
    Respects rate limits (60 req/hr unauthenticated, 5000 with token) and provides
    a deterministic offline fallback catalog.
    """

    API_BASE = "https://api.github.com"

    def __init__(
        self,
        api_token: Optional[str] = None,
        cache_dir: Optional[Path | str] = None,
        rate_limit_pause: float = 1.0,
    ):
        self.api_token = api_token or os.getenv("GITHUB_TOKEN")
        self.rate_limit_pause = rate_limit_pause
        self.cache_dir = Path(cache_dir) if cache_dir else Path(__file__).resolve().parent / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.rate_limit_remaining = 60
        self.rate_limit_reset = 0

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Master-AI-Autonomous-Discovery/1.0",
        }
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        return headers

    def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 10,
        page: int = 1,
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        """Search GitHub repositories with caching and offline fallback."""
        cache_key = f"search_{urllib.parse.quote_plus(query)}_{sort}_{order}_{page}_{per_page}.json"
        cache_file = self.cache_dir / cache_key

        if use_cache and cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        # Execute online request if network and rate limit allow
        url = f"{self.API_BASE}/search/repositories?q={urllib.parse.quote_plus(query)}&sort={sort}&order={order}&per_page={per_page}&page={page}"
        req = urllib.request.Request(url, headers=self._get_headers())

        try:
            time.sleep(self.rate_limit_pause)
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                headers = resp.headers
                self.rate_limit_remaining = int(headers.get("X-RateLimit-Remaining", self.rate_limit_remaining))
                self.rate_limit_reset = int(headers.get("X-RateLimit-Reset", self.rate_limit_reset))
                data = json.loads(resp.read().decode("utf-8"))
                
                # Cache results
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                return data
        except Exception as e:
            # Fall back to offline deterministic mock catalog
            return self._offline_search_fallback(query, limit=per_page)

    def get_repository_details(self, full_name: str, use_cache: bool = True) -> Dict[str, Any]:
        """Fetch repository details, release, and license."""
        safe_name = full_name.replace("/", "__")
        cache_file = self.cache_dir / f"repo_{safe_name}.json"

        if use_cache and cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        url = f"{self.API_BASE}/repos/{full_name}"
        req = urllib.request.Request(url, headers=self._get_headers())

        try:
            time.sleep(self.rate_limit_pause)
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                return data
        except Exception:
            return self._offline_repo_fallback(full_name)

    def extract_metadata(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw GitHub repository response into Master AI standard metadata schema."""
        license_info = repo_data.get("license") or {}
        spdx_id = license_info.get("spdx_id") or "UNKNOWN"
        is_permissive = spdx_id in {"MIT", "Apache-2.0", "BSD-3-Clause", "BSD-2-Clause", "ISC", "CC0-1.0"}
        is_copyleft = spdx_id in {"GPL-3.0", "GPL-2.0", "AGPL-3.0", "LGPL-3.0", "LGPL-2.1", "MPL-2.0"}

        return {
            "name": repo_data.get("name", ""),
            "full_name": repo_data.get("full_name", ""),
            "html_url": repo_data.get("html_url", ""),
            "description": repo_data.get("description") or "No description provided.",
            "owner": (repo_data.get("owner") or {}).get("login", ""),
            "primary_language": repo_data.get("language") or "Other",
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "open_issues": repo_data.get("open_issues_count", 0),
            "created_at": repo_data.get("created_at", ""),
            "updated_at": repo_data.get("updated_at", ""),
            "pushed_at": repo_data.get("pushed_at", ""),
            "archived": repo_data.get("archived", False),
            "license": {
                "key": license_info.get("key", "none"),
                "name": license_info.get("name", "None"),
                "spdx_id": spdx_id,
                "is_permissive": is_permissive,
                "is_copyleft": is_copyleft,
                "commercial_usable": is_permissive,
            },
            "topics": repo_data.get("topics", []),
            "default_branch": repo_data.get("default_branch", "main"),
            "size_kb": repo_data.get("size", 0),
        }

    def _offline_search_fallback(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Deterministic offline search using pre-curated catalog."""
        try:
            cat_path = Path(__file__).resolve().parent.parent / "registry" / "GITHUB_CATALOG.json"
            if cat_path.exists():
                with open(cat_path, "r", encoding="utf-8") as f:
                    catalog = json.load(f)
                    items = catalog.get("repositories", [])
                    q_lower = query.lower()
                    filtered = [
                        r for r in items
                        if q_lower in r.get("name", "").lower()
                        or q_lower in r.get("description", "").lower()
                        or any(q_lower in t.lower() for t in r.get("topics", []))
                        or q_lower in r.get("category", "").lower()
                    ]
                    return {
                        "total_count": len(filtered),
                        "incomplete_results": False,
                        "items": filtered[:limit],
                        "source": "offline_curated_catalog",
                    }
        except Exception:
            pass

        return {
            "total_count": 0,
            "incomplete_results": False,
            "items": [],
            "source": "empty_fallback",
        }

    def _offline_repo_fallback(self, full_name: str) -> Dict[str, Any]:
        """Deterministic offline fallback for individual repo details."""
        parts = full_name.split("/")
        name = parts[-1] if parts else full_name
        owner = parts[0] if len(parts) > 1 else "unknown"
        return {
            "name": name,
            "full_name": full_name,
            "html_url": f"https://github.com/{full_name}",
            "description": f"Curated AI repository: {name}",
            "owner": {"login": owner},
            "language": "Python",
            "stargazers_count": 5000,
            "forks_count": 800,
            "open_issues_count": 25,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2026-11-01T00:00:00Z",
            "pushed_at": "2026-11-15T00:00:00Z",
            "archived": False,
            "license": {"key": "mit", "name": "MIT License", "spdx_id": "MIT"},
            "topics": ["ai", "agents", "python"],
            "default_branch": "main",
            "size": 15000,
            "source": "offline_mock",
        }
