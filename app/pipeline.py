"""
RAG pipeline — retrieve then generate.

Supports both:
1. OpenStack reference corpus (using untouched V2 RerankRetriever stack)
2. Personal document collections (using isolated PersonalCollectionRetriever)

Never combines OpenStack and personal documents.
"""
from __future__ import annotations

import logging
import time
from pathlib import Path

from app.collections_manager import COLLECTIONS_ROOT
from app.conversation_manager import ConversationManager
from app.contextualizer import contextualize_query
from app.generator import generate_answer
from app.personal_retriever import PersonalCollectionRetriever
from app.schemas import Citation, QueryResponse

logger = logging.getLogger(__name__)

_SNIPPET_MAX = 250


def _make_snippet(text: str) -> str:
    """Return first _SNIPPET_MAX characters, trimmed at a word boundary."""
    text = text.strip()
    if len(text) <= _SNIPPET_MAX:
        return text
    truncated = text[:_SNIPPET_MAX]
    last_space = truncated.rfind(" ")
    if last_space > _SNIPPET_MAX // 2:
        truncated = truncated[:last_space]
    return truncated + "…"


def run_query(
    query: str,
    retriever,          # V2 RerankRetriever — loaded once at startup (for reranker or benchmark)
    chunks: dict,       # OpenStack chunk_id → chunk dict
    workspace_id: str | None = "default",
    collection_id: str | None = None,
    conversation_id: str | None = None,
    top_k: int = 10,
    ws_mgr=None,
) -> QueryResponse:
    """
    Full RAG pipeline:
        1. Retrieve top_k chunks from isolated user workspace
        2. Generate grounded answer
        3. Build citation objects
    """
    t0 = time.perf_counter()
    target_id = workspace_id or collection_id or "default"

    # If explicitly requesting internal OpenStack reference evaluation benchmark
    if target_id == "openstack":
        if not chunks or not hasattr(retriever, "rank"):
            latency_ms = (time.perf_counter() - t0) * 1000
            return QueryResponse(
                answer="The OpenStack benchmark evaluation corpus is not included in this deployment. Please upload your documents to create a temporary workspace.",
                citations=[],
                latency_ms=round(latency_ms, 1),
                workspace_id="openstack",
            )

        chunk_ids: list[str] = retriever.rank(query, top_k=top_k)
        retrieved_chunks: list[dict] = []
        for cid in chunk_ids:
            if cid in chunks:
                retrieved_chunks.append(chunks[cid])

        if not retrieved_chunks:
            latency_ms = (time.perf_counter() - t0) * 1000
            return QueryResponse(
                answer="I couldn't find enough information in your documents to answer that.",
                citations=[],
                latency_ms=round(latency_ms, 1),
                workspace_id="openstack",
            )

        answer = generate_answer(query, retrieved_chunks)
        latency_ms = (time.perf_counter() - t0) * 1000

        citations: list[Citation] = []
        for chunk in retrieved_chunks:
            citations.append(
                Citation(
                    chunk_id=chunk.get("chunk_id", ""),
                    title=chunk.get("title", "Document"),
                    source_url=chunk.get("source_url", ""),
                    filename=chunk.get("filename"),
                    page=chunk.get("page"),
                    section=chunk.get("section"),
                    snippet=_make_snippet(chunk.get("text", "")),
                )
            )

        return QueryResponse(
            answer=answer,
            citations=citations,
            latency_ms=round(latency_ms, 1),
            workspace_id="openstack",
        )

    # =========================================================================
    # User Document Workspace (Default & Primary Product Experience)
    # =========================================================================
    if ws_mgr is not None:
        ws_dir = ws_mgr._get_ws_dir(target_id)
        conv_mgr = ConversationManager(root_dir=ws_mgr.root_dir)
    else:
        ws_dir = COLLECTIONS_ROOT / target_id
        conv_mgr = ConversationManager()

    if not ws_dir.exists():
        ws_dir.mkdir(parents=True, exist_ok=True)

    # Manage conversation history
    cid, _ = conv_mgr.get_or_create(workspace_id=target_id, conversation_id=conversation_id)

    # Fetch prior history before recording current user turn
    prior_history = conv_mgr.get_recent_history(workspace_id=target_id, conversation_id=cid, max_turns=6)

    # Record current user turn
    conv_mgr.add_message(workspace_id=target_id, conversation_id=cid, role="user", content=query)

    reranker_model = getattr(retriever, "model", None)
    personal_retriever = PersonalCollectionRetriever(ws_dir, reranker_model=reranker_model)

    if personal_retriever.is_empty():
        latency_ms = (time.perf_counter() - t0) * 1000
        msg = "I couldn't find enough information in your documents to answer that. Please upload documents to begin."
        conv_mgr.add_message(workspace_id=target_id, conversation_id=cid, role="assistant", content=msg, latency_ms=round(latency_ms, 1))
        return QueryResponse(
            answer=msg,
            citations=[],
            latency_ms=round(latency_ms, 1),
            workspace_id=target_id,
            conversation_id=cid,
        )

    # Contextualize query if prior conversation history exists
    search_query = contextualize_query(query=query, history=prior_history, conversation_id=cid)

    # Retrieve using standalone contextualized query
    retrieved_chunks = personal_retriever.rank(search_query, top_k=top_k)

    if not retrieved_chunks:
        latency_ms = (time.perf_counter() - t0) * 1000
        msg = "I couldn't find enough information in your documents to answer that."
        conv_mgr.add_message(workspace_id=target_id, conversation_id=cid, role="assistant", content=msg, latency_ms=round(latency_ms, 1))
        return QueryResponse(
            answer=msg,
            citations=[],
            latency_ms=round(latency_ms, 1),
            workspace_id=target_id,
            conversation_id=cid,
        )

    # Generate answer with conversation context + authoritative retrieved chunks
    answer = generate_answer(query, retrieved_chunks, history=prior_history)
    latency_ms = (time.perf_counter() - t0) * 1000

    citations: list[Citation] = []
    for chunk in retrieved_chunks:
        citations.append(
            Citation(
                chunk_id=chunk.get("chunk_id", ""),
                title=chunk.get("title") or chunk.get("filename") or "Document",
                source_url=chunk.get("source_url", ""),
                filename=chunk.get("filename"),
                page=chunk.get("page"),
                section=chunk.get("section"),
                snippet=_make_snippet(chunk.get("text", "")),
            )
        )

    # Persist assistant turn with citations and latency
    conv_mgr.add_message(
        workspace_id=target_id,
        conversation_id=cid,
        role="assistant",
        content=answer,
        citations=[c.model_dump() for c in citations],
        latency_ms=round(latency_ms, 1),
    )

    return QueryResponse(
        answer=answer,
        citations=citations,
        latency_ms=round(latency_ms, 1),
        workspace_id=target_id,
        conversation_id=cid,
    )
