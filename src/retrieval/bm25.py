"""
V2-A — BM25 lexical retrieval.

Pipeline:
    chunks -> tokenize text -> BM25 index -> query tokens -> BM25 scores
    -> ranked Top-K chunk_ids

Why BM25 (lexical) complements dense retrieval:
    Dense embeddings match on *meaning*. They can miss exact tokens like
    `ec_num_parity_fragments`, `nova-manage`, `fernet_rotate`, port numbers,
    or CLI flags, because those rare tokens are smoothed into a semantic
    average. BM25 scores on *exact token overlap*, so precise technical /
    configuration terms score highly. That is exactly the V1 weakness
    (exact_terminology / technical_detail misses) we want to attack.

BM25 scoring (Okapi BM25), per query term t in document d:

    score += IDF(t) * ( f(t,d) * (k1 + 1) )
                       ---------------------------------------------
                       f(t,d) + k1 * (1 - b + b * |d| / avgdl)

    - f(t,d)  term frequency: how often t appears in d.
    - IDF(t)  inverse document frequency: rare terms across the corpus
              carry more weight than common ones.
    - |d|/avgdl  length normalization: without it, long documents win just
              by containing more words; b controls how strongly we correct
              for that.
    - k1 (default 1.5) controls TF saturation (diminishing returns on repeats).
    - b  (default 0.75) controls how much length normalization is applied.

We keep rank_bm25's defaults (k1=1.5, b=0.75) — standard, well-understood, and
we are not tuning against the benchmark (that would leak the test set).

Tokenization is deliberately simple and reproducible: lowercase, then split on
non-alphanumeric while KEEPING underscores/dots/hyphens joined inside a token
is NOT done — instead we split into alphanumeric runs but also emit the raw
underscore/hyphen forms so that `ec_num_parity_fragments` is matchable both as
the whole token and as its parts. See `tokenize()`.
"""

import re
import sys

from rank_bm25 import BM25Okapi

from src.retrieval.evaluate import (
    CATEGORY_VALUES, HOP_VALUES, SERVICE_VALUES, EVAL_DIR,
    load_chunks, load_questions, evaluate_retriever,
    print_overall, print_group_table, print_failures, print_unanswerable,
    save_evaluation,
)


# =============================================================================
# TOKENIZATION
# =============================================================================

_TOKEN_RE = re.compile(r"[a-z0-9]+(?:[._-][a-z0-9]+)*")


def tokenize(text: str) -> list[str]:
    """
    Lowercase and extract tokens.

    A token is an alphanumeric run, optionally joined by ._- to keep
    identifiers like `ec_num_parity_fragments`, `nova-manage`, or
    `object.ring.gz` intact. We ALSO append the split sub-parts so a query
    that says "num parity fragments" can still match the compound token.
    """
    text = text.lower()
    tokens = []
    for match in _TOKEN_RE.findall(text):
        tokens.append(match)
        # also emit sub-parts for compound identifiers (num, parity, fragments)
        if any(sep in match for sep in "._-"):
            parts = re.split(r"[._-]", match)
            tokens.extend(p for p in parts if p)
    return tokens


# =============================================================================
# BM25 INDEX
# =============================================================================

class BM25Retriever:
    def __init__(self, chunks: dict[str, dict]):
        # Fixed ordering so index positions map back to chunk_ids deterministically.
        self.chunk_ids = list(chunks.keys())
        self.corpus_tokens = [tokenize(chunks[c]["text"]) for c in self.chunk_ids]
        self.bm25 = BM25Okapi(self.corpus_tokens)  # k1=1.5, b=0.75 defaults

    def rank(self, query: str, top_k: int = 10) -> list[str]:
        scores = self.bm25.get_scores(tokenize(query))
        # argsort descending; take top_k
        ranked = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )[:top_k]
        return [self.chunk_ids[i] for i in ranked]


# =============================================================================
# MAIN
# =============================================================================

def build_retriever():
    """Shared entry point reused by hybrid.py."""
    chunks = load_chunks()
    return BM25Retriever(chunks), chunks


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("Building BM25 index...")
    retriever, chunks = build_retriever()
    print(f"Indexed {len(retriever.chunk_ids)} chunks.")

    questions = load_questions()
    results, overall = evaluate_retriever(
        retriever.rank, questions, top_k=10, label="V2-A BM25",
    )

    print_overall("V2-A BM25 (lexical, rank_bm25 Okapi, k1=1.5 b=0.75)", overall)
    print_group_table(results, "type", CATEGORY_VALUES, "CATEGORY-WISE")
    print_group_table(results, "hop", HOP_VALUES, "HOP-WISE")
    print_group_table(results, "service", SERVICE_VALUES, "SERVICE-WISE")
    print_failures(results)
    print_unanswerable(results)

    save_evaluation(
        EVAL_DIR / "bm25_v2a_evaluation.json",
        config={
            "retrieval": "bm25",
            "library": "rank_bm25 (BM25Okapi)",
            "k1": 1.5,
            "b": 0.75,
            "tokenization": "lowercase; alphanumeric runs joined by ._- ; compound identifiers also split into sub-parts",
            "top_k_evaluated": 10,
        },
        overall=overall,
        results=results,
    )


if __name__ == "__main__":
    main()
