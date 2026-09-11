"""
V2-B — Dense + BM25 hybrid retrieval via Reciprocal Rank Fusion (RRF).

Why not just add the scores?
    Dense cosine scores live in roughly [0, 1]. BM25 scores are unbounded and
    corpus-dependent (they can be 5, 20, 40+). Adding raw scores would let BM25
    silently dominate, and any min-max normalization would be fragile to
    outliers and to the particular query. RRF sidesteps scale entirely by using
    only the RANK a document gets from each retriever.

RRF:
    For a document d that a retriever ranks at position rank(d) (1-based):

        RRF(d) = Σ_retrievers  1 / (k + rank(d))

    Documents not returned by a retriever simply get no contribution from it.
    We fuse the top-N of each retriever (N = FUSE_DEPTH), then take the Top-K.

    k (RRF_K) = 60. This is the standard value from the original RRF paper
    (Cormack et al., 2009). Intuition: k dampens how much the very top ranks
    dominate — with k=60, rank 1 gives 1/61 and rank 2 gives 1/62, so early
    ranks are weighted similarly and a document must rank well in BOTH systems
    (or very high in one) to rise. We keep the literature default rather than
    tuning against our own benchmark (that would leak the test set).

    FUSE_DEPTH = 100. We fuse each retriever's top-100 candidates. Deep enough
    that a gold chunk sitting at, say, dense-rank 40 can still be rescued by a
    strong BM25 rank, but bounded for speed.
"""

import sys

from src.retrieval.bm25 import BM25Retriever
from src.retrieval.dense import DenseRetriever
from src.retrieval.evaluate import (
    CATEGORY_VALUES, HOP_VALUES, SERVICE_VALUES, EVAL_DIR,
    load_chunks, load_questions, evaluate_retriever,
    print_overall, print_group_table, print_failures, print_unanswerable,
    save_evaluation,
)

RRF_K = 60
FUSE_DEPTH = 100


def rrf_fuse(ranked_lists: list[list[str]], k: int = RRF_K) -> list[tuple[str, float]]:
    """Fuse multiple ranked chunk_id lists with Reciprocal Rank Fusion.
    Returns (chunk_id, rrf_score) sorted descending."""
    scores: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, cid in enumerate(ranked, start=1):
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)


class HybridRetriever:
    def __init__(self, dense: DenseRetriever, bm25: BM25Retriever,
                 fuse_depth: int = FUSE_DEPTH, k: int = RRF_K):
        self.dense = dense
        self.bm25 = bm25
        self.fuse_depth = fuse_depth
        self.k = k

    def rank_with_scores(self, query: str, top_k: int = 10):
        dense_ids = self.dense.rank(query, self.fuse_depth)
        bm25_ids = self.bm25.rank(query, self.fuse_depth)
        fused = rrf_fuse([dense_ids, bm25_ids], self.k)
        return fused[:top_k]

    def rank(self, query: str, top_k: int = 10) -> list[str]:
        return [cid for cid, _ in self.rank_with_scores(query, top_k)]


def build_retriever():
    """Shared entry point reused by reranker.py."""
    chunks = load_chunks()
    dense = DenseRetriever()
    bm25 = BM25Retriever(chunks)
    return HybridRetriever(dense, bm25), chunks


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("Building hybrid retriever (dense + BM25)...")
    retriever, chunks = build_retriever()
    questions = load_questions()

    # Pre-warm query embeddings (cached; no cost if already embedded).
    print("Ensuring query embeddings are cached...")
    for q in questions:
        retriever.dense.embed_query(q["question"])

    results, overall = evaluate_retriever(
        retriever.rank, questions, top_k=10, label="V2-B Hybrid",
    )

    print_overall(f"V2-B Hybrid (Dense + BM25, RRF k={RRF_K}, fuse_depth={FUSE_DEPTH})", overall)
    print_group_table(results, "type", CATEGORY_VALUES, "CATEGORY-WISE")
    print_group_table(results, "hop", HOP_VALUES, "HOP-WISE")
    print_group_table(results, "service", SERVICE_VALUES, "SERVICE-WISE")
    print_failures(results)
    print_unanswerable(results)

    save_evaluation(
        EVAL_DIR / "hybrid_v2b_evaluation.json",
        config={
            "retrieval": "hybrid_dense_bm25_rrf",
            "fusion": "reciprocal_rank_fusion",
            "rrf_k": RRF_K,
            "fuse_depth": FUSE_DEPTH,
            "dense_model": "jina-embeddings-v3 (reused V1 embeddings)",
            "bm25": "rank_bm25 BM25Okapi k1=1.5 b=0.75",
            "top_k_evaluated": 10,
        },
        overall=overall,
        results=results,
    )


if __name__ == "__main__":
    main()
