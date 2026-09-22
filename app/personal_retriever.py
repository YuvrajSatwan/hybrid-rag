"""
Personal collection retriever.

Reuses the exact same retrieval pipeline as V2:
    Dense (cosine similarity via Jina query embedding)
  + BM25 (BM25Okapi lexical retrieval)
  → RRF (Reciprocal Rank Fusion, k=60)
  → CrossEncoder reranker (ms-marco-MiniLM-L-6-v2)
  → Top-K final chunks

Guarantees 100% collection isolation:
Only searches within the specified collection's chunks.jsonl and embeddings.jsonl.
Never touches or queries the OpenStack benchmark data.
"""
from __future__ import annotations

import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any

import numpy as np
import requests
from rank_bm25 import BM25Okapi

logger = logging.getLogger(__name__)

RRF_K = 60
RERANK_DEPTH = 30
JINA_URL = "https://api.jina.ai/v1/embeddings"
JINA_MODEL = "jina-embeddings-v3"

_WORKSPACE_QUERY_CACHE: dict[str, list[float]] = {}


def _embed_workspace_query(text: str) -> list[float]:
    """Embed query via Jina API with isolated in-memory cache to never touch data/processed/."""
    if text in _WORKSPACE_QUERY_CACHE:
        return _WORKSPACE_QUERY_CACHE[text]
    api_key = os.environ.get("JINA_API_KEY", "")
    resp = requests.post(
        JINA_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": JINA_MODEL, "input": [text]},
        timeout=60,
    )
    resp.raise_for_status()
    vec = resp.json()["data"][0]["embedding"]
    _WORKSPACE_QUERY_CACHE[text] = vec
    return vec


def _simple_tokenize(text: str) -> list[str]:
    """Tokenize lowercase words/numbers for BM25, consistent with V2 BM25Retriever."""
    return re.findall(r"\w+", text.lower())



class PersonalCollectionRetriever:
    """Retriever for a specific personal collection."""

    def __init__(self, coll_dir: Path, reranker_model=None):
        self.coll_dir = coll_dir
        self.reranker_model = reranker_model

        self.chunks: dict[str, dict[str, Any]] = {}
        self.chunk_ids: list[str] = []
        self.matrix: np.ndarray | None = None
        self.bm25: BM25Okapi | None = None

        self._load_index()

    def _load_index(self) -> None:
        chunks_file = self.coll_dir / "chunks.jsonl"
        emb_file = self.coll_dir / "embeddings.jsonl"

        if not chunks_file.exists() or not emb_file.exists():
            return

        # Load chunks
        with chunks_file.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    c = json.loads(line)
                    self.chunks[c["chunk_id"]] = c

        if not self.chunks:
            return

        # Load embeddings in order
        vectors = []
        cids = []
        with emb_file.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    cid = rec["chunk_id"]
                    if cid in self.chunks:
                        cids.append(cid)
                        vectors.append(rec["embedding"])

        if not vectors:
            return

        self.chunk_ids = cids
        mat = np.array(vectors, dtype=np.float32)
        # Normalize for cosine similarity
        norms = np.linalg.norm(mat, axis=1, keepdims=True)
        norms[norms == 0] = 1e-10
        self.matrix = mat / norms

        # Build BM25 index over collection chunks
        corpus_tokens = [
            _simple_tokenize(self.chunks[cid].get("text", ""))
            for cid in self.chunk_ids
        ]
        self.bm25 = BM25Okapi(corpus_tokens)

        logger.info(
            "Loaded personal retriever for %s: %d chunks, matrix %s",
            self.coll_dir.name,
            len(self.chunk_ids),
            self.matrix.shape,
        )

    def is_empty(self) -> bool:
        return len(self.chunk_ids) == 0 or self.matrix is None or self.bm25 is None

    def rank(self, query: str, top_k: int = 10) -> list[dict[str, Any]]:
        """
        Execute full V2 retrieval over the personal collection:
        1. Dense retrieval (cosine similarity)
        2. BM25 retrieval
        3. RRF fusion
        4. Cross-encoder reranker
        """
        if self.is_empty():
            return []

        # -------------------------------------------------------------
        # 1. Dense retrieval
        # -------------------------------------------------------------
        t_embed_start = time.perf_counter()
        q_vec = np.array(_embed_workspace_query(query), dtype=np.float32)
        t_embed_end = time.perf_counter()
        logger.info("STAGE_LATENCY | stage=jina_embedding | latency_ms=%.2f", (t_embed_end - t_embed_start) * 1000)

        t_dense_start = time.perf_counter()
        q_norm = np.linalg.norm(q_vec)

        if q_norm > 0:
            q_vec /= q_norm
        dense_scores = self.matrix @ q_vec
        dense_ranking = [self.chunk_ids[i] for i in np.argsort(-dense_scores)]
        t_dense_end = time.perf_counter()
        logger.info("STAGE_LATENCY | stage=dense_retrieval | latency_ms=%.2f", (t_dense_end - t_dense_start) * 1000)

        # -------------------------------------------------------------
        # 2. BM25 retrieval
        # -------------------------------------------------------------
        t_bm25_start = time.perf_counter()
        q_tokens = _simple_tokenize(query)
        bm25_scores = self.bm25.get_scores(q_tokens)
        bm25_ranking = [self.chunk_ids[i] for i in np.argsort(-bm25_scores)]
        t_bm25_end = time.perf_counter()
        logger.info("STAGE_LATENCY | stage=bm25_retrieval | latency_ms=%.2f", (t_bm25_end - t_bm25_start) * 1000)

        # -------------------------------------------------------------
        # 3. RRF Fusion (identical formula to V2 HybridRetriever)
        # -------------------------------------------------------------
        t_rrf_start = time.perf_counter()
        rrf_scores: dict[str, float] = {}
        for rank_idx, cid in enumerate(dense_ranking, start=1):
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (RRF_K + rank_idx))

        for rank_idx, cid in enumerate(bm25_ranking, start=1):
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (RRF_K + rank_idx))

        fused_candidates = sorted(rrf_scores.keys(), key=lambda c: rrf_scores[c], reverse=True)
        top_candidates = fused_candidates[: min(RERANK_DEPTH, len(fused_candidates))]
        t_rrf_end = time.perf_counter()
        logger.info("STAGE_LATENCY | stage=rrf_fusion | latency_ms=%.2f", (t_rrf_end - t_rrf_start) * 1000)

        # -------------------------------------------------------------
        # 4. CrossEncoder Reranker (reusing loaded model if available)
        # -------------------------------------------------------------
        t_rerank_start = time.perf_counter()
        if self.reranker_model is not None and top_candidates:
            pairs = [[query, self.chunks[cid]["text"]] for cid in top_candidates]
            ce_scores = self.reranker_model.predict(pairs)
            reranked = sorted(
                zip(top_candidates, ce_scores),
                key=lambda x: x[1],
                reverse=True,
            )
            final_cids = [cid for cid, _ in reranked[:top_k]]
        else:
            final_cids = top_candidates[:top_k]
        t_rerank_end = time.perf_counter()
        logger.info("STAGE_LATENCY | stage=crossencoder_reranking | latency_ms=%.2f", (t_rerank_end - t_rerank_start) * 1000)

        return [self.chunks[cid] for cid in final_cids if cid in self.chunks]
