"""
V2-C — Hybrid retrieval + cross-encoder reranker.

Pipeline:
    query
      -> dense top-N  +  bm25 top-N
      -> RRF fusion              (candidate generation, from hybrid.py)
      -> take top RERANK_DEPTH candidates
      -> cross-encoder scores each (query, chunk_text) pair directly
      -> re-sort -> Top-K final

Bi-encoder vs cross-encoder:
    Bi-encoder (dense/Jina): encodes query and document SEPARATELY into vectors,
    then compares with cosine. Fast (documents pre-encoded once), but the query
    and document never "see" each other — matching is coarse.

    Cross-encoder (reranker): feeds "query [SEP] document" through the model
    TOGETHER and outputs one relevance score. Far more accurate because it does
    full cross-attention between query and document tokens — but it cannot be
    pre-computed, so we only run it on a small candidate set, never the corpus.
    That is why reranking happens AFTER candidate generation.

Model choice:
    cross-encoder/ms-marco-MiniLM-L-6-v2 — the standard, small (~80MB), CPU-
    friendly English reranker trained on MS MARCO passage ranking. Chosen for
    explainability and low latency over larger BGE/monoT5 rerankers; this is a
    learning/interview project, not a leaderboard chase.

RERANK_DEPTH = 30: rerank the top-30 fused candidates. Deep enough to recover a
gold chunk that fusion ranked at, say, 20; shallow enough that per-query cross-
encoder cost stays modest (30 pairs).
"""

import sys

from sentence_transformers import CrossEncoder

from src.retrieval.hybrid import HybridRetriever, RRF_K, FUSE_DEPTH
from src.retrieval.bm25 import BM25Retriever
from src.retrieval.dense import DenseRetriever
from src.retrieval.evaluate import (
    CATEGORY_VALUES, HOP_VALUES, SERVICE_VALUES, EVAL_DIR,
    load_chunks, load_questions, evaluate_retriever,
    print_overall, print_group_table, print_failures, print_unanswerable,
    save_evaluation,
)

RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_DEPTH = 30


class RerankRetriever:
    def __init__(self, hybrid: HybridRetriever, chunks: dict[str, dict],
                 model_name: str = RERANK_MODEL, depth: int = RERANK_DEPTH):
        self.hybrid = hybrid
        self.chunks = chunks
        self.depth = depth
        self.model = CrossEncoder(model_name)

    def rank(self, query: str, top_k: int = 10) -> list[str]:
        # 1) candidate generation via hybrid RRF
        candidates = self.hybrid.rank(query, self.depth)
        # 2) cross-encoder scores each (query, doc) pair
        pairs = [(query, self.chunks[c]["text"]) for c in candidates]
        scores = self.model.predict(pairs)
        # 3) re-sort candidates by cross-encoder score
        reranked = sorted(
            zip(candidates, scores),
            key=lambda cs: cs[1],
            reverse=True,
        )
        return [c for c, _ in reranked[:top_k]]


def build_retriever():
    chunks = load_chunks()
    dense = DenseRetriever()
    bm25 = BM25Retriever(chunks)
    hybrid = HybridRetriever(dense, bm25, fuse_depth=FUSE_DEPTH, k=RRF_K)
    return RerankRetriever(hybrid, chunks), chunks


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("Building hybrid + reranker...")
    retriever, chunks = build_retriever()
    questions = load_questions()

    print("Ensuring query embeddings are cached...")
    for q in questions:
        retriever.hybrid.dense.embed_query(q["question"])

    results, overall = evaluate_retriever(
        retriever.rank, questions, top_k=10, label="V2-C Hybrid+Reranker",
    )

    print_overall(
        f"V2-C Hybrid + Reranker ({RERANK_MODEL}, rerank_depth={RERANK_DEPTH})",
        overall,
    )
    print_group_table(results, "type", CATEGORY_VALUES, "CATEGORY-WISE")
    print_group_table(results, "hop", HOP_VALUES, "HOP-WISE")
    print_group_table(results, "service", SERVICE_VALUES, "SERVICE-WISE")
    print_failures(results)
    print_unanswerable(results)

    save_evaluation(
        EVAL_DIR / "hybrid_reranker_v2c_evaluation.json",
        config={
            "retrieval": "hybrid_dense_bm25_rrf + cross_encoder_rerank",
            "candidate_generation": f"RRF(k={RRF_K}, fuse_depth={FUSE_DEPTH}) top-{RERANK_DEPTH}",
            "reranker_model": RERANK_MODEL,
            "reranker_type": "cross-encoder",
            "rerank_depth": RERANK_DEPTH,
            "top_k_evaluated": 10,
        },
        overall=overall,
        results=results,
    )


if __name__ == "__main__":
    main()
