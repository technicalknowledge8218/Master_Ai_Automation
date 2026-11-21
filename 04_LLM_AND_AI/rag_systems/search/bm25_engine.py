"""
Pure-Python Okapi BM25 Sparse Search Engine for Master AI
=========================================================
Implements BM25 keyword search with inverted index, term frequency calculation,
and persistence without external C dependencies.
"""

import math
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Common English stopwords
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
    "to", "was", "were", "will", "with", "or", "this", "but", "they",
}


def tokenize(text: str) -> List[str]:
    """Normalize and tokenize text into lowercase terms."""
    if not text:
        return []
    words = re.findall(r"[a-z0-9_\-]+", text.lower())
    return [w for w in words if len(w) > 1 and w not in STOPWORDS]


class BM25Engine:
    """Okapi BM25 ranker with JSON persistence."""

    def __init__(
        self,
        k1: float = 1.5,
        b: float = 0.75,
        index_file: Optional[Path | str] = None,
    ):
        self.k1 = k1
        self.b = b
        self.index_file = Path(index_file) if index_file else None

        # Index data structures
        self.doc_count: int = 0
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_len: float = 0.0
        self.doc_term_freqs: Dict[str, Dict[str, int]] = {}
        self.term_doc_freqs: Dict[str, int] = {}
        self.doc_metadata: Dict[str, Dict[str, Any]] = {}

        if self.index_file and self.index_file.exists():
            self.load()

    def add_document(self, doc_id: str, text: str, metadata: Optional[Dict[str, Any]] = None):
        """Index a single text document or chunk."""
        tokens = tokenize(text)
        if not tokens:
            return

        # Check if already present and remove old stats
        if doc_id in self.doc_lengths:
            self.remove_document(doc_id)

        doc_len = len(tokens)
        self.doc_lengths[doc_id] = doc_len
        self.doc_count += 1
        self.doc_metadata[doc_id] = metadata or {}

        tf: Dict[str, int] = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
        self.doc_term_freqs[doc_id] = tf

        for t in tf.keys():
            self.term_doc_freqs[t] = self.term_doc_freqs.get(t, 0) + 1

        total_len = sum(self.doc_lengths.values())
        self.avg_doc_len = total_len / self.doc_count if self.doc_count > 0 else 0.0

    def remove_document(self, doc_id: str):
        """Remove document from BM25 index."""
        if doc_id not in self.doc_lengths:
            return

        del self.doc_lengths[doc_id]
        self.doc_count -= 1
        if doc_id in self.doc_metadata:
            del self.doc_metadata[doc_id]

        if doc_id in self.doc_term_freqs:
            for t in self.doc_term_freqs[doc_id].keys():
                self.term_doc_freqs[t] = max(0, self.term_doc_freqs.get(t, 1) - 1)
                if self.term_doc_freqs[t] == 0:
                    del self.term_doc_freqs[t]
            del self.doc_term_freqs[doc_id]

        total_len = sum(self.doc_lengths.values())
        self.avg_doc_len = total_len / self.doc_count if self.doc_count > 0 else 0.0

    def _idf(self, term: str) -> float:
        """Compute Robertson-Spärck Jones IDF."""
        df = self.term_doc_freqs.get(term, 0)
        if df == 0:
            return 0.0
        # Standard BM25 IDF with smoothing
        return math.log(((self.doc_count - df + 0.5) / (df + 0.5)) + 1.0)

    def search(
        self,
        query: str,
        limit: int = 10,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Score all matching documents for the query."""
        query_terms = tokenize(query)
        if not query_terms or self.doc_count == 0:
            return []

        scores: Dict[str, float] = {}
        matched_terms: Dict[str, List[str]] = {}

        for term in query_terms:
            idf = self._idf(term)
            if idf <= 0.0:
                continue

            for doc_id, tf_dict in self.doc_term_freqs.items():
                # Apply metadata filter
                if filter_metadata:
                    meta = self.doc_metadata.get(doc_id, {})
                    if not all(meta.get(k) == v for k, v in filter_metadata.items()):
                        continue

                tf = tf_dict.get(term, 0)
                if tf == 0:
                    continue

                d_len = self.doc_lengths.get(doc_id, 1)
                num = tf * (self.k1 + 1.0)
                denom = tf + self.k1 * (1.0 - self.b + self.b * (d_len / (self.avg_doc_len or 1.0)))
                term_score = idf * (num / denom)

                scores[doc_id] = scores.get(doc_id, 0.0) + term_score
                matched_terms.setdefault(doc_id, []).append(term)

        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]

        results = []
        for doc_id, score in sorted_docs:
            results.append({
                "id": doc_id,
                "score": float(score),
                "matched_terms": matched_terms.get(doc_id, []),
                "payload": self.doc_metadata.get(doc_id, {}),
            })
        return results

    def save(self):
        """Persist BM25 index to disk."""
        if not self.index_file:
            return
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "doc_count": self.doc_count,
            "avg_doc_len": self.avg_doc_len,
            "doc_lengths": self.doc_lengths,
            "term_doc_freqs": self.term_doc_freqs,
            "doc_term_freqs": self.doc_term_freqs,
            "doc_metadata": self.doc_metadata,
        }
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load(self):
        """Load BM25 index from disk."""
        if not self.index_file or not self.index_file.exists():
            return
        with open(self.index_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.doc_count = data.get("doc_count", 0)
            self.avg_doc_len = data.get("avg_doc_len", 0.0)
            self.doc_lengths = data.get("doc_lengths", {})
            self.term_doc_freqs = data.get("term_doc_freqs", {})
            self.doc_term_freqs = data.get("doc_term_freqs", {})
            self.doc_metadata = data.get("doc_metadata", {})
