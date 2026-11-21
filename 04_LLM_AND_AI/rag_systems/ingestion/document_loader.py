"""
Multiformat Document Loader for Master AI RAG
=============================================
Loads documents from diverse formats (Markdown, TXT, JSON, CSV, Python, YAML)
and packages them into normalized Document objects with metadata.
"""

import os
import json
import csv
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class LoadedDocument:
    """Represents raw loaded document ready for filtering and chunking."""
    doc_id: str
    title: str
    content: str
    source_path: str
    doc_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class DocumentLoader:
    """Extracts text content and metadata from multiple file formats."""

    SUPPORTED_EXTENSIONS = {
        ".md", ".markdown",
        ".txt", ".rst",
        ".py",
        ".json",
        ".csv",
        ".yaml", ".yml",
        ".html",
    }

    @classmethod
    def can_load(cls, path: str | Path) -> bool:
        p = Path(path)
        return p.suffix.lower() in cls.SUPPORTED_EXTENSIONS

    @classmethod
    def load_file(cls, file_path: str | Path, base_dir: Optional[str | Path] = None) -> LoadedDocument:
        p = Path(file_path).resolve()
        if not p.is_file():
            raise FileNotFoundError(f"File not found: {p}")

        ext = p.suffix.lower()

        # Compute relative doc_id
        if base_dir:
            try:
                rel_path = p.relative_to(Path(base_dir).resolve())
                doc_id = str(rel_path).replace("\\", "/")
            except ValueError:
                doc_id = p.name
        else:
            doc_id = p.name

        stat = p.stat()
        base_meta = {
            "source_path": str(p),
            "file_name": p.name,
            "extension": ext,
            "size_bytes": stat.st_size,
            "mtime": stat.st_mtime,
        }

        if ext in {".md", ".markdown"}:
            return cls._load_markdown(p, doc_id, base_meta)
        elif ext in {".py"}:
            return cls._load_python(p, doc_id, base_meta)
        elif ext in {".json"}:
            return cls._load_json(p, doc_id, base_meta)
        elif ext in {".csv"}:
            return cls._load_csv(p, doc_id, base_meta)
        else:
            return cls._load_plaintext(p, doc_id, base_meta)

    @classmethod
    def _load_markdown(cls, p: Path, doc_id: str, meta: Dict[str, Any]) -> LoadedDocument:
        content = p.read_text(encoding="utf-8", errors="replace")
        title = p.stem.replace("_", " ").title()
        for line in content.splitlines():
            line_str = line.strip()
            if line_str.startswith("# "):
                title = line_str[2:].strip()
                break
        return LoadedDocument(
            doc_id=doc_id,
            title=title,
            content=content,
            source_path=str(p),
            doc_type="markdown",
            metadata=meta,
        )

    @classmethod
    def _load_python(cls, p: Path, doc_id: str, meta: Dict[str, Any]) -> LoadedDocument:
        content = p.read_text(encoding="utf-8", errors="replace")
        title = f"Python Module: {p.name}"
        return LoadedDocument(
            doc_id=doc_id,
            title=title,
            content=content,
            source_path=str(p),
            doc_type="python",
            metadata=meta,
        )

    @classmethod
    def _load_json(cls, p: Path, doc_id: str, meta: Dict[str, Any]) -> LoadedDocument:
        raw_text = p.read_text(encoding="utf-8", errors="replace")
        try:
            parsed = json.loads(raw_text)
            content = json.dumps(parsed, indent=2)
            title = parsed.get("title") or parsed.get("name") or p.stem
        except Exception:
            content = raw_text
            title = p.stem
        return LoadedDocument(
            doc_id=doc_id,
            title=str(title),
            content=content,
            source_path=str(p),
            doc_type="json",
            metadata=meta,
        )

    @classmethod
    def _load_csv(cls, p: Path, doc_id: str, meta: Dict[str, Any]) -> LoadedDocument:
        content = p.read_text(encoding="utf-8", errors="replace")
        title = f"Dataset: {p.stem}"
        return LoadedDocument(
            doc_id=doc_id,
            title=title,
            content=content,
            source_path=str(p),
            doc_type="csv",
            metadata=meta,
        )

    @classmethod
    def _load_plaintext(cls, p: Path, doc_id: str, meta: Dict[str, Any]) -> LoadedDocument:
        content = p.read_text(encoding="utf-8", errors="replace")
        title = p.stem.replace("_", " ").title()
        return LoadedDocument(
            doc_id=doc_id,
            title=title,
            content=content,
            source_path=str(p),
            doc_type="text",
            metadata=meta,
        )
