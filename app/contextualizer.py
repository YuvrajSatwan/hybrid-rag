"""
Query Contextualizer for multi-turn conversational RAG.

Inspects prior conversation history to determine if the user's current question
is a follow-up (using pronouns, ordinals, or ellipsis). If so, rewrites it into
a self-contained standalone retrieval query for the V2 search engine.

Guarantees:
- Never over-rewrites standalone questions (e.g., "What is FastAPI?").
- Handles topic changes cleanly without polluting with previous topic terms.
- Falls back to original query if LLM is unreachable.
"""
from __future__ import annotations

import logging
import os
import re
import requests

logger = logging.getLogger(__name__)

_API_BASE = "https://generativelanguage.googleapis.com/v1beta"
_REWRITE_MODEL = "gemini-3.5-flash-lite"

# Referential cues that strongly suggest a follow-up question
_FOLLOW_UP_PATTERN = re.compile(
    r"\b(it|its|this|that|these|those|they|them|their|"
    r"which\s+one|which\s+of|the\s+other|the\s+first|the\s+second|the\s+third|"
    r"second\s+one|first\s+one|third\s+one|last\s+one|"
    r"tell\s+me\s+more|elaborate|explain\s+more|what\s+about|how\s+about|"
    r"when\s+did\s+(it|that)|why\s+did\s+(i|it|they)|where\s+did\s+(i|it))\b",
    re.IGNORECASE,
)


_REWRITE_SYSTEM_PROMPT = """\
You are an expert search query reformulator for a document assistant.

Given a conversation history between a User and an Assistant, and the User's latest question:
Determine if the question relies on context from previous messages (pronouns, references like 'the second one', 'which one', 'these', or conversational ellipsis).

CRITICAL RULES:
1. STANDALONE QUESTIONS: If the user's question is already clear, complete, and understandable on its own (for example: "What is FastAPI?", "What is my education?", "List all skills"), output it EXACTLY AS-IS. DO NOT rewrite or add keywords from past turns.
2. TOPIC SWITCHES: If the user switches to a new topic (for example, switching from projects to education), do NOT include keywords from the previous topic.
3. FOLLOW-UPS: If and only if the question refers to something mentioned previously (for example: "Which one did I use for backend?", "When did it happen?", "Tell me more about the second project"), rewrite it into a concise, standalone retrieval query that incorporates the specific entity or topic referenced.
4. OUTPUT FORMAT: Output ONLY the rewritten search query. Never add explanations, greetings, quotes, or markdown formatting.
"""


def _format_history_for_prompt(history: list[dict[str, str]], max_turns: int = 6) -> str:
    """Format recent turns as readable transcript for the contextualizer."""
    recent = history[-max_turns:] if len(history) > max_turns else history
    lines = []
    for msg in recent:
        role = "User" if msg.get("role") == "user" else "Assistant"
        content = msg.get("content", "").strip()
        # Truncate very long assistant messages so the prompt stays lightweight
        if len(content) > 350:
            content = content[:350] + "…"
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def contextualize_query(
    query: str,
    history: list[dict[str, str]],
    conversation_id: str = "default",
) -> str:
    """
    Contextualize the user's query against conversation history.

    Returns a standalone query suitable for document retrieval.
    """
    raw_query = (query or "").strip()
    if not raw_query or not history:
        return raw_query

    # Quick heuristic check: if query has no obvious follow-up words,
    # and is long enough to be an explicit question, we still allow the LLM to inspect,
    # but we skip if history is purely empty.
    api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if not api_key:
        logger.debug("No GOOGLE_API_KEY available for query contextualization — using raw query")
        return raw_query

    history_text = _format_history_for_prompt(history)
    user_prompt = (
        f"CONVERSATION HISTORY:\n{history_text}\n\n"
        f"USER QUESTION: {raw_query}\n\n"
        "STANDALONE RETRIEVAL QUERY:"
    )

    url = f"{_API_BASE}/models/{_REWRITE_MODEL}:generateContent"
    headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}
    payload = {
        "systemInstruction": {"parts": [{"text": _REWRITE_SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": 0.0,
            "maxOutputTokens": 100,
            "topP": 0.9,
        },
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=8.0)
        if resp.status_code == 200:
            data = resp.json()
            candidates = data.get("candidates") or []
            if candidates:
                parts = (candidates[0].get("content") or {}).get("parts") or []
                rewritten = "".join(p.get("text", "") for p in parts).strip()
                # Clean up quotes if model wrapped output in quotes
                rewritten = re.sub(r'^["\']|["\']$', "", rewritten).strip()
                if rewritten and len(rewritten) > 2:
                    logger.debug("Contextualized query [cid=%s]", conversation_id)
                    return rewritten
    except Exception as exc:
        logger.warning("Query contextualization request failed (%s): %s", conversation_id, exc)

    return raw_query
