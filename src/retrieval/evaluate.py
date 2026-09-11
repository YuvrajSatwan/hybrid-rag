"""
Shared evaluation utilities for the SIMPLE-RAG retrieval experiments.

Every V2 experiment (BM25, hybrid, hybrid+reranker) reuses THIS module so that
the metric definitions are identical to the frozen V1 baseline:

    Any-Gold@K   : at least one gold chunk appears in Top-K.
    All-Gold@K   : every gold chunk appears in Top-K (strict).
    Coverage@K   : fraction of gold chunks retrieved in Top-K.
    MRR@10       : reciprocal rank of the FIRST gold chunk.

Unanswerable questions (empty gold set) are tracked separately and are NEVER
counted as retrieval successes.

A "retriever" here is just a function:

    rank(query: str, top_k: int) -> list[str]     # returns ranked chunk_ids

This keeps every experiment to one small function plus this shared harness.
"""

import json
import time
from collections import Counter
from pathlib import Path

import numpy as np


# =============================================================================
# PATHS
# =============================================================================

CHUNKS_PATH = Path("data/processed/chunks.jsonl")
EMBEDDINGS_PATH = Path("data/processed/embeddings.jsonl")
QUESTIONS_PATH = Path("data/benchmark/dev_questions.json")
EVAL_DIR = Path("data/benchmark/evaluation")


# =============================================================================
# DATA LOADING
# =============================================================================

def load_chunks(path: Path = CHUNKS_PATH) -> dict[str, dict]:
    """Load chunks into a dict keyed by chunk_id (matches V1 semantics:
    duplicate ids collapse, last write wins on text)."""
    chunks = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunk = json.loads(line)
                chunks[chunk["chunk_id"]] = chunk
    return chunks


def load_questions(path: Path = QUESTIONS_PATH) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# =============================================================================
# CORE METRICS  (identical definitions to V1 search.py)
# =============================================================================

def any_gold_retrieved(retrieved_ids, relevant_ids, k) -> bool:
    if not relevant_ids:
        return False
    return bool(set(relevant_ids) & set(retrieved_ids[:k]))


def all_gold_retrieved(retrieved_ids, relevant_ids, k) -> bool:
    if not relevant_ids:
        return False
    return set(relevant_ids).issubset(set(retrieved_ids[:k]))


def gold_coverage(retrieved_ids, relevant_ids, k) -> float:
    if not relevant_ids:
        return 0.0
    found = len(set(relevant_ids) & set(retrieved_ids[:k]))
    return found / len(relevant_ids)


def reciprocal_rank(retrieved_ids, relevant_ids) -> float:
    """MRR contribution using the FIRST relevant gold chunk."""
    if not relevant_ids:
        return 0.0
    gold = set(relevant_ids)
    for rank, cid in enumerate(retrieved_ids, start=1):
        if cid in gold:
            return 1.0 / rank
    return 0.0


def first_relevant_rank(retrieved_ids, relevant_ids):
    if not relevant_ids:
        return None
    gold = set(relevant_ids)
    for rank, cid in enumerate(retrieved_ids, start=1):
        if cid in gold:
            return rank
    return None


def all_gold_rank(retrieved_ids, relevant_ids):
    """Extra diagnostic (does NOT replace MRR): the rank position at which the
    LAST required gold chunk is retrieved, i.e. the depth needed to cover all
    gold. None if the full set is never covered."""
    if not relevant_ids:
        return None
    gold = set(relevant_ids)
    seen = set()
    for rank, cid in enumerate(retrieved_ids, start=1):
        if cid in gold:
            seen.add(cid)
            if seen == gold:
                return rank
    return None


# =============================================================================
# HELPERS  (hop / service grouping, matching V1)
# =============================================================================

def get_service_from_chunk_id(chunk_id: str) -> str:
    return chunk_id.split("_")[0]


def get_hop_label(relevant_ids) -> str:
    n = len(relevant_ids)
    if n == 0:
        return "unanswerable"
    if n == 1:
        return "1-hop"
    if n == 2:
        return "2-hop"
    return "3+-hop"


def get_service_group(relevant_ids) -> str:
    if not relevant_ids:
        return "unanswerable"
    services = {get_service_from_chunk_id(c) for c in relevant_ids}
    return next(iter(services)) if len(services) == 1 else "cross-service"


def percentile(values, p) -> float:
    if not values:
        return 0.0
    return float(np.percentile(np.array(values), p))


# =============================================================================
# EVALUATION LOOP
# =============================================================================

def evaluate_retriever(rank_fn, questions, top_k=10, label="retriever"):
    """
    Run `rank_fn(query, top_k)` over every benchmark question and compute all
    metrics. `rank_fn` must return a ranked list of chunk_ids.

    Returns (results_list, overall_dict).
    """
    results = []

    for q in questions:
        relevant_ids = q["relevant_chunk_ids"]

        start = time.perf_counter()
        retrieved_ids = rank_fn(q["question"], top_k)
        latency_ms = (time.perf_counter() - start) * 1000

        retrieved_top10 = set(retrieved_ids[:10])
        found = [c for c in relevant_ids if c in retrieved_top10]
        missing = [c for c in relevant_ids if c not in retrieved_top10]

        if not relevant_ids:
            strict_status = "UNANSWERABLE"
        elif all_gold_retrieved(retrieved_ids, relevant_ids, 10):
            strict_status = "PASS"
        else:
            strict_status = "FAIL"

        results.append({
            "id": q["id"],
            "question": q["question"],
            "type": q["type"],
            "hop": get_hop_label(relevant_ids),
            "service": get_service_group(relevant_ids),
            "gold_chunk_ids": relevant_ids,
            "num_gold_chunks": len(relevant_ids),
            "retrieved_top10": retrieved_ids[:10],
            "found_gold_chunks": found,
            "missing_gold_chunks": missing,
            "gold_coverage_at_5": gold_coverage(retrieved_ids, relevant_ids, 5),
            "gold_coverage_at_10": gold_coverage(retrieved_ids, relevant_ids, 10),
            "any_gold_recall_at_5": any_gold_retrieved(retrieved_ids, relevant_ids, 5),
            "any_gold_recall_at_10": any_gold_retrieved(retrieved_ids, relevant_ids, 10),
            "all_gold_at_5": all_gold_retrieved(retrieved_ids, relevant_ids, 5),
            "all_gold_at_10": all_gold_retrieved(retrieved_ids, relevant_ids, 10),
            "strict_status": strict_status,
            "first_relevant_rank": first_relevant_rank(retrieved_ids, relevant_ids),
            "all_gold_rank": all_gold_rank(retrieved_ids, relevant_ids),
            "mrr_at_10": reciprocal_rank(retrieved_ids, relevant_ids),
            "latency_ms": latency_ms,
        })

    overall = aggregate_results(results)
    return results, overall


def aggregate_results(results):
    answerable = [r for r in results if r["gold_chunk_ids"]]
    unanswerable = [r for r in results if not r["gold_chunk_ids"]]
    latencies = [r["latency_ms"] for r in results]

    def mean(field):
        return (sum(r[field] for r in answerable) / len(answerable)) if answerable else 0.0

    return {
        "total_questions": len(results),
        "answerable_questions": len(answerable),
        "unanswerable_questions": len(unanswerable),
        "any_gold_recall_at_5": mean("any_gold_recall_at_5"),
        "any_gold_recall_at_10": mean("any_gold_recall_at_10"),
        "all_gold_at_5": mean("all_gold_at_5"),
        "all_gold_at_10": mean("all_gold_at_10"),
        "average_gold_coverage_at_5": mean("gold_coverage_at_5"),
        "average_gold_coverage_at_10": mean("gold_coverage_at_10"),
        "mrr_at_10": mean("mrr_at_10"),
        "avg_latency_ms": float(np.mean(latencies)) if latencies else 0.0,
        "p50_latency_ms": percentile(latencies, 50),
        "p95_latency_ms": percentile(latencies, 95),
    }


# =============================================================================
# GROUPED (category / hop / service) METRICS
# =============================================================================

def aggregate_group(results, field, value):
    group = [r for r in results if r[field] == value and r["gold_chunk_ids"]]
    if not group:
        return None
    def m(f):
        return 100 * float(np.mean([r[f] for r in group]))
    return {
        "N": len(group),
        "any_at_5": m("any_gold_recall_at_5"),
        "any_at_10": m("any_gold_recall_at_10"),
        "all_at_5": m("all_gold_at_5"),
        "all_at_10": m("all_gold_at_10"),
        "cov_at_5": m("gold_coverage_at_5"),
        "cov_at_10": m("gold_coverage_at_10"),
        "mrr_at_10": float(np.mean([r["mrr_at_10"] for r in group])),
    }


CATEGORY_VALUES = [
    "single_hop", "exact_terminology", "technical_detail", "comparison",
    "reasoning", "two_hop", "multi_hop", "cross_document", "unanswerable",
]
HOP_VALUES = ["1-hop", "2-hop", "3+-hop"]
SERVICE_VALUES = [
    "neutron", "swift", "nova", "keystone", "glance",
    "barbican", "heat", "placement", "cinder", "cross-service",
]


def grouped_tables(results):
    """Return category/hop/service grouped metrics as plain dicts."""
    out = {"by_type": {}, "by_hop": {}, "by_service": {}}
    for v in CATEGORY_VALUES:
        g = aggregate_group(results, "type", v)
        if g:
            out["by_type"][v] = g
    for v in HOP_VALUES:
        g = aggregate_group(results, "hop", v)
        if g:
            out["by_hop"][v] = g
    for v in SERVICE_VALUES:
        g = aggregate_group(results, "service", v)
        if g:
            out["by_service"][v] = g
    return out


# =============================================================================
# CONSOLE REPORTING
# =============================================================================

def print_overall(label, overall):
    print()
    print("#" * 80)
    print(f"OVERALL — {label}")
    print("#" * 80)
    print(f"Questions: {overall['total_questions']}  "
          f"Answerable: {overall['answerable_questions']}  "
          f"Unanswerable: {overall['unanswerable_questions']}")
    print()
    print(f"Any-Gold@5 : {100*overall['any_gold_recall_at_5']:6.2f}%   "
          f"Any-Gold@10 : {100*overall['any_gold_recall_at_10']:6.2f}%")
    print(f"All-Gold@5 : {100*overall['all_gold_at_5']:6.2f}%   "
          f"All-Gold@10 : {100*overall['all_gold_at_10']:6.2f}%")
    print(f"Coverage@5 : {100*overall['average_gold_coverage_at_5']:6.2f}%   "
          f"Coverage@10 : {100*overall['average_gold_coverage_at_10']:6.2f}%")
    print(f"MRR@10     : {overall['mrr_at_10']:.4f}")
    print(f"Latency    : avg {overall['avg_latency_ms']:.2f} ms  "
          f"p50 {overall['p50_latency_ms']:.2f} ms  "
          f"p95 {overall['p95_latency_ms']:.2f} ms")


def print_group_table(results, field, values, title):
    print()
    print("=" * 96)
    print(title)
    print("=" * 96)
    print(f"{'Group':<20}{'N':>4}{'Any@5':>9}{'Any@10':>9}"
          f"{'All@5':>9}{'All@10':>9}{'Cov@5':>9}{'Cov@10':>9}{'MRR@10':>9}")
    print("-" * 96)
    for v in values:
        g = aggregate_group(results, field, v)
        if not g:
            continue
        print(f"{v:<20}{g['N']:>4}{g['any_at_5']:>8.1f}%{g['any_at_10']:>8.1f}%"
              f"{g['all_at_5']:>8.1f}%{g['all_at_10']:>8.1f}%"
              f"{g['cov_at_5']:>8.1f}%{g['cov_at_10']:>8.1f}%{g['mrr_at_10']:>9.4f}")


def print_failures(results, limit=None):
    failures = [r for r in results if r["strict_status"] == "FAIL"]
    print()
    print("=" * 96)
    print(f"STRICT FAILURES ({len(failures)})")
    print("=" * 96)
    shown = failures if limit is None else failures[:limit]
    for r in shown:
        print(f"\n{r['id']} [{r['type']}] [{r['hop']}] [{r['service']}]  "
              f"cov@10={r['gold_coverage_at_10']:.0%}")
        print(f"  Q: {r['question']}")
        print(f"  gold({r['num_gold_chunks']}): {r['gold_chunk_ids']}")
        print(f"  found:   {r['found_gold_chunks']}")
        print(f"  missing: {r['missing_gold_chunks']}")


def print_unanswerable(results):
    unans = [r for r in results if r["strict_status"] == "UNANSWERABLE"]
    print()
    print("=" * 96)
    print(f"UNANSWERABLE ({len(unans)})  — no gold; retriever always returns nearest chunks (no abstention in V2)")
    print("=" * 96)
    for r in unans:
        print(f"  {r['id']}: {r['question']}")
        print(f"     top-3: {r['retrieved_top10'][:3]}")


# =============================================================================
# SAVE
# =============================================================================

def save_evaluation(out_path, config, overall, results):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "configuration": config,
        "overall": overall,
        "grouped": grouped_tables(results),
        "results": results,
    }
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"\nSaved evaluation -> {out_path}")
