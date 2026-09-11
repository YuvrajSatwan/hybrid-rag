# V2 Engineering Decisions

Interview-oriented log. Each decision: what I chose, why, the alternative I rejected, the tradeoff, and the measured result.

---

### 1. Add BM25 as a second retriever (V2-A)

- **Decision:** Add Okapi BM25 lexical retrieval (`rank_bm25`, k1=1.5, b=0.75) alongside the V1 dense retriever.
- **Why:** V1's dense misses were concentrated in `exact_terminology` and `technical_detail` — rare tokens like `ec_num_parity_fragments`, `nova-manage`, port numbers. Dense embeddings smooth rare tokens into a semantic average; BM25 scores exact token overlap.
- **Alternative:** Tune the dense model / swap embeddings. Rejected — the spec froze the embedding model, and swapping wouldn't fix lexical exactness.
- **Tradeoff:** BM25 alone is *worse* overall than dense (All@10 57.9% vs 61.1%) and collapses on paraphrased questions. It's a complement, not a replacement.
- **Result:** Standalone BM25 underperforms dense but wins a disjoint set of queries (8 BM25-only passes vs 11 dense-only) — that disjointness is the whole reason hybrid works.

### 2. Fuse dense + BM25 with Reciprocal Rank Fusion, not score addition (V2-B)

- **Decision:** Combine the two retrievers with RRF (k=60), fusing each retriever's top-100.
- **Why:** Dense cosine ∈ [0,1]; BM25 is unbounded and corpus-dependent (5, 20, 40+). Adding raw scores lets BM25 silently dominate; min-max normalization is fragile to outliers. RRF uses only *rank*, so scale is irrelevant.
- **Alternative:** Weighted score sum with normalization. Rejected as fragile and requiring a tuned weight (which would leak the benchmark).
- **Tradeoff:** RRF throws away score *magnitude* — a document ranked #1 with a huge margin is treated the same as a narrow #1. We accept that; the reranker recovers magnitude later.
- **Result:** Hybrid beats both parents on every headline metric: All@10 61%→63%, Coverage@10 70%→74%, MRR 0.53→0.56. Confirmed the complementarity hypothesis.

### 3. k=60 and fuse_depth=100 taken from the literature, not tuned

- **Decision:** Use the original RRF paper's k=60 (Cormack et al., 2009) and fuse the top-100 of each retriever.
- **Why:** Tuning these against our own 100-question benchmark would leak the test set and inflate results — exactly what the spec forbids.
- **Alternative:** Grid-search k and depth on the dev set. Rejected — that's benchmark overfitting dressed up as engineering.
- **Tradeoff:** We're likely leaving a point or two on the table vs a tuned k. Honest generalization is worth more here.
- **Result:** Literature defaults already delivered the hybrid gain; no tuning needed to prove the thesis.

### 4. Cross-encoder reranker over the candidate set only (V2-C)

- **Decision:** Rerank the top-30 fused candidates with `cross-encoder/ms-marco-MiniLM-L-6-v2`, re-sorting to Top-K.
- **Why:** A bi-encoder (dense) never lets query and doc tokens interact. A cross-encoder feeds `query [SEP] doc` through the model together (full cross-attention) — far more accurate at judging relevance. It can't be precomputed, so it runs only on candidates, never the 1,495-chunk corpus.
- **Alternative:** Larger reranker (BGE-reranker-large, monoT5). Rejected — bigger and slower for a CPU learning project; MiniLM-L-6 is the standard small English reranker (~80MB).
- **Tradeoff:** Latency. p95 jumps to ~3.5s on CPU (30 cross-encoder pairs/query) vs ~30ms for hybrid. Quality-vs-latency is the classic reranker tradeoff.
- **Result:** Best stage on every metric: All@10 63%→68%, Coverage@10 74%→79%, **MRR 0.56→0.67**. The MRR jump is the story — cross-attention pulls the first gold chunk sharply higher.

### 5. rerank_depth = 30

- **Decision:** Rerank the top-30 candidates.
- **Why:** Deep enough to rescue a gold chunk fusion ranked at ~20-30; shallow enough that per-query cost stays bounded (30 pairs).
- **Alternative:** Depth 50-100. Would rescue ~14 more missing golds (they sit at ranks 31-96 in the fused pool) but multiplies latency.
- **Tradeoff:** We cap recoverable recall to what fusion puts in the top-30. Failure analysis shows this is the current ceiling, not the reranker.
- **Result:** 22 of 30 strict failures have gold *outside* the top-30 — deepening would help, but the bigger wall is candidate generation (see V2 report).

### 6. Reuse frozen V1 embeddings; call Jina directly for queries

- **Decision:** Load the 1,495 precomputed V1 chunk vectors from disk; embed only the *query* live, via a direct `requests` call to the Jina API, cached to disk.
- **Why:** The spec froze the embedding model and the V1 baseline. Re-embedding the corpus would risk drift and cost. The old `langchain_community` wrapper was uninstalled, so I called the API directly.
- **Alternative:** Reinstall langchain and re-embed. Rejected — unnecessary and risks changing the baseline.
- **Tradeoff:** Query cache means latency numbers exclude the live embedding call. I document this explicitly so hybrid's 30ms isn't misread against V1's 766ms.
- **Result:** Verified the reused-embedding dense retriever reproduces V1's top-10 exactly (5/5 identical) — the baseline is preserved.

### 7. Keep every stage on the identical benchmark and metrics

- **Decision:** One shared `evaluate.py` harness; same 100 questions, gold IDs, Top-K, and metric definitions (Any/All-Gold@K, Coverage@K, MRR@10) for V1→V2-C. Unanswerable questions tracked separately, never counted as successes.
- **Why:** Any metric or benchmark change between stages makes the comparison meaningless.
- **Alternative:** Per-stage bespoke metrics. Rejected.
- **Result:** The four-way comparison table is apples-to-apples. Added one diagnostic (`all_gold_rank`) without replacing MRR, per spec.
