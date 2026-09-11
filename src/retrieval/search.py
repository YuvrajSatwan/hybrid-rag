import json
import time
from pathlib import Path

import numpy as np
from langchain_community.embeddings import JinaEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()


# =============================================================================
# CONFIGURATION
# =============================================================================

CHUNKS_PATH = Path("data/processed/chunks.jsonl")
EMBEDDINGS_PATH = Path("data/processed/embeddings.jsonl")
QUESTIONS_PATH = Path("data/benchmark/dev_questions.json")

OUTPUT_PATH = Path(
    "data/benchmark/evaluation/dense_v1_evaluation.json"
)

TOP_K_VALUES = [5, 10]


# =============================================================================
# EMBEDDING MODEL
# =============================================================================

embeddings = JinaEmbeddings(
    jina_api_key=os.environ["JINA_API_KEY"],
    model_name="jina-embeddings-v3",
)


# =============================================================================
# LOAD DATA
# =============================================================================

def load_chunks(path: Path) -> dict[str, dict]:
    """
    Load chunks into a dictionary keyed by chunk_id.
    """
    chunks = {}

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunk = json.loads(line)
                chunks[chunk["chunk_id"]] = chunk

    return chunks


def load_embeddings(path: Path) -> list[dict]:
    """
    Load embedding records.
    """
    records = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    return records


def load_questions(path: Path) -> list[dict]:
    """
    Load benchmark questions.
    """
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# =============================================================================
# VECTOR OPERATIONS
# =============================================================================

def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors.
    """
    a = np.array(vector_a)
    b = np.array(vector_b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


# =============================================================================
# RETRIEVAL
# =============================================================================

def search(
    query: str,
    chunks: dict[str, dict],
    embedding_records: list[dict],
    top_k: int = 10,
):
    """
    Dense retrieval using brute-force cosine similarity.

    Returns the top_k highest-scoring chunks.
    """

    query_vector = embeddings.embed_query(query)

    results = []

    for record in embedding_records:

        chunk_id = record["chunk_id"]

        # Skip embedding records whose chunk is not available.
        if chunk_id not in chunks:
            continue

        score = cosine_similarity(
            query_vector,
            record["embedding"],
        )

        results.append(
            {
                "chunk_id": chunk_id,
                "score": score,
                "chunk": chunks[chunk_id],
            }
        )

    results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return results[:top_k]


# =============================================================================
# METRICS
# =============================================================================

def any_gold_retrieved(
    retrieved_ids: list[str],
    relevant_ids: list[str],
    k: int,
) -> bool:
    """
    Original hit-style Recall@K.

    TRUE if at least ONE gold chunk appears in Top-K.
    """

    if not relevant_ids:
        return False

    retrieved_top_k = set(retrieved_ids[:k])
    gold_ids = set(relevant_ids)

    return bool(gold_ids & retrieved_top_k)


def all_gold_retrieved(
    retrieved_ids: list[str],
    relevant_ids: list[str],
    k: int,
) -> bool:
    """
    STRICT retrieval metric.

    TRUE only if EVERY required gold chunk appears in Top-K.

    Example:

        Gold = [A, B, C]

        Top-10 = [A, X, Y, B, Z, ...]

        => FAIL because C is missing.
    """

    if not relevant_ids:
        return False

    retrieved_top_k = set(retrieved_ids[:k])
    gold_ids = set(relevant_ids)

    return gold_ids.issubset(retrieved_top_k)


def gold_coverage(
    retrieved_ids: list[str],
    relevant_ids: list[str],
    k: int,
) -> float:
    """
    Fraction of required gold chunks retrieved in Top-K.

    Example:

        Gold = [A, B, C]
        Retrieved = [A, B, X, Y, ...]

        Coverage = 2 / 3 = 0.667
    """

    if not relevant_ids:
        return 0.0

    retrieved_top_k = set(retrieved_ids[:k])
    gold_ids = set(relevant_ids)

    found = len(gold_ids & retrieved_top_k)

    return found / len(gold_ids)


def reciprocal_rank(
    retrieved_ids: list[str],
    relevant_ids: list[str],
) -> float:
    """
    MRR contribution.

    Uses the FIRST relevant gold chunk.

    Rank 1 -> 1.0
    Rank 2 -> 0.5
    Rank 3 -> 0.333...
    Not in Top-10 -> 0
    """

    if not relevant_ids:
        return 0.0

    relevant_ids = set(relevant_ids)

    for rank, chunk_id in enumerate(
        retrieved_ids,
        start=1,
    ):
        if chunk_id in relevant_ids:
            return 1.0 / rank

    return 0.0


def first_relevant_rank(
    retrieved_ids: list[str],
    relevant_ids: list[str],
):
    """
    Return the rank of the first relevant chunk.

    Returns None if no relevant chunk appears.
    """

    if not relevant_ids:
        return None

    relevant_ids = set(relevant_ids)

    for rank, chunk_id in enumerate(
        retrieved_ids,
        start=1,
    ):
        if chunk_id in relevant_ids:
            return rank

    return None


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def percentile(values, percentile):
    """
    Calculate percentile safely.
    """

    if not values:
        return 0.0

    return float(
        np.percentile(
            np.array(values),
            percentile,
        )
    )


def get_service_from_chunk_id(chunk_id: str) -> str:
    """
    Extract OpenStack service from chunk ID.

    Example:

        nova_admin_architecture_0001
        -> nova
    """

    return chunk_id.split("_")[0]


def get_hop_label(relevant_ids: list[str]) -> str:
    """
    Determine hop label based on number of gold chunks.
    """

    count = len(relevant_ids)

    if count == 0:
        return "unanswerable"

    if count == 1:
        return "1-hop"

    if count == 2:
        return "2-hop"

    return "3+-hop"


def get_service_group(relevant_ids: list[str]) -> str:
    """
    Determine whether gold evidence belongs to one service
    or multiple services.
    """

    if not relevant_ids:
        return "unanswerable"

    services = {
        get_service_from_chunk_id(chunk_id)
        for chunk_id in relevant_ids
    }

    if len(services) == 1:
        return next(iter(services))

    return "cross-service"


# =============================================================================
# EVALUATE ONE QUESTION
# =============================================================================

def evaluate_question(
    question_item,
    chunks,
    embedding_records,
):
    """
    Run retrieval and calculate all metrics for one question.
    """

    question_id = question_item["id"]
    question = question_item["question"]
    question_type = question_item["type"]

    relevant_ids = question_item["relevant_chunk_ids"]

    # -------------------------------------------------------------------------
    # Retrieval timing
    # -------------------------------------------------------------------------

    start_time = time.perf_counter()

    results = search(
        query=question,
        chunks=chunks,
        embedding_records=embedding_records,
        top_k=10,
    )

    end_time = time.perf_counter()

    latency_ms = (end_time - start_time) * 1000

    retrieved_ids = [
        result["chunk_id"]
        for result in results
    ]

    # -------------------------------------------------------------------------
    # Metrics
    # -------------------------------------------------------------------------

    any_r5 = any_gold_retrieved(
        retrieved_ids,
        relevant_ids,
        5,
    )

    any_r10 = any_gold_retrieved(
        retrieved_ids,
        relevant_ids,
        10,
    )

    all_r5 = all_gold_retrieved(
        retrieved_ids,
        relevant_ids,
        5,
    )

    all_r10 = all_gold_retrieved(
        retrieved_ids,
        relevant_ids,
        10,
    )

    coverage_r5 = gold_coverage(
        retrieved_ids,
        relevant_ids,
        5,
    )

    coverage_r10 = gold_coverage(
        retrieved_ids,
        relevant_ids,
        10,
    )

    mrr = reciprocal_rank(
        retrieved_ids,
        relevant_ids,
    )

    first_rank = first_relevant_rank(
        retrieved_ids,
        relevant_ids,
    )

    # -------------------------------------------------------------------------
    # Missing gold chunks
    # -------------------------------------------------------------------------

    retrieved_top10 = set(retrieved_ids[:10])
    gold_set = set(relevant_ids)

    found_gold = [
        chunk_id
        for chunk_id in relevant_ids
        if chunk_id in retrieved_top10
    ]

    missing_gold = [
        chunk_id
        for chunk_id in relevant_ids
        if chunk_id not in retrieved_top10
    ]

    # -------------------------------------------------------------------------
    # Strict pass/fail
    # -------------------------------------------------------------------------

    if not relevant_ids:
        strict_status = "UNANSWERABLE"
    elif all_r10:
        strict_status = "PASS"
    else:
        strict_status = "FAIL"

    # -------------------------------------------------------------------------
    # Result
    # -------------------------------------------------------------------------

    return {
        "id": question_id,
        "question": question,
        "type": question_type,

        "hop": get_hop_label(relevant_ids),
        "service": get_service_group(relevant_ids),

        "gold_chunk_ids": relevant_ids,
        "num_gold_chunks": len(relevant_ids),

        "retrieved_top10": retrieved_ids,

        "found_gold_chunks": found_gold,
        "missing_gold_chunks": missing_gold,

        "gold_coverage_at_5": coverage_r5,
        "gold_coverage_at_10": coverage_r10,

        "any_gold_recall_at_5": any_r5,
        "any_gold_recall_at_10": any_r10,

        "all_gold_at_5": all_r5,
        "all_gold_at_10": all_r10,

        "strict_status": strict_status,

        "first_relevant_rank": first_rank,
        "mrr_at_10": mrr,

        "latency_ms": latency_ms,

        "retrieved_results": results,
    }


# =============================================================================
# AGGREGATION
# =============================================================================

def aggregate_results(results):
    """
    Calculate overall metrics.
    """

    answerable = [
        r
        for r in results
        if r["gold_chunk_ids"]
    ]

    unanswerable = [
        r
        for r in results
        if not r["gold_chunk_ids"]
    ]

    latencies = [
        r["latency_ms"]
        for r in results
    ]

    # -------------------------------------------------------------------------
    # Any-gold metrics
    # -------------------------------------------------------------------------

    any_r5 = (
        sum(
            r["any_gold_recall_at_5"]
            for r in answerable
        )
        / len(answerable)
        if answerable
        else 0
    )

    any_r10 = (
        sum(
            r["any_gold_recall_at_10"]
            for r in answerable
        )
        / len(answerable)
        if answerable
        else 0
    )

    # -------------------------------------------------------------------------
    # STRICT all-gold metrics
    # -------------------------------------------------------------------------

    all_r5 = (
        sum(
            r["all_gold_at_5"]
            for r in answerable
        )
        / len(answerable)
        if answerable
        else 0
    )

    all_r10 = (
        sum(
            r["all_gold_at_10"]
            for r in answerable
        )
        / len(answerable)
        if answerable
        else 0
    )

    # -------------------------------------------------------------------------
    # Coverage
    # -------------------------------------------------------------------------

    coverage5 = (
        sum(
            r["gold_coverage_at_5"]
            for r in answerable
        )
        / len(answerable)
        if answerable
        else 0
    )

    coverage10 = (
        sum(
            r["gold_coverage_at_10"]
            for r in answerable
        )
        / len(answerable)
        if answerable
        else 0
    )

    # -------------------------------------------------------------------------
    # MRR
    # -------------------------------------------------------------------------

    mrr = (
        sum(
            r["mrr_at_10"]
            for r in answerable
        )
        / len(answerable)
        if answerable
        else 0
    )

    return {
        "total_questions": len(results),

        "answerable_questions": len(answerable),

        "unanswerable_questions": len(unanswerable),

        # Original hit-style metric
        "any_gold_recall_at_5": any_r5,
        "any_gold_recall_at_10": any_r10,

        # New strict metric
        "all_gold_at_5": all_r5,
        "all_gold_at_10": all_r10,

        # Evidence coverage
        "average_gold_coverage_at_5": coverage5,
        "average_gold_coverage_at_10": coverage10,

        "mrr_at_10": mrr,

        "avg_latency_ms": float(
            np.mean(latencies)
        ),

        "p50_latency_ms": percentile(
            latencies,
            50,
        ),

        "p95_latency_ms": percentile(
            latencies,
            95,
        ),
    }


# =============================================================================
# GROUPED EVALUATION
# =============================================================================

def aggregate_group(results, field, value):
    """
    Calculate metrics for a particular group.

    Example:

        field="type"
        value="comparison"
    """

    group = [
        r
        for r in results
        if r[field] == value
        and r["gold_chunk_ids"]
    ]

    if not group:
        return {
            "N": 0,
            "R@5": 0.0,
            "R@10": 0.0,
            "All-Gold@5": 0.0,
            "All-Gold@10": 0.0,
            "Coverage@5": 0.0,
            "Coverage@10": 0.0,
            "MRR@10": 0.0,
            "Avg ms": 0.0,
            "P50 ms": 0.0,
            "P95 ms": 0.0,
        }

    latencies = [
        r["latency_ms"]
        for r in group
    ]

    return {
        "N": len(group),

        "R@5": 100 * np.mean([
            r["any_gold_recall_at_5"]
            for r in group
        ]),

        "R@10": 100 * np.mean([
            r["any_gold_recall_at_10"]
            for r in group
        ]),

        "All-Gold@5": 100 * np.mean([
            r["all_gold_at_5"]
            for r in group
        ]),

        "All-Gold@10": 100 * np.mean([
            r["all_gold_at_10"]
            for r in group
        ]),

        "Coverage@5": 100 * np.mean([
            r["gold_coverage_at_5"]
            for r in group
        ]),

        "Coverage@10": 100 * np.mean([
            r["gold_coverage_at_10"]
            for r in group
        ]),

        "MRR@10": np.mean([
            r["mrr_at_10"]
            for r in group
        ]),

        "Avg ms": np.mean(latencies),

        "P50 ms": percentile(
            latencies,
            50,
        ),

        "P95 ms": percentile(
            latencies,
            95,
        ),
    }


# =============================================================================
# PRINT GROUP TABLE
# =============================================================================

def print_group_table(
    results,
    field,
    values,
    title,
):
    """
    Print category/hop/service evaluation table.
    """

    print()
    print("=" * 150)
    print(title)
    print("=" * 150)

    print(
        f"{'Group':<22}"
        f"{'N':>5}"
        f"{'R@5':>10}"
        f"{'R@10':>10}"
        f"{'All@5':>10}"
        f"{'All@10':>10}"
        f"{'Cov@5':>10}"
        f"{'Cov@10':>10}"
        f"{'MRR@10':>10}"
        f"{'Avg ms':>11}"
        f"{'P50 ms':>11}"
        f"{'P95 ms':>11}"
    )

    print("-" * 150)

    for value in values:

        metrics = aggregate_group(
            results,
            field,
            value,
        )

        print(
            f"{str(value):<22}"
            f"{metrics['N']:>5}"
            f"{metrics['R@5']:>9.1f}%"
            f"{metrics['R@10']:>9.1f}%"
            f"{metrics['All-Gold@5']:>9.1f}%"
            f"{metrics['All-Gold@10']:>9.1f}%"
            f"{metrics['Coverage@5']:>9.1f}%"
            f"{metrics['Coverage@10']:>9.1f}%"
            f"{metrics['MRR@10']:>10.4f}"
            f"{metrics['Avg ms']:>11.2f}"
            f"{metrics['P50 ms']:>11.2f}"
            f"{metrics['P95 ms']:>11.2f}"
        )


# =============================================================================
# FAILURE REPORT
# =============================================================================

def print_failures(results):
    """
    Print every question that failed strict All-Gold@10.
    """

    failures = [
        r
        for r in results
        if r["strict_status"] == "FAIL"
    ]

    print()
    print("=" * 110)
    print(f"STRICT FAILURES ({len(failures)})")
    print("=" * 110)

    for result in failures:

        print()
        print(
            f"{result['id']} "
            f"[{result['type']}] "
            f"[{result['hop']}] "
            f"[{result['service']}]"
        )

        print(
            f"Question: {result['question']}"
        )

        print(
            f"Gold chunks "
            f"({result['num_gold_chunks']}): "
            f"{result['gold_chunk_ids']}"
        )

        print(
            f"Found: "
            f"{result['found_gold_chunks']}"
        )

        print(
            f"Missing: "
            f"{result['missing_gold_chunks']}"
        )

        print(
            f"Coverage@5: "
            f"{result['gold_coverage_at_5']:.2%}"
        )

        print(
            f"Coverage@10: "
            f"{result['gold_coverage_at_10']:.2%}"
        )

        print("Retrieved Top-10:")

        for rank, chunk_id in enumerate(
            result["retrieved_top10"],
            start=1,
        ):
            print(
                f"   {rank:>2}. {chunk_id}"
            )


# =============================================================================
# TOP-1 SUCCESSES
# =============================================================================

def print_top1_successes(results):
    """
    Print questions where the first retrieved chunk
    is one of the gold chunks.
    """

    successes = [
        r
        for r in results
        if r["first_relevant_rank"] == 1
    ]

    print()
    print("=" * 110)
    print(
        f"TOP-1 SUCCESSES ({len(successes)})"
    )
    print("=" * 110)

    for result in successes:

        print(
            f"{result['id']} | "
            f"{result['type']:<20} | "
            f"{result['hop']:<12} | "
            f"{result['service']:<15} | "
            f"{result['question']}"
        )


# =============================================================================
# RANK DISTRIBUTION
# =============================================================================

def print_rank_distribution(results):
    """
    Print distribution of first relevant result rank.
    """

    answerable = [
        r
        for r in results
        if r["gold_chunk_ids"]
    ]

    rank_counts = {}

    for result in answerable:

        rank = result["first_relevant_rank"]

        if rank is None:
            rank = "Not in Top-10"

        rank_counts[rank] = (
            rank_counts.get(rank, 0) + 1
        )

    print()
    print("=" * 80)
    print("FIRST RELEVANT RESULT DISTRIBUTION")
    print("=" * 80)

    total = len(answerable)

    for rank in [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        "Not in Top-10",
    ]:

        count = rank_counts.get(rank, 0)

        if count:
            print(
                f"{str(rank):<18}"
                f"{count:>4} "
                f"({100 * count / total:.1f}%)"
            )


# =============================================================================
# UNANSWERABLE EVALUATION
# =============================================================================

def evaluate_unanswerable(results):
    """
    Report how the system behaves on questions
    whose gold evidence set is empty.

    There is no Recall@K here because there is
    intentionally no gold chunk.

    We simply report that retrieval produced results,
    which demonstrates that dense retrieval does not
    currently have an abstention mechanism.
    """

    unanswerable = [
        r
        for r in results
        if not r["gold_chunk_ids"]
    ]

    if not unanswerable:
        return

    print()
    print("=" * 100)
    print("UNANSWERABLE QUESTIONS")
    print("=" * 100)

    for result in unanswerable:

        print()
        print(
            f"{result['id']} | "
            f"{result['question']}"
        )

        print("Retrieved Top-10:")

        for rank, chunk_id in enumerate(
            result["retrieved_top10"],
            start=1,
        ):
            print(
                f"   {rank:>2}. {chunk_id}"
            )


# =============================================================================
# MAIN
# =============================================================================

def main():

    print()
    print("=" * 110)
    print("RUNNING DENSE RETRIEVAL EVALUATION")
    print("=" * 110)

    # -------------------------------------------------------------------------
    # Load
    # -------------------------------------------------------------------------

    chunks = load_chunks(
        CHUNKS_PATH
    )

    embedding_records = load_embeddings(
        EMBEDDINGS_PATH
    )

    questions = load_questions(
        QUESTIONS_PATH
    )

    print(
        f"Questions: {len(questions)}"
    )

    print(
        f"Chunks: {len(chunks)}"
    )

    print(
        f"Embeddings: {len(embedding_records)}"
    )

    # -------------------------------------------------------------------------
    # Evaluate
    # -------------------------------------------------------------------------

    results = []

    for i, question_item in enumerate(
        questions,
        start=1,
    ):

        result = evaluate_question(
            question_item,
            chunks,
            embedding_records,
        )

        results.append(result)

        # Status for console
        if result["strict_status"] == "PASS":
            status = "✅"
        elif result["strict_status"] == "UNANSWERABLE":
            status = "❌"
        else:
            status = "❌"

        print(
            f"{status} "
            f"{result['id']} | "
            f"rank="
            f"{result['first_relevant_rank'] or 'MISS':<4} | "
            f"latency="
            f"{result['latency_ms']:7.2f} ms | "
            f"{result['question']}"
        )

    # -------------------------------------------------------------------------
    # Overall
    # -------------------------------------------------------------------------

    overall = aggregate_results(
        results
    )

    print()
    print("#" * 110)
    print("OVERALL V1 DENSE RETRIEVAL BASELINE")
    print("#" * 110)

    print(
        f"Questions: "
        f"{overall['total_questions']}"
    )

    print(
        f"Answerable: "
        f"{overall['answerable_questions']}"
    )

    print(
        f"Unanswerable: "
        f"{overall['unanswerable_questions']}"
    )

    print()

    print(
        "ANY-GOLD METRICS "
        "(original hit-style evaluation)"
    )

    print(
        f"Recall@5:  "
        f"{100 * overall['any_gold_recall_at_5']:.2f}%"
    )

    print(
        f"Recall@10: "
        f"{100 * overall['any_gold_recall_at_10']:.2f}%"
    )

    print()

    print(
        "STRICT ALL-GOLD METRICS"
    )

    print(
        f"All-Gold@5:  "
        f"{100 * overall['all_gold_at_5']:.2f}%"
    )

    print(
        f"All-Gold@10: "
        f"{100 * overall['all_gold_at_10']:.2f}%"
    )

    print()

    print(
        "EVIDENCE COVERAGE"
    )

    print(
        f"Average Gold Coverage@5:  "
        f"{100 * overall['average_gold_coverage_at_5']:.2f}%"
    )

    print(
        f"Average Gold Coverage@10: "
        f"{100 * overall['average_gold_coverage_at_10']:.2f}%"
    )

    print()

    print(
        f"MRR@10: "
        f"{overall['mrr_at_10']:.4f}"
    )

    print(
        f"Avg latency: "
        f"{overall['avg_latency_ms']:.2f} ms"
    )

    print(
        f"P50 latency: "
        f"{overall['p50_latency_ms']:.2f} ms"
    )

    print(
        f"P95 latency: "
        f"{overall['p95_latency_ms']:.2f} ms"
    )

    # -------------------------------------------------------------------------
    # Category
    # -------------------------------------------------------------------------

    category_values = [
        "single_hop",
        "exact_terminology",
        "technical_detail",
        "comparison",
        "reasoning",
        "two_hop",
        "multi_hop",
        "cross_document",
        "unanswerable",
    ]

    print_group_table(
        results,
        field="type",
        values=category_values,
        title="CATEGORY-WISE EVALUATION",
    )

    # -------------------------------------------------------------------------
    # Hop
    # -------------------------------------------------------------------------

    hop_values = [
        "1-hop",
        "2-hop",
        "3+-hop",
        "unanswerable",
    ]

    print_group_table(
        results,
        field="hop",
        values=hop_values,
        title="HOP-WISE EVALUATION",
    )

    # -------------------------------------------------------------------------
    # Service
    # -------------------------------------------------------------------------

    service_values = [
        "neutron",
        "swift",
        "nova",
        "keystone",
        "glance",
        "barbican",
        "heat",
        "placement",
        "cinder",
        "cross-service",
        "unanswerable",
    ]

    print_group_table(
        results,
        field="service",
        values=service_values,
        title="SERVICE-WISE EVALUATION",
    )

    # -------------------------------------------------------------------------
    # Rank distribution
    # -------------------------------------------------------------------------

    print_rank_distribution(
        results
    )

    # -------------------------------------------------------------------------
    # Strict failures
    # -------------------------------------------------------------------------

    print_failures(
        results
    )

    # -------------------------------------------------------------------------
    # Top-1 successes
    # -------------------------------------------------------------------------

    print_top1_successes(
        results
    )

    # -------------------------------------------------------------------------
    # Unanswerable
    # -------------------------------------------------------------------------

    evaluate_unanswerable(
        results
    )

    # -------------------------------------------------------------------------
    # Save JSON
    # -------------------------------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = {
        "configuration": {
            "retrieval": "dense",
            "embedding_model": "jina-embeddings-v3",
            "top_k_evaluated": 10,

            "strict_evaluation_rule": (
                "A question passes All-Gold@K only when "
                "every relevant gold chunk is present in Top-K."
            ),

            "any_gold_recall_definition": (
                "Question passes when at least one relevant "
                "gold chunk is present in Top-K."
            ),
        },

        "overall": overall,

        "results": results,
    }

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            output,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print("#" * 110)
    print("REPORT SAVED")
    print("#" * 110)

    print(
        OUTPUT_PATH
    )


if __name__ == "__main__":
    main()