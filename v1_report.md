# SIMPLE-RAG — V1 Dense Retrieval Evaluation Report

**Version:** V1
**Corpus:** OpenStack Documentation
**Benchmark:** 100 questions
**Answerable:** 95
**Unanswerable:** 5
**Retrieval:** Jina `jina-embeddings-v3` dense embeddings
**Evaluation:** Top-5 and Top-10 retrieval
**Purpose:** Establish a reproducible baseline before introducing BM25/hybrid retrieval.

---

## 1. Executive Summary

V1 dense retrieval provides a solid baseline, achieving:

| Metric             |         V1 |
| ------------------ | ---------: |
| Any-Gold Recall@5  | **73.68%** |
| Any-Gold Recall@10 | **77.89%** |
| **All-Gold@5**     | **56.84%** |
| **All-Gold@10**    | **61.05%** |
| Gold Coverage@5    | **65.26%** |
| Gold Coverage@10   | **69.82%** |
| MRR@10             | **0.5330** |
| Average latency    | **584 ms** |
| P50 latency        | **543 ms** |
| P95 latency        | **766 ms** |



### Main conclusion

> **Dense retrieval is effective at locating semantically relevant regions of the OpenStack corpus, but struggles to retrieve precise evidence and, more importantly, complete evidence sets required by multi-hop and cross-document questions.**

Therefore, V1 is **good enough to freeze and move to V2**.

---

# 2. Why We Track Two Recall Metrics

This is important for the project.

### Any-Gold Recall

A question is successful if **at least one** gold chunk appears in Top-K.

This measures:

> "Can the retriever find relevant evidence?"

### All-Gold Recall

A question is successful only when **every required gold chunk** appears in Top-K.

This measures:

> "Can the retriever retrieve the complete evidence required to answer the question?"

For V1:

**Any-Gold@10 = 77.89%**

but

**All-Gold@10 = 61.05%**



That ~17 percentage-point gap is extremely useful. It tells us that finding *some* relevant information isn't the main challenge; **complete evidence retrieval is.**

---

# 3. Category Results

| Category          |  N | Any@10 |    All@10 | Coverage@10 |  MRR |
| ----------------- | -: | -----: | --------: | ----------: | ---: |
| Single-hop        | 20 |    90% |   **90%** |         90% | .566 |
| Exact terminology | 10 |    90% |   **90%** |         90% | .567 |
| Technical detail  | 10 |    80% |   **80%** |         80% | .421 |
| Comparison        | 10 |    60% |   **60%** |         60% | .513 |
| Reasoning         | 10 |    60% |   **60%** |         60% | .433 |
| Two-hop           | 15 |    80% | **46.7%** |       63.3% | .700 |
| Multi-hop         | 10 |    80% |   **20%** |       53.3% | .595 |
| Cross-document    | 10 |    70% |   **20%** |         45% | .353 |



### Interpretation

The first five categories are mostly single-evidence tasks, so Any-Gold and All-Gold are identical.

But once multiple chunks are required:

```text
Single-hop       All@10 = 90%
Two-hop          All@10 = 46.7%
Multi-hop        All@10 = 20%
Cross-document   All@10 = 20%
```

This is probably the **single most important V1 finding**.

---

# 4. Hop-wise Performance

| Evidence required | Any@10 |    All@10 | Coverage@10 |
| ----------------- | -----: | --------: | ----------: |
| 1-hop             |  78.3% | **78.3%** |       78.3% |
| 2-hop             |  76.0% | **36.0%** |       56.0% |
| 3+ hop            |  80.0% | **20.0%** |       53.3% |



This shows that the old interpretation of "80% multi-hop recall" would have been misleading.

For example, q077 retrieved **2/3** required chunks:

> Coverage = 66.67%, but strict result = FAIL.



That's exactly why All-Gold is now the important metric.

---

# 5. Service-wise Results

| Service       | Any@10 |    All@10 | Coverage@10 |   MRR |
| ------------- | -----: | --------: | ----------: | ----: |
| Neutron       |  78.6% | **71.4%** |       76.2% |  .519 |
| Swift         |  76.7% | **60.0%** |       68.3% |  .544 |
| Nova          |  58.8% | **47.1%** |       52.0% |  .247 |
| Keystone      |   100% | **81.8%** |       92.4% |  .788 |
| Glance        |   100% |  **100%** |        100% |  .667 |
| Heat          |    80% |   **60%** |       73.3% |  .667 |
| Placement     |   100% |  **100%** |        100% | 1.000 |
| Cinder        |   100% |  **100%** |        100% | 1.000 |
| Cross-service |    70% |   **20%** |         45% |  .353 |



### Biggest concern

**Nova** is the weakest major service:

**All-Gold@10 = 47.1%**

and

**MRR = 0.2466**.



This is likely related to the large number of highly similar Nova architecture/install/cells/scheduling chunks.

---

# 6. Failure Analysis

There are **37 strict failures**. 

They reveal three major failure modes.

### A. Semantic neighborhood but wrong exact chunk

Example q032:

The query asks specifically about:

`ec_num_data_fragments`

and

`ec_num_parity_fragments`

Dense retrieval returns many Swift erasure-code chunks, but misses the exact gold chunk. 

This suggests:

**semantic similarity ≠ precise lexical retrieval.**

---

### B. Multiple required chunks, but only some retrieved

Example q061:

```text
Required: 2
Retrieved: 1
Coverage: 50%
Strict: FAIL
```



Example q077:

```text
Required: 3
Retrieved: 2
Coverage: 66.67%
Strict: FAIL
```



This becomes increasingly severe with more hops.

---

### C. Cross-service evidence isn't covered

Example q087:

```text
Nova evidence       ✅
Glance evidence     ❌
Coverage             50%
```



Example q090:

```text
Nova evidence       ❌
Keystone evidence   ❌
Coverage             0%
```



This strongly suggests dense retrieval has difficulty **covering independent semantic regions of the corpus with one query**.

---

# 7. Unanswerable Behavior

The five unanswerable questions correctly have no gold evidence, but dense retrieval still returns Top-10 chunks.

For example, the Kubernetes question retrieves Neutron, Heat, Swift and Nova material despite Kubernetes not being an answerable topic in the benchmark. 

This is expected behavior for a pure Top-K dense retriever:

> It always returns the nearest available chunks.

### V1 decision

**Do not add abstention yet.**

We record this as a future weakness rather than introducing another variable before V2.

---

# 8. V1 Failure Diagnosis

So our diagnosis is:

| Problem                     | Evidence                               | Importance  |
| --------------------------- | -------------------------------------- | ----------- |
| Semantic retrieval          | Any@10 = 77.9%                         | 🟢 Good     |
| Precise ranking             | Many related chunks outrank exact gold | 🔴 Major    |
| Exact terminology           | 90% All@10                             | 🟢 Strong   |
| Multi-hop evidence coverage | 20% All@10                             | 🔴 Critical |
| Cross-document retrieval    | 20% All@10                             | 🔴 Critical |
| Nova retrieval              | 47.1% All@10                           | 🔴 Major    |
| Latency                     | P95 766 ms                             | 🟡 Monitor  |
| Unanswerable detection      | No abstention                          | 🟡 Future   |

---

# 9. What V2 Is Supposed to Test

This is where we freeze V1.

**Do not change:**

* corpus
* chunks
* benchmark
* gold IDs
* evaluation definitions
* embedding model

V2 introduces retrieval improvements one at a time.

### V2 Experiment Matrix

| System                     | Purpose                              |
| -------------------------- | ------------------------------------ |
| **V1 Dense**               | Baseline                             |
| **V2-A BM25**              | Test lexical retrieval independently |
| **V2-B Dense + BM25**      | Test complementary retrieval         |
| **V2-C Hybrid + Reranker** | Test precision improvement           |

The key question isn't:

> "Does V2 have a higher score?"

It's:

> **"Which failure modes does each retrieval strategy fix?"**

---

# 10. V1 → V2 Comparison Sheet

This is the table I'd keep permanently in your project.

```text
SIMPLE-RAG RETRIEVAL EXPERIMENTS

                         V1 Dense    V2 BM25    V2 Hybrid    V2 Reranker
---------------------------------------------------------------------------
Any-Gold@5                 73.68%       ?           ?             ?
Any-Gold@10                77.89%       ?           ?             ?

All-Gold@5                 56.84%       ?           ?             ?
All-Gold@10                61.05%       ?           ?             ?

Coverage@5                 65.26%       ?           ?             ?
Coverage@10                69.82%       ?           ?             ?

MRR@10                      0.533       ?           ?             ?

1-hop All@10               78.3%        ?           ?             ?
2-hop All@10               36.0%        ?           ?             ?
3+ hop All@10              20.0%        ?           ?             ?
Cross-doc All@10           20.0%        ?           ?             ?

Avg latency                584 ms       ?           ?             ?
P50                         543 ms       ?           ?             ?
P95                         766 ms       ?           ?             ?
```

The **bold metrics to watch** are:

### 🥇 All-Gold@10

Primary overall metric.

### 🥈 Coverage@10

Shows whether we're retrieving *more of the required evidence*, even when strict success isn't achieved.

### 🥉 Multi-hop All@10

Shows whether the system is actually becoming better at complete evidence retrieval.

### 🥉 Cross-document All@10

Shows whether we're getting better at combining evidence across services/documents.

---

# 11. What Would Count as a Successful V2?

Don't hard-code a required improvement before running the experiment.

But as a practical benchmark:

### Weak improvement

`61% → 63–66% All-Gold@10`

Small gain; investigate whether the added complexity is justified.

### Good improvement

`61% → 68–72%`

Clearly meaningful.

### Very good

`61% → 73–78%`

Strong evidence that V2 architecture addresses V1's weaknesses.

### Excellent

`61% → 80%+`

Excellent result — but we'd then need to verify that it isn't caused by some evaluation artifact or benchmark-specific behavior.

And **multi-hop/cross-document improvement matters more than simply pushing overall Recall@10 upward.**

---

# 12. Final V1 Decision

### ✅ V1 is complete.

I would record the project decision as:

> **V1 Dense Retrieval Baseline Accepted.**
>
> Dense retrieval achieves 77.89% Any-Gold@10 but only 61.05% All-Gold@10, with particularly poor complete-evidence retrieval for 3+ hop and cross-document questions (20% All-Gold@10 in both cases). Failure analysis shows frequent retrieval of semantically related but non-gold chunks and incomplete coverage of required evidence. These results justify investigating lexical retrieval and hybrid retrieval in V2.

That's the point where you should **stop touching V1**.

### Next: V2-A = BM25

Build **plain BM25 first**, evaluate it against this exact report, and **don't combine it with dense retrieval yet**.

That experiment will tell us whether lexical retrieval actually fixes the specific weaknesses we've identified. Then we'll have evidence for the hybrid step rather than assuming hybrid is better. 🔬
