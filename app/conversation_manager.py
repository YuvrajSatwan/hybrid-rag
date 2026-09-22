"""
Conversation history manager for workspace-scoped multi-turn sessions.

Stores conversation threads on disk at:
    data/user_documents/{workspace_id}/conversations/{conversation_id}.json

Maintains clean isolation between different workspaces and provides bounded
history for prompt assembly.
"""
from __future__ import annotations

import json
import logging
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.collections_manager import USER_DOCS_ROOT

logger = logging.getLogger(__name__)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ConversationManager:
    def __init__(self, root_dir: Path = USER_DOCS_ROOT):
        self.root_dir = root_dir

    def _get_conv_dir(self, workspace_id: str) -> Path:
        clean_ws = re.sub(r"[^\w\-]", "", workspace_id) or "default"
        conv_dir = self.root_dir / clean_ws / "conversations"
        conv_dir.mkdir(parents=True, exist_ok=True)
        return conv_dir

    def _get_conv_path(self, workspace_id: str, conversation_id: str) -> Path:
        clean_cid = re.sub(r"[^\w\-]", "", conversation_id)
        if not clean_cid:
            clean_cid = "default"
        return self._get_conv_dir(workspace_id) / f"{clean_cid}.json"

    def get_or_create(
        self,
        workspace_id: str = "default",
        conversation_id: str | None = None,
    ) -> tuple[str, list[dict[str, Any]]]:
        """
        Get or initialize a conversation for the given workspace.
        Returns (conversation_id, messages_list).
        """
        cid = conversation_id or f"conv_{uuid.uuid4().hex[:12]}"
        path = self._get_conv_path(workspace_id, cid)

        if not path.exists():
            data = {
                "conversation_id": cid,
                "workspace_id": workspace_id,
                "created_at": _now_iso(),
                "updated_at": _now_iso(),
                "messages": [],
            }
            try:
                with path.open("w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
            except Exception as exc:
                logger.error("Failed to initialize conversation %s in %s: %s", cid, workspace_id, exc)
            return cid, []

        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return cid, data.get("messages", [])
        except Exception as exc:
            logger.error("Failed to read conversation %s in %s: %s", cid, workspace_id, exc)
            return cid, []

    def get_conversation(self, workspace_id: str, conversation_id: str) -> dict[str, Any] | None:
        """Read full conversation record including metadata and all messages."""
        path = self._get_conv_path(workspace_id, conversation_id)
        if not path.exists():
            return None
        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.error("Failed to read conversation %s: %s", conversation_id, exc)
            return None

    def add_message(
        self,
        workspace_id: str,
        conversation_id: str,
        role: str,
        content: str,
        citations: list[dict[str, Any]] | None = None,
        latency_ms: float | None = None,
    ) -> dict[str, Any]:
        """
        Append a message to the conversation and persist to disk.
        """
        cid, messages = self.get_or_create(workspace_id, conversation_id)
        msg_id = f"msg_{uuid.uuid4().hex[:10]}"
        msg = {
            "id": msg_id,
            "role": role,
            "content": content,
            "citations": citations or [],
            "timestamp": _now_iso(),
        }
        if latency_ms is not None:
            msg["latency_ms"] = latency_ms

        messages.append(msg)

        path = self._get_conv_path(workspace_id, cid)
        data = {
            "conversation_id": cid,
            "workspace_id": workspace_id,
            "updated_at": _now_iso(),
            "messages": messages,
        }
        try:
            with path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as exc:
            logger.error("Failed to save message to %s: %s", cid, exc)

        return msg

    def get_recent_history(
        self,
        workspace_id: str,
        conversation_id: str,
        max_turns: int = 6,
    ) -> list[dict[str, str]]:
        """
        Return the most recent user/assistant turns formatted for prompt context.
        Each entry has 'role' and 'content'.
        Bounded by max_turns (where 1 turn = 1 user or assistant message).
        """
        _, messages = self.get_or_create(workspace_id, conversation_id)
        recent = messages[-max_turns:] if len(messages) > max_turns else messages
        return [{"role": m["role"], "content": m["content"]} for m in recent]

    def delete_conversation(self, workspace_id: str, conversation_id: str) -> bool:
        """Delete a conversation file from disk."""
        path = self._get_conv_path(workspace_id, conversation_id)
        if path.exists():
            try:
                path.unlink()
                return True
            except Exception as exc:
                logger.error("Failed to delete conversation %s: %s", conversation_id, exc)
        return False
