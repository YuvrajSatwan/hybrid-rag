# V2 Interview Notes

Concise explanations of the concepts behind V2. Written so I can talk through each one without notes.

---

## BM25 (lexical retrieval)

Ranks documents by exact term overlap with the query. For each query term in a document:

```
score += IDF(t) * ( f(t,d) * (k1 + 1) ) / ( f(t,d) + k1 * (1 - b + b * |d|/avgdl) )
```

- **f(t,d)** — term frequency: how often the term appears in the doc.
- **IDF(t)** — rare terms across the corpus count for more than common ones.
- **k1 (1.5)** — TF saturation: the 5th occurrence of a word adds less than the 2nd (diminishing returns).
- **b (0.75)** — length normalization: without it, long docs win just by containing more words.

**Why it complements dense:** BM25 matches surface tokens, so `ec_num_parity_fragments` or a CLI flag scores exactly. It has no idea two paraphrases mean the same thing — that's dense's job.

## Bi-encoder vs cross-encoder

- **Bi-encoder** (our Jina dense retriever): encodes the query and each document into vectors *separately*, compares with cosine. Documents are pre-encoded once, so search is fast — but the query and document never see each other. Matching is coarse.
- **Cross-encoder** (our reranker): feeds `query [SEP] document` through the model *together* and outputs a single relevance score. Full cross-attention between query and document tokens = far more accurate. But nothing can be precomputed, so you can only afford to run it on a small candidate set.

That asymmetry is the entire architecture: bi-encoder for cheap recall over the whole corpus, cross-encoder for expensive precision over ~30 candidates.

## Reciprocal Rank Fusion (RRF)

Combines ranked lists using only *rank*, never raw scores:

```
RRF(d) = Σ_retrievers  1 / (k + rank_retriever(d))
```

- A document gets a contribution from each retriever that ranked it; retrievers that didn't return it contribute nothing.
- **k=60** dampens how much the very top ranks dominate: rank 1 → 1/61, rank 2 → 1/62, nearly equal. So a doc must rank well in *both* systems (or extremely high in one) to rise.
- **Why not add scores:** dense cosine ∈ [0,1], BM25 is unbounded — different scales. RRF sidesteps scale entirely by using position.

## The two-stage retrieve-then-rerank pattern

1. **Candidate generation** (cheap, high recall): hybrid dense+BM25 → top-30. Goal: get every gold chunk *somewhere* in the 30.
2. **Reranking** (expensive, high precision): cross-encoder rescore the 30 → Top-10. Goal: put the right ones at the top.

The reranker can only ever be as good as the candidate set. If gold isn't in the top-30, no reranker can recover it. This is why our failure analysis splits failures into "candidate-recall ceiling" vs "ranking loss."

## The metrics

- **Any-Gold@K** — did *at least one* gold chunk land in the Top-K? (Did we surface *something* relevant.)
- **All-Gold@K** — did *every* gold chunk land in the Top-K? (Strict; the real bar for multi-hop questions that need several chunks.)
- **Coverage@K** — fraction of gold chunks retrieved. (Partial credit between Any and All.)
- **MRR@10** — 1/rank of the *first* gold chunk, averaged. Measures *ranking quality*, not just presence.

**Why Any vs All matters:** a single-chunk question passes All@K as easily as Any@K. A 3-chunk multi-hop question can score Any@K = 100% while All@K = 0% — you found one hop, missed the rest. Reporting only Any@K would hide every multi-hop failure. That gap was the headline finding of V1 and the reason multi-hop is still the hard case in V2.

- **Unanswerable questions** (5, no gold) are tracked separately and never counted as retrieval successes. V2 has no abstention, so the retriever always returns its nearest chunks for them — we report what it returned but score nothing.

## Why multi-hop / cross-document stays hard

A cross-document question ("how do Keystone roles control access to Swift containers?") needs one chunk from Keystone *and* one from Swift. A single query vector points at one semantic region — it surfaces the Swift-auth chunk strongly and the generic Keystone-overview chunk barely, or not at all. Neither dense nor BM25 puts the second hop in the candidate pool, so the reranker never sees it. Fixing this properly needs query decomposition or multi-vector retrieval — deliberately out of scope for V2 (that's V3).
