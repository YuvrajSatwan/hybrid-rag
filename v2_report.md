# V2 Retrieval Evaluation Report

Incremental retrieval experiments on the SIMPLE-RAG OpenStack-docs corpus. Same corpus (1,495 unique chunks), same 100-question benchmark, same gold IDs, same Top-K, same metric definitions as the frozen V1 baseline. No benchmark or embedding-model changes.

---

## 1. Final V2 architecture

```
query
  │
  ├─► Dense retriever (Jina jina-embeddings-v3, cosine)   ── top-100 ─┐
  │                                                                    │
  └─► BM25 retriever (Okapi, k1=1.5 b=0.75)               ── top-100 ─┤
                                                                       ▼
                                              Reciprocal Rank Fusion (k=60)
                                                                       │
                                                            top-30 candidates
                                                                       ▼
                                    Cross-encoder reranker (ms-marco-MiniLM-L-6-v2)
                                          scores each (query, chunk) pair
                                                                       ▼
                                                              re-sorted Top-10
```

Two stages: **cheap high-recall candidate generation** (hybrid dense+BM25 → RRF) feeding **expensive high-precision reranking** (cross-encoder over 30 candidates).

## 2. Main comparison table

100 questions (95 answerable, 5 unanswerable). Metrics averaged over answerable questions.

| Stage | Any@5 | Any@10 | All@5 | All@10 | Cov@5 | Cov@10 | MRR@10 | p95 latency |
|-------|------:|-------:|------:|-------:|------:|-------:|-------:|------------:|
| V1 Dense | 73.7% | 77.9% | 56.8% | 61.1% | 65.3% | 69.8% | 0.5330 | 766 ms |
| V2-A BM25 | 68.4% | 76.8% | 51.6% | 57.9% | 59.3% | 67.4% | 0.5170 | 29 ms |
| V2-B Hybrid | 77.9% | 84.2% | 57.9% | 63.2% | 68.1% | 74.4% | 0.5589 | 31 ms |
| **V2-C Hybrid+Rerank** | **78.9%** | **87.4%** | **58.9%** | **68.4%** | **68.9%** | **78.9%** | **0.6651** | 3542 ms |

**Latency fairness note:** V1's 766ms includes the live Jina query-embedding API call. V2-B/C reuse a query-embedding cache, so their hybrid stage runs local-only (~30ms). V2-C's 3.5s is the CPU cross-encoder scoring 30 pairs/query. The comparison of *quality* is apples-to-apples; the latency column mixes cached vs live embedding and CPU reranking — read it as an ordering of computational cost, not a production SLA.

### All-Gold@10 by hop count

| Hop | Dense | BM25 | Hybrid | Rerank |
|-----|------:|-----:|-------:|-------:|
| 1-hop | 78.3% | 78.3% | 83.3% | **90.0%** |
| 2-hop | 36.0% | 28.0% | 36.0% | **40.0%** |
| 3+-hop | **20.0%** | 10.0% | 10.0% | 10.0% |

### MRR@10 by hop count

| Hop | Dense | BM25 | Hybrid | Rerank |
|-----|------:|-----:|-------:|-------:|
| 1-hop | 0.5109 | 0.5327 | 0.5501 | **0.6738** |
| 2-hop | 0.5613 | 0.4847 | 0.5643 | **0.6570** |
| 3+-hop | 0.5950 | 0.5033 | 0.5976 | **0.6333** |

### All-Gold@10 by question type

| Type | Dense | BM25 | Hybrid | Rerank |
|------|------:|-----:|-------:|-------:|
| single_hop | 90% | 85% | 90% | **95%** |
| exact_terminology | **90%** | 60% | 80% | 80% |
| technical_detail | **80%** | 60% | 70% | **80%** |
| comparison | 60% | 80% | 90% | **100%** |
| reasoning | 60% | **100%** | 80% | 90% |
| two_hop | 46.7% | 33.3% | 40.0% | **46.7%** |
| multi_hop | **20%** | 10% | 10% | 10% |
| cross_document | 20% | 20% | **30%** | **30%** |

## 3. What each stage contributed

- **BM25 (V2-A)** — worse alone than dense overall, but wins a disjoint set of queries. On the answerable set: 47 questions pass All@10 in both, **11 dense-only, 8 BM25-only**, 29 in neither. That 8-query disjoint win is the headroom hybrid exploits. BM25 dominates `reasoning` (100%) and `comparison` (80%) here because those questions happen to share surface vocabulary with their gold chunks.
- **Hybrid RRF (V2-B)** — realized the complementarity: beats *both* parents on every headline metric. Biggest lift on Any@10 (+6.3 pts over dense) and Coverage@10 (+4.6). `comparison` jumped to 90%, `cross_document` 20%→30%.
- **Cross-encoder rerank (V2-C)** — the biggest single quality jump. **MRR +0.11**, All@10 +5.2, Coverage@10 +4.5. Cross-attention re-scores the fused top-30 and pulls the correct chunk sharply upward — visible as the MRR jump across *every* hop bucket.

## 4. Biggest improvements (V1 → V2-C)

- **MRR@10: 0.533 → 0.665 (+0.13, +25%)** — the first relevant chunk now lands much higher. The single most improved metric.
- **All-Gold@10: 61.1% → 68.4% (+7.3 pts)** — strict multi-chunk success.
- **Coverage@10: 69.8% → 78.9% (+9.1 pts)**.
- **Any-Gold@10: 77.9% → 87.4% (+9.5 pts)**.
- **1-hop All@10: 78.3% → 90.0%**, and 1-hop MRR 0.51 → 0.67 — reranking is decisive when there's exactly one right answer to float to the top.

## 5. Remaining weaknesses (failure analysis)

Classified all 30 strict failures of V2-C by whether the reranker *could* have fixed them (was the missing gold in the top-30 it scored?):

- **22 / 30 are candidate-recall ceilings** — the missing gold chunk sits *outside* the reranked top-30 (ranks 31-96 in the fused pool), or **9 missing golds aren't in the top-100 fused pool at all**. The reranker never saw them; this is a candidate-generation limit, not a reranking limit.
- **8 / 30 are true ranking losses** — all missing gold was inside the top-30, but the reranker still didn't float the full set into the Top-10. These are the only failures a better reranker could fix.

By failure category:

- **Incomplete multi-hop coverage** (dominant): 3+-hop All@10 stuck at 10%. A single query vector points at one semantic region, so for a 3-chunk question it reliably surfaces 1-2 hops and buries the rest. e.g. q084 (Swift sharding + policies + zones) recovers 1 of 3.
- **Cross-document coverage failure:** q090 (Nova↔Keystone), q086/091/095 — the second service's generic overview chunk (`keystone_overview_0001`, `swift_overview_0001`) never enters the pool. Neither dense nor BM25 ranks a generic overview highly against a specific question.
- **Exact-lexical regression vs dense:** `exact_terminology` slipped 90%→80% (q021, q023). Fusion sometimes dilutes a chunk that dense ranked #1 alone. A known RRF side effect — it rewards agreement, so a single-retriever star can drop.
- **Ranking failure (the 8):** gold in candidates but not floated to Top-10 — the reranker's residual error.

**Net:** V2 fixed most 1-hop and comparison failures. Multi-hop and cross-document remain the wall, and the failure analysis proves it's a *candidate-generation* wall (single-vector recall), not something more reranking can solve. That's the motivation for V3 (query decomposition / multi-vector) — deliberately not built here.

## 6. Key engineering decisions

Full detail in [`docs/V2_DECISIONS.md`](docs/V2_DECISIONS.md). Summary:

1. Added BM25 to attack V1's exact-token misses (complement, not replacement).
2. Fused with **RRF, not score addition** — avoids the dense∈[0,1] vs unbounded-BM25 scale problem.
3. Took **k=60 / fuse_depth=100 from the literature**, didn't tune on the benchmark (no test-set leakage).
4. **Cross-encoder over candidates only** — full cross-attention precision without scoring the whole corpus.
5. **rerank_depth=30** — bounded latency; failure analysis shows the ceiling is now recall, not depth.
6. **Reused frozen V1 embeddings**, embedded only queries live (cached); verified dense reproduces V1 top-10 exactly (5/5).
7. **One shared eval harness** — identical metrics/benchmark across all stages; added `all_gold_rank` diagnostic without replacing MRR.

## 7. Interview questions (with short answers)

1. **Why did BM25 alone score worse than dense but still help?** — It wins a *disjoint* 8 queries dense misses (exact tokens). Hybrid captures the union.
2. **Why RRF instead of summing scores?** — Dense cosine ∈ [0,1], BM25 unbounded and corpus-dependent; adding raw scores lets BM25 dominate. RRF uses only rank, so scale is irrelevant.
3. **What does k=60 do in RRF?** — Dampens top-rank dominance (rank 1→1/61, rank 2→1/62). A doc must rank well in both systems to rise.
4. **Bi-encoder vs cross-encoder — why not just use the cross-encoder for everything?** — Cross-encoder can't precompute doc vectors; it must see query+doc together. Scoring the full 1,495-chunk corpus per query is infeasible, so it only reranks candidates.
5. **Why does the reranker help MRR so much more than All-Gold?** — MRR rewards floating the *first* gold chunk up (cross-attention is great at this). All-Gold needs *every* gold chunk present, which is capped by candidate recall.
6. **Your reranker only lifted 3+-hop from 10% to 10% — why?** — 22/30 failures are recall ceilings: gold isn't in the top-30 the reranker scores. You can't rerank what you didn't retrieve.
7. **How would you fix multi-hop without an LLM?** — Deepen rerank_depth (helps ~14 cases, costs latency) or add query decomposition / multi-vector retrieval so each hop gets its own query vector. That's V3.
8. **Why not tune k1, b, k, or fuse_depth on your benchmark?** — Test-set leakage. Tuning on the 100 dev questions inflates numbers that won't generalize. Literature defaults keep the comparison honest.
9. **How do you handle unanswerable questions?** — Tracked separately, never counted as successes. V2 has no abstention, so it returns nearest chunks; we report but don't score them. Abstention is future work.
10. **Why is All-Gold@K stricter and more important than Any-Gold@K here?** — Multi-hop questions need several chunks. Any@K = 100% with All@K = 0% means you found one hop and missed the rest — Any@K alone hides every multi-hop failure.
11. **Is the latency comparison fair?** — Not directly: V1 includes a live embedding API call, hybrid uses a query cache, and V2-C adds CPU cross-encoding. Read the column as compute-cost ordering, not a production SLA.
12. **What's the single biggest win of V2?** — MRR@10 +25% (0.53→0.67). The right chunk now surfaces near the top far more often.
13. **Why MiniLM-L-6 and not BGE-reranker-large?** — Small (~80MB), CPU-friendly, the standard English MS MARCO reranker. Bigger models chase a leaderboard; this is a learning project where I need to explain every part.
14. **What breaks if a gold chunk is a duplicate ID?** — The corpus has 7 duplicate IDs; dense dedupes last-write-wins to match V1's dict-keyed loader (1,495 unique), so index positions stay aligned. Verified against V1.
15. **What would you measure next?** — Recall@30/@50 of candidate generation directly (the real ceiling), and rerank_depth vs latency curves, before touching the model.

## 8. Reproduction

Run from the repo root, in order:

```bash
python -m src.retrieval.bm25       # V2-A  -> bm25_v2a_evaluation.json
python -m src.retrieval.hybrid     # V2-B  -> hybrid_v2b_evaluation.json
python -m src.retrieval.reranker   # V2-C  -> hybrid_reranker_v2c_evaluation.json
```

The V1 baseline (`dense_v1_evaluation.json`) is frozen and not regenerated. Dense query embeddings are cached in `data/processed/query_embeddings_cache.json` (needs `JINA_API_KEY` in `.env` only for uncached queries). Requires `rank_bm25`, `sentence-transformers`, `numpy`, `requests`, `python-dotenv`.

All four evaluation JSONs are in `data/benchmark/evaluation/`. Concept explanations: [`docs/V2_INTERVIEW_NOTES.md`](docs/V2_INTERVIEW_NOTES.md).

## 9. V3 confirmation

**V3 was not implemented.** No query rewriting, HyDE, LLM judge, GraphRAG, multi-vector retrieval, generation/answer-synthesis, or production API layer was added. V2 stops at retrieval + reranking evaluation, exactly as scoped. The failure analysis in §5 identifies candidate-generation recall as the next bottleneck — that motivates V3 but is left unbuilt.
