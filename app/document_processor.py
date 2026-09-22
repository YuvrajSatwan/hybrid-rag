"""
Document processor for Personal Documents.

Extracts text from PDF, Markdown, TXT, and HTML.
Chunks text using the existing chunking strategy (tiktoken, 500 tokens, 100 overlap).
Generates embeddings using Jina API (jina-embeddings-v3).
Stores chunks and embeddings in collection-isolated files.
"""
from __future__ import annotations

import io
import json
import logging
import os
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

from src.ingestion.chunker import chunk_text

load_dotenv()

logger = logging.getLogger(__name__)

JINA_URL = "https://api.jina.ai/v1/embeddings"
JINA_MODEL = "jina-embeddings-v3"
MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB limit
ALLOWED_EXTENSIONS = {".pdf", ".md", ".txt", ".html", ".htm"}


class _HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.title = ""
        self._in_title = False
        self._ignore = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._ignore = True
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._ignore = False
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
        elif not self._ignore:
            t = data.strip()
            if t:
                self.text_parts.append(t)

    def get_text(self) -> str:
        return " ".join(self.text_parts)


def extract_text_from_file(file_path: Path, filename: str) -> list[dict[str, Any]]:
    """
    Extract structured text from a document.
    Returns a list of sections: [{"text": ..., "page": int | None, "section": str}]
    """
    ext = Path(filename).suffix.lower()

    if ext == ".pdf":
        import pypdf
        sections = []
        with file_path.open("rb") as f:
            reader = pypdf.PdfReader(f)
            if reader.is_encrypted:
                try:
                    reader.decrypt("")
                except Exception:
                    raise ValueError("Password-protected or encrypted PDFs are not supported.")

            for i, page in enumerate(reader.pages, start=1):
                page_text = (page.extract_text() or "").strip()
                if page_text:
                    sections.append({
                        "text": page_text,
                        "page": i,
                        "section": f"Page {i}",
                    })

        if not sections:
            raise ValueError("No readable text found in PDF. It may be scanned or empty.")
        return sections

    elif ext in (".md", ".txt"):
        content = None
        for enc in ("utf-8", "latin-1", "cp1252"):
            try:
                content = file_path.read_text(encoding=enc)
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            raise ValueError("Unable to decode text file. Ensure it is UTF-8 or ASCII encoded.")

        content = content.strip()
        if not content:
            raise ValueError("Uploaded text file is empty.")

        # Try to infer title from first markdown header
        section_title = filename
        if ext == ".md":
            m = re.search(r"^#\s+(.+)$", content, flags=re.MULTILINE)
            if m:
                section_title = m.group(1).strip()

        return [{
            "text": content,
            "page": None,
            "section": section_title,
        }]

    elif ext in (".html", ".htm"):
        raw_html = file_path.read_text(encoding="utf-8", errors="replace")
        parser = _HTMLTextExtractor()
        parser.feed(raw_html)
        text = parser.get_text().strip()
        if not text:
            raise ValueError("No text content found in HTML file.")
        title = parser.title or filename
        return [{
            "text": text,
            "page": None,
            "section": title,
        }]

    else:
        raise ValueError(f"Unsupported file extension: {ext}. Supported: PDF, Markdown (.md), TXT, HTML.")


def embed_passages_jina(texts: list[str]) -> list[list[float]]:
    """Embed a list of chunk passages via the Jina embeddings API."""
    api_key = os.environ.get("JINA_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("JINA_API_KEY is not configured in .env")

    embeddings: list[list[float]] = []
    batch_size = 16

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        resp = requests.post(
            JINA_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": JINA_MODEL,
                "input": batch,
            },
            timeout=60,
        )
        if resp.status_code != 200:
            logger.error("Jina API error: %d - %s", resp.status_code, resp.text)
            raise RuntimeError(f"Embedding API failed ({resp.status_code}): {resp.text}")

        data = resp.json()
        for item in data["data"]:
            embeddings.append(item["embedding"])

    return embeddings


def process_and_index_document(
    coll_dir: Path,
    document_id: str,
    stored_filename: str,
    display_filename: str,
) -> int:
    """
    Ingest a document:
    1. Extract text sections (with page/section metadata)
    2. Chunk text using tiktoken strategy
    3. Generate embeddings with Jina
    4. Append chunks to chunks.jsonl and embeddings to embeddings.jsonl
    Returns total chunks generated.
    """
    file_path = coll_dir / "documents" / stored_filename
    if not file_path.exists():
        raise FileNotFoundError(f"Document file {stored_filename} not found")

    # Step 1: Extract text
    sections = extract_text_from_file(file_path, display_filename)

    # Step 2: Chunk text
    all_chunks: list[dict[str, Any]] = []
    chunk_index = 0

    for sec in sections:
        sec_text = sec["text"]
        page_num = sec.get("page")
        sec_title = sec.get("section") or display_filename

        raw_chunks = chunk_text(sec_text, chunk_size=500, overlap=100)
        for rc in raw_chunks:
            chunk_id = f"{document_id}_{chunk_index:04d}"
            all_chunks.append({
                "chunk_id": chunk_id,
                "document_id": document_id,
                "filename": display_filename,
                "title": f"{display_filename} — {sec_title}" if page_num is None else f"{display_filename} (Page {page_num})",
                "service": "Personal",
                "page": page_num,
                "section": sec_title,
                "text": rc,
                "source_url": "",  # Local documents have no web URL
            })
            chunk_index += 1

    if not all_chunks:
        raise ValueError("Document produced 0 text chunks.")

    # Step 3: Embed chunks
    chunk_texts = [c["text"] for c in all_chunks]
    embeddings = embed_passages_jina(chunk_texts)

    if len(embeddings) != len(all_chunks):
        raise RuntimeError(f"Embedding count mismatch: {len(embeddings)} vectors for {len(all_chunks)} chunks")

    # Step 4: Append to collection chunks.jsonl and embeddings.jsonl
    chunks_file = coll_dir / "chunks.jsonl"
    with chunks_file.open("a", encoding="utf-8") as f:
        for c in all_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    embeddings_file = coll_dir / "embeddings.jsonl"
    with embeddings_file.open("a", encoding="utf-8") as f:
        for c, emb in zip(all_chunks, embeddings):
            f.write(json.dumps({"chunk_id": c["chunk_id"], "embedding": emb}) + "\n")

    logger.info("Successfully indexed %d chunks for doc %s (%s)", len(all_chunks), document_id, display_filename)
    return len(all_chunks)
