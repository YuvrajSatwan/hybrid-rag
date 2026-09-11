"""
Dense retriever for V2 (reuses the frozen V1 embeddings).

This does NOT re-embed the corpus. It loads the 1,502 pre-computed
`jina-embeddings-v3` chunk vectors from data/processed/embeddings.jsonl and
ranks by cosine similarity — identical retrieval math to V1's search.py.

The only online cost is embedding the QUERY. We call the Jina API directly
with `requests` (the project's langchain_community wrapper is no longer
installed) and CACHE query vectors to disk so hybrid / reranker stages don't
re-hit the API. The frozen V1 baseline file is never touched.

Unlike V1's cached eval (top-10 only), this returns a FULL ranking over all
chunks, which hybrid RRF needs.
"""

import json
import os
from pathlib import Path

import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()

EMBEDDINGS_PATH = Path("data/processed/embeddings.jsonl")
QUERY_CACHE_PATH = Path("data/processed/query_embeddings_cache.json")

JINA_URL = "https://api.jina.ai/v1/embeddings"
JINA_MODEL = "jina-embeddings-v3"


# =============================================================================
# QUERY EMBEDDING (Jina API, cached)
# =============================================================================

def _load_query_cache() -> dict:
    if QUERY_CACHE_PATH.exists():
        with QUERY_CACHE_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_query_cache(cache: dict) -> None:
    QUERY_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with QUERY_CACHE_PATH.open("w", encoding="utf-8") as f:
        json.dump(cache, f)


def _embed_query_api(text: str) -> list[float]:
    api_key = os.environ["JINA_API_KEY"]
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
    return resp.json()["data"][0]["embedding"]


class DenseRetriever:
    def __init__(self):
        self.chunk_ids = []
        vectors = []
        with EMBEDDINGS_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    self.chunk_ids.append(rec["chunk_id"])
                    vectors.append(rec["embedding"])

        # De-duplicate chunk_ids the same way V1's dict-keyed loader does:
        # keep the LAST occurrence (dict last-write-wins), so index positions
        # match the answerable corpus of 1,495 unique ids.
        last_index = {}
        for i, cid in enumerate(self.chunk_ids):
            last_index[cid] = i
        keep = sorted(last_index.values())
        self.chunk_ids = [self.chunk_ids[i] for i in keep]
        matrix = np.array([vectors[i] for i in keep], dtype=np.float32)

        # Pre-normalize corpus vectors so cosine = dot product.
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.matrix = matrix / norms

        self._cache = _load_query_cache()

    def embed_query(self, query: str) -> np.ndarray:
        if query not in self._cache:
            self._cache[query] = _embed_query_api(query)
            _save_query_cache(self._cache)
        v = np.array(self._cache[query], dtype=np.float32)
        n = np.linalg.norm(v)
        return v / n if n else v

    def rank_with_scores(self, query: str, top_k: int | None = None):
        """Return list of (chunk_id, cosine_score) sorted descending."""
        q = self.embed_query(query)
        scores = self.matrix @ q  # cosine (both normalized)
        order = np.argsort(-scores)
        if top_k is not None:
            order = order[:top_k]
        return [(self.chunk_ids[i], float(scores[i])) for i in order]

    def rank(self, query: str, top_k: int = 10) -> list[str]:
        return [cid for cid, _ in self.rank_with_scores(query, top_k)]


def prewarm_query_cache(questions):
    """Embed all benchmark queries up front (one API call each, then cached)."""
    r = DenseRetriever()
    missing = [q["question"] for q in questions if q["question"] not in r._cache]
    for i, text in enumerate(missing, 1):
        r.embed_query(text)
        print(f"  embedded query {i}/{len(missing)}")
    return r
