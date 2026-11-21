"""
Semantic Document Chunker for Master AI
========================================
Splits documents into overlapping semantic chunks with heading awareness,
preserving context for dense and sparse retrieval.
"""

import re
from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class DocumentChunk:
    """Represents a discrete semantic chunk of a document."""
    text: str
    chunk_index: int
    total_chunks: int = 1
    heading: str = ""
    char_start: int = 0
    char_end: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class DocumentChunker:
    """Splits text and code into semantically coherent overlapping segments."""

    def __init__(
        self,
        target_chunk_size: int = 800,
        chunk_overlap: int = 100,
        min_chunk_size: int = 100,
    ):
        self.target_size = target_chunk_size
        self.overlap = chunk_overlap
        self.min_size = min_chunk_size

    def chunk_document(
        self,
        content: str,
        doc_type: str = "markdown",
        base_metadata: Dict[str, Any] = None,
    ) -> List[DocumentChunk]:
        """Route to appropriate chunker based on document type."""
        base_meta = base_metadata or {}
        doc_type = doc_type.lower().strip(".")

        if not content or not content.strip():
            return []

        if doc_type in {"md", "markdown"}:
            chunks = self._chunk_markdown(content)
        elif doc_type in {"py", "python"}:
            chunks = self._chunk_python(content)
        else:
            chunks = self._chunk_generic_text(content)

        # Populate total_chunks and merge base metadata
        total = len(chunks)
        for c in chunks:
            c.total_chunks = total
            merged_meta = dict(base_meta)
            merged_meta.update(c.metadata)
            c.metadata = merged_meta

        return chunks

    def _chunk_markdown(self, text: str) -> List[DocumentChunk]:
        """Split markdown along heading boundaries while keeping small sections together."""
        heading_re = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
        sections = []
        last_pos = 0
        current_heading = "Introduction"

        for match in heading_re.finditer(text):
            start = match.start()
            if start > last_pos:
                body = text[last_pos:start].strip()
                if body:
                    sections.append((current_heading, body, last_pos, start))
            current_heading = match.group(2).strip()
            last_pos = start

        # Tail
        tail = text[last_pos:].strip()
        if tail:
            sections.append((current_heading, tail, last_pos, len(text)))

        # If no headings found, fallback to generic
        if not sections:
            return self._chunk_generic_text(text)

        chunks: List[DocumentChunk] = []
        for heading, body, s_pos, e_pos in sections:
            if len(body) <= self.target_size:
                chunks.append(
                    DocumentChunk(
                        text=f"### {heading}\n{body}",
                        chunk_index=len(chunks),
                        heading=heading,
                        char_start=s_pos,
                        char_end=e_pos,
                        metadata={"heading": heading},
                    )
                )
            else:
                # Sub-chunk large section
                sub_chunks = self._split_with_overlap(body, heading)
                for sc in sub_chunks:
                    sc.chunk_index = len(chunks)
                    chunks.append(sc)

        return chunks

    def _chunk_python(self, code: str) -> List[DocumentChunk]:
        """Split Python code on class or top-level function boundaries."""
        block_re = re.compile(r"^(class\s+[A-Za-z0-9_]+|def\s+[A-Za-z0-9_]+)", re.MULTILINE)
        matches = list(block_re.finditer(code))

        if not matches:
            return self._chunk_generic_text(code)

        chunks: List[DocumentChunk] = []
        last_pos = 0
        current_def = "Module Header"

        for m in matches:
            start = m.start()
            if start > last_pos:
                block = code[last_pos:start].strip()
                if block:
                    chunks.append(
                        DocumentChunk(
                            text=block,
                            chunk_index=len(chunks),
                            heading=current_def,
                            char_start=last_pos,
                            char_end=start,
                            metadata={"code_symbol": current_def},
                        )
                    )
            current_def = m.group(1).strip()
            last_pos = start

        tail = code[last_pos:].strip()
        if tail:
            chunks.append(
                DocumentChunk(
                    text=tail,
                    chunk_index=len(chunks),
                    heading=current_def,
                    char_start=last_pos,
                    char_end=len(code),
                    metadata={"code_symbol": current_def},
                )
            )

        return chunks

    def _chunk_generic_text(self, text: str) -> List[DocumentChunk]:
        """Sliding window chunking with paragraph/sentence awareness."""
        return self._split_with_overlap(text, heading="General")

    def _split_with_overlap(self, text: str, heading: str) -> List[DocumentChunk]:
        """Sliding window splitting with character overlap."""
        chunks: List[DocumentChunk] = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = min(start + self.target_size, text_len)

            # Try to break at a natural newline or period boundary
            if end < text_len:
                break_point = text.rfind("\n\n", start, end)
                if break_point == -1 or break_point < start + self.min_size:
                    break_point = text.rfind("\n", start, end)
                if break_point == -1 or break_point < start + self.min_size:
                    break_point = text.rfind(". ", start, end)
                if break_point != -1 and break_point >= start + self.min_size:
                    end = break_point + 1

            chunk_text = text[start:end].strip()
            if len(chunk_text) >= self.min_size or not chunks:
                chunks.append(
                    DocumentChunk(
                        text=chunk_text,
                        chunk_index=len(chunks),
                        heading=heading,
                        char_start=start,
                        char_end=end,
                        metadata={"heading": heading},
                    )
                )

            # Advance with overlap
            advance = (end - start) - self.overlap
            if advance <= 0:
                advance = max(1, end - start)
            start += advance

        return chunks
