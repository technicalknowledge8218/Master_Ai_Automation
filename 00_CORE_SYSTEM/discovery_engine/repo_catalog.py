"""
GitHub Knowledge Library & Repository Catalog Manager for Master AI
===================================================================
Manages 100-200 curated AI/developer repositories, supports multi-attribute
filtering, duplicate detection, and indexes into Qdrant collection 'github_research'
for dense/sparse hybrid search.
"""

import json
import time
import importlib
from pathlib import Path
from typing import Dict, Any, List, Optional


def _get_catalog_file() -> Path:
    return Path(__file__).resolve().parent.parent / "registry" / "GITHUB_CATALOG.json"


class RepositoryCatalogManager:
    """Manages the curated GitHub repository library."""

    COLLECTION_NAME = "github_research"

    def __init__(self, catalog_path: Optional[Path | str] = None, qdrant_manager=None, embedding_engine=None):
        self.catalog_path = Path(catalog_path) if catalog_path else _get_catalog_file()
        self._data: Dict[str, Any] = self._load()

        # Dependencies for vector indexing
        self._qdrant = qdrant_manager
        self._embedder = embedding_engine

    def _load(self) -> Dict[str, Any]:
        if self.catalog_path.exists():
            try:
                with open(self.catalog_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {"catalog_version": "1.0.0", "repositories": []}
        return {"catalog_version": "1.0.0", "repositories": []}

    def save(self):
        """Persist catalog to JSON."""
        self.catalog_path.parent.mkdir(parents=True, exist_ok=True)
        temp_file = self.catalog_path.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)
        temp_file.replace(self.catalog_path)

    @property
    def total_repositories(self) -> int:
        return len(self._data.get("repositories", []))

    def list_repositories(
        self,
        category: Optional[str] = None,
        min_stars: int = 0,
        language: Optional[str] = None,
        permissive_only: bool = False,
        min_score: int = 0,
        domain_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Filter repositories based on criteria."""
        results = []
        for r in self._data.get("repositories", []):
            if category and r.get("category") != category:
                continue
            if domain_id and r.get("domain_id") != domain_id:
                continue
            if r.get("stars", 0) < min_stars:
                continue
            if language and r.get("primary_language", "").lower() != language.lower():
                continue
            if permissive_only and not r.get("license", {}).get("is_permissive", False):
                continue
            if r.get("evaluation_score", 0) < min_score:
                continue
            results.append(r)
        return results

    def get_repository(self, full_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve single repo by full name."""
        target = full_name.lower().strip()
        for r in self._data.get("repositories", []):
            if r.get("full_name", "").lower() == target:
                return r
        return None

    def is_duplicate(self, full_name: str) -> bool:
        """Check if repository is already catalogued."""
        return self.get_repository(full_name) is not None

    def add_repository(self, repo_entry: Dict[str, Any]) -> bool:
        """Add new repository with duplicate prevention."""
        full_name = repo_entry.get("full_name", "")
        if not full_name or self.is_duplicate(full_name):
            return False

        if "repositories" not in self._data:
            self._data["repositories"] = []

        self._data["repositories"].append(repo_entry)
        self.save()
        return True

    def get_categories(self) -> List[str]:
        """List all distinct categories in catalog."""
        cats = set(r.get("category", "general") for r in self._data.get("repositories", []))
        return sorted(list(cats))

    def sync_to_qdrant(self, dimension: int = 128) -> int:
        """Index all catalog entries into Qdrant vector database and BM25."""
        if self._qdrant is None:
            vdb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.vector_db")
            self._qdrant = vdb_mod.QdrantManager()

        if self._embedder is None:
            emb_mod = importlib.import_module("04_LLM_AND_AI.rag_systems.embeddings")
            self._embedder = emb_mod.get_embedding_engine("auto", dimension=dimension)

        self._qdrant.ensure_collection(self.COLLECTION_NAME, dimension=self._embedder.dimension)

        points = []
        for r in self._data.get("repositories", []):
            fn = r.get("full_name", "")
            title = f"GitHub Repo: {fn} ({r.get('category')})"
            text = (
                f"# {r.get('name')}\n"
                f"Full Name: {fn}\n"
                f"Category: {r.get('category')}\n"
                f"Description: {r.get('description')}\n"
                f"Stars: {r.get('stars')} | Language: {r.get('primary_language')}\n"
                f"License: {r.get('license', {}).get('spdx_id', 'UNKNOWN')}\n"
                f"Topics: {', '.join(r.get('topics', []))}\n"
                f"Score: {r.get('evaluation_score')} (Grade {r.get('evaluation_grade')})"
            )
            vec = self._embedder.embed_text(text)
            points.append({
                "id": f"gh-{fn.replace('/', '-')}",
                "vector": vec,
                "payload": {
                    "full_name": fn,
                    "title": title,
                    "category": r.get("category"),
                    "domain_id": r.get("domain_id"),
                    "stars": r.get("stars"),
                    "language": r.get("primary_language"),
                    "score": r.get("evaluation_score"),
                    "grade": r.get("evaluation_grade"),
                    "text": text,
                    "url": r.get("html_url"),
                }
            })

        upserted = self._qdrant.upsert_points(
            collection_name=self.COLLECTION_NAME,
            points=points,
            dimension=self._embedder.dimension,
        )
        return upserted
