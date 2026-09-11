# SIMPLE-RAG

A retrieval RAG over the **OpenStack 2026.1 documentation** — built evaluation-first.

The point of this project isn't "I made a chatbot." It's a **measured retrieval pipeline**: a 100-question benchmark with strict multi-hop gold sets, an honest diagnosis of where dense retrieval breaks, and three incremental upgrades (BM25 → hybrid → reranker) each measured against the same ruler.

---

## The one interesting finding

Dense retrieval is great at finding *something* relevant. It's much worse at finding *everything* a question needs.

| A question needs… | Retriever finds **at least one** gold chunk | Retriever finds **every** gold chunk |
|---|:--:|:--:|
| 1 chunk (single-hop) | 78% | **78%** |
| 2 chunks (two-hop) | 76% | **36%** |
| 3+ chunks (multi-hop / cross-doc) | 80% | **20%** |

The "find at least one" number barely moves. The "find all of them" number **collapses**. That gap is the whole story — and it's invisible if you only track ordinary Recall@K. V2 goes after it.

---

## Results: V1 → V2 (same 100-Q benchmark throughout)

| Stage | Any-Gold@10 | All-Gold@10 | Coverage@10 | MRR@10 |
|---|:--:|:--:|:--:|:--:|
| V1 Dense (`jina-embeddings-v3`) | 77.9% | 61.1% | 69.8% | 0.533 |
| V2-A BM25 (lexical) | 76.8% | 57.9% | 67.4% | 0.517 |
| V2-B Hybrid (dense + BM25, RRF) | 84.2% | 63.2% | 74.4% | 0.559 |
| **V2-C Hybrid + reranker** | **87.4%** | **68.4%** | **78.9%** | **0.665** |

The two-stage retrieve-then-rerank pipeline lifts **MRR +25%** and **All-Gold@10 +7.3 pts** over the dense baseline. The reranker is the biggest single jump — cross-attention pulls the right chunk sharply toward the top.

📄 Full write-ups: [`v1_report.md`](v1_report.md) · [`v2_report.md`](v2_report.md) · decisions in [`docs/V2_DECISIONS.md`](docs/V2_DECISIONS.md) · concepts in [`docs/V2_INTERVIEW_NOTES.md`](docs/V2_INTERVIEW_NOTES.md)

---

## Pipeline (V2-C)

```
141 OpenStack docs
      │  chunk (tiktoken cl100k_base · 500 tokens · 100 overlap) · embed (Jina v3)
      ▼
1,495 chunks/vectors
      │
      ├─► dense cosine ──── top-100 ─┐
      ├─► BM25 (Okapi)  ──── top-100 ─┤
      │                               ▼
      │                    RRF fusion (k=60) → top-30
      │                               ▼
      │        cross-encoder rerank (ms-marco-MiniLM-L-6-v2)
      ▼                               ▼
100-question benchmark ──eval──▶  Top-10 + metrics + failure analysis
```

## Quickstart

```bash
pip install tiktoken numpy rank_bm25 sentence-transformers python-dotenv requests
echo "JINA_API_KEY=your_key_here" > .env

python -m src.retrieval.bm25       # V2-A  -> bm25_v2a_evaluation.json
python -m src.retrieval.hybrid     # V2-B  -> hybrid_v2b_evaluation.json
python -m src.retrieval.reranker   # V2-C  -> hybrid_reranker_v2c_evaluation.json
```

Processed data, cached query embeddings, and all evaluation JSONs are committed, so the V2 stages run out of the box. The `JINA_API_KEY` is only needed to embed queries not already in the cache.

## Repo layout

```
src/ingestion/     chunker.py, loader.py           # docs -> chunks
src/retrieval/     embedding.py, search.py          # V1 dense (frozen)
                   evaluate.py                       # shared eval harness (all stages)
                   bm25.py, hybrid.py, reranker.py   # V2-A / V2-B / V2-C
data/processed/    chunks.jsonl, embeddings.jsonl, query_embeddings_cache.json
data/benchmark/    dev_questions.json                # the 100-question benchmark
data/benchmark/evaluation/                           # one eval JSON per stage
v1_report.md, v2_report.md                           # frozen analyses
docs/              V2_DECISIONS.md, V2_INTERVIEW_NOTES.md
```

## The benchmark

100 hand-verified questions, every gold ID checked against the actual corpus (no invented chunks, no answers from general OpenStack knowledge). Nine types spanning single-hop → multi-hop → cross-document, plus 5 **unanswerable** questions whose topics were confirmed absent from the corpus.

Two recall metrics, on purpose:
- **Any-Gold** — *can it find relevant evidence?*
- **All-Gold (strict)** — *can it find the **complete** evidence set the question requires?*

## What V2 tested — one hypothesis at a time

Everything (corpus, chunks, benchmark, metrics, Top-K) stays frozen so each upgrade is measured against the same ruler. The success metric is **not** "higher Recall@10" — it's *which failure mode each strategy actually fixes.*

| Stage | Hypothesis | Verdict |
|---|---|---|
| **V2-A** BM25 | Lexical retrieval fixes exact-term misses | Worse alone, but wins 8 queries dense misses → complementary |
| **V2-B** Dense + BM25 (RRF) | The evidence is complementary | ✅ beats both parents on every headline metric |
| **V2-C** Hybrid + reranker | Reranking closes the multi-hop / cross-doc gap | Partly — big MRR/1-hop win; multi-hop still capped by candidate recall |

**Where it still breaks:** 3+-hop and cross-document questions. Failure analysis shows **22 of 30 strict failures are candidate-recall ceilings** — the gold chunk never reaches the top-30 the reranker scores, so no amount of reranking recovers it. That's a single-vector candidate-generation limit, and the motivation for a future V3 (query decomposition / multi-vector). V3 is **not** implemented here.
