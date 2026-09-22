"""
Workspace and Document storage manager for user documents.

Filesystem-based persistence under `data/user_documents/<workspace_id>/`.
Stores:
    - metadata.json (workspace info, uploaded documents list)
    - documents/ (sanitized uploaded source files)
    - chunks.jsonl (chunk text and metadata)
    - embeddings.jsonl (Jina dense embeddings)

Guarantees 100% isolation from OpenStack benchmark data in data/processed/ and data/benchmark/.
"""
from __future__ import annotations

import json
import logging
import os
import re
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

USER_DOCS_ROOT = Path("data/user_documents")
COLLECTIONS_ROOT = USER_DOCS_ROOT

# Configurable TTL for temporary user workspaces (default: 3600 seconds = 1 hour)
WORKSPACE_TTL_SECONDS = int(os.environ.get("WORKSPACE_TTL_SECONDS", "3600"))
WORKSPACE_CLEANUP_INTERVAL_SECONDS = int(os.environ.get("WORKSPACE_CLEANUP_INTERVAL_SECONDS", "60"))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_iso(iso_str: str | None) -> datetime | None:
    if not iso_str:
        return None
    try:
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def sanitize_filename(filename: str) -> str:
    """Strip path traversal elements and unsafe characters from filenames."""
    name = Path(filename).name
    clean = re.sub(r"[^\w\.\-\s\(\)\[\]]", "_", name).strip()
    return clean or "document"


class WorkspaceManager:
    def __init__(self, root_dir: Path = USER_DOCS_ROOT, default_ttl: int = WORKSPACE_TTL_SECONDS):
        self.root_dir = root_dir
        self.default_ttl = default_ttl
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def _get_ws_dir(self, workspace_id: str) -> Path:
        clean_id = re.sub(r"[^\w\-]", "", workspace_id)
        if not clean_id or clean_id != workspace_id:
            raise ValueError(f"Invalid workspace_id: {workspace_id}")
        ws_dir = self.root_dir / clean_id
        # Boundary check: ensure directory is strictly inside root_dir
        resolved_root = self.root_dir.resolve()
        resolved_ws = ws_dir.resolve()
        if not str(resolved_ws).startswith(str(resolved_root)):
            raise ValueError(f"Directory traversal detected for workspace_id: {workspace_id}")
        return ws_dir

    _get_coll_dir = _get_ws_dir

    def _get_meta_path(self, workspace_id: str) -> Path:
        return self._get_ws_dir(workspace_id) / "metadata.json"

    def touch_workspace(self, workspace_id: str) -> None:
        """Update last_activity timestamp for the workspace."""
        try:
            meta_path = self._get_meta_path(workspace_id)
            if meta_path.exists():
                with meta_path.open("r", encoding="utf-8") as f:
                    meta = json.load(f)
                meta["last_activity"] = _now_iso()
                with meta_path.open("w", encoding="utf-8") as f:
                    json.dump(meta, f, indent=2)
        except Exception as exc:
            logger.debug("Failed to touch workspace %s: %s", workspace_id, exc)

    def is_workspace_expired(self, workspace_id: str, ttl_seconds: int | None = None) -> bool:
        """
        Check if workspace has exceeded its inactivity TTL.
        Uses last_activity if present, falling back to created_at or directory mtime.
        """
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        try:
            ws_dir = self._get_ws_dir(workspace_id)
            if not ws_dir.exists():
                return False

            meta_path = self._get_meta_path(workspace_id)
            last_dt = None
            if meta_path.exists():
                try:
                    with meta_path.open("r", encoding="utf-8") as f:
                        meta = json.load(f)
                    last_dt = _parse_iso(meta.get("last_activity")) or _parse_iso(meta.get("created_at"))
                except Exception:
                    pass

            if last_dt is None:
                # Fallback to directory last modified time
                mtime = ws_dir.stat().st_mtime
                last_dt = datetime.fromtimestamp(mtime, tz=timezone.utc)

            elapsed = (datetime.now(timezone.utc) - last_dt).total_seconds()
            return elapsed > ttl
        except Exception as exc:
            logger.error("Error checking expiration for %s: %s", workspace_id, exc)
            return False

    def get_or_create_workspace(self, workspace_id: str = "default", name: str = "My Documents") -> dict[str, Any]:
        """Get or initialize a temporary user workspace."""
        ws_dir = self._get_ws_dir(workspace_id)
        meta_path = self._get_meta_path(workspace_id)

        # If existing workspace has expired, clean it up before recreating
        if ws_dir.exists() and self.is_workspace_expired(workspace_id):
            logger.info("workspace_expired workspace_id=%s", workspace_id)
            self.delete_workspace(workspace_id)
            logger.info("workspace_cleanup_completed workspace_id=%s", workspace_id)

        now = _now_iso()
        if not meta_path.exists():
            ws_dir.mkdir(parents=True, exist_ok=True)
            (ws_dir / "documents").mkdir(parents=True, exist_ok=True)
            (ws_dir / "chunks.jsonl").touch()
            (ws_dir / "embeddings.jsonl").touch()

            meta = {
                "workspace_id": workspace_id,
                "name": name,
                "created_at": now,
                "last_activity": now,
                "documents": [],
            }
            with meta_path.open("w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
            return meta

        try:
            with meta_path.open("r", encoding="utf-8") as f:
                meta = json.load(f)
            # Touch last_activity
            meta["last_activity"] = now
            with meta_path.open("w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
            return meta
        except Exception as e:
            logger.error("Error reading workspace %s: %s", workspace_id, e)
            return {
                "workspace_id": workspace_id,
                "name": name,
                "created_at": now,
                "last_activity": now,
                "documents": [],
            }

    def save_document_file(
        self,
        workspace_id: str,
        filename: str,
        content: bytes,
        file_type: str,
    ) -> dict[str, Any]:
        """Save an uploaded file and register document entry."""
        ws_dir = self._get_ws_dir(workspace_id)
        if not ws_dir.exists():
            self.get_or_create_workspace(workspace_id)

        safe_name = sanitize_filename(filename)
        doc_id = f"doc_{uuid.uuid4().hex[:12]}"
        stored_filename = f"{doc_id}_{safe_name}"
        dest_path = ws_dir / "documents" / stored_filename

        with dest_path.open("wb") as f:
            f.write(content)

        doc_entry = {
            "document_id": doc_id,
            "filename": safe_name,
            "file_type": file_type,
            "file_size": len(content),
            "stored_filename": stored_filename,
            "uploaded_at": _now_iso(),
            "status": "Processing",
            "chunk_count": 0,
            "error": None,
        }

        meta = self.get_or_create_workspace(workspace_id)
        docs = meta.get("documents", [])
        docs.append(doc_entry)
        meta["documents"] = docs

        with self._get_meta_path(workspace_id).open("w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        return doc_entry

    def update_document_status(
        self,
        workspace_id: str,
        document_id: str,
        status: str,
        chunk_count: int | None = None,
        error: str | None = None,
    ) -> None:
        """Update indexing status of a document."""
        meta = self.get_or_create_workspace(workspace_id)
        for doc in meta.get("documents", []):
            if doc["document_id"] == document_id:
                doc["status"] = status
                if chunk_count is not None:
                    doc["chunk_count"] = chunk_count
                if error is not None:
                    doc["error"] = error
                break

        with self._get_meta_path(workspace_id).open("w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

    def delete_document(self, workspace_id: str, document_id: str) -> bool:
        """
        Delete a document:
        1. Remove original file from documents/
        2. Remove its chunks from chunks.jsonl
        3. Remove its embeddings from embeddings.jsonl
        4. Update metadata.json
        """
        ws_dir = self._get_ws_dir(workspace_id)
        meta = self.get_or_create_workspace(workspace_id)

        doc_to_delete = None
        new_docs = []
        for doc in meta.get("documents", []):
            if doc["document_id"] == document_id:
                doc_to_delete = doc
            else:
                new_docs.append(doc)

        if not doc_to_delete:
            return False

        # Remove physical file
        stored_name = doc_to_delete.get("stored_filename")
        if stored_name:
            file_path = ws_dir / "documents" / stored_name
            if file_path.exists():
                file_path.unlink()

        # Filter chunks.jsonl
        chunks_file = ws_dir / "chunks.jsonl"
        kept_chunk_ids = set()
        if chunks_file.exists():
            temp_chunks = []
            with chunks_file.open("r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        c = json.loads(line)
                        if c.get("document_id") != document_id:
                            temp_chunks.append(line)
                            kept_chunk_ids.add(c.get("chunk_id"))
            with chunks_file.open("w", encoding="utf-8") as f:
                f.writelines(temp_chunks)

        # Filter embeddings.jsonl
        emb_file = ws_dir / "embeddings.jsonl"
        if emb_file.exists():
            temp_embs = []
            with emb_file.open("r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        e = json.loads(line)
                        if e.get("chunk_id") in kept_chunk_ids:
                            temp_embs.append(line)
            with emb_file.open("w", encoding="utf-8") as f:
                f.writelines(temp_embs)

        # Update metadata
        meta["documents"] = new_docs
        with self._get_meta_path(workspace_id).open("w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        logger.info("Deleted document %s from workspace %s", document_id, workspace_id)
        return True

    def get_workspace(self, workspace_id: str = "default", auto_cleanup: bool = True) -> dict[str, Any] | None:
        ws_dir = self._get_ws_dir(workspace_id)
        if not ws_dir.exists():
            return None

        if auto_cleanup and self.is_workspace_expired(workspace_id):
            logger.info("workspace_expired workspace_id=%s", workspace_id)
            self.delete_workspace(workspace_id)
            logger.info("workspace_cleanup_completed workspace_id=%s", workspace_id)
            return None

        meta_path = self._get_meta_path(workspace_id)
        if not meta_path.exists():
            return None
        try:
            with meta_path.open("r", encoding="utf-8") as f:
                meta = json.load(f)
            # Touch activity on successful fetch
            self.touch_workspace(workspace_id)
            return meta
        except Exception:
            return None

    def list_workspaces(self) -> list[dict[str, Any]]:
        results = []
        for p in self.root_dir.iterdir():
            if p.is_dir() and (p / "metadata.json").exists():
                if self.is_workspace_expired(p.name):
                    logger.info("workspace_expired workspace_id=%s", p.name)
                    self.delete_workspace(p.name)
                    logger.info("workspace_cleanup_completed workspace_id=%s", p.name)
                    continue
                try:
                    with (p / "metadata.json").open("r", encoding="utf-8") as f:
                        data = json.load(f)
                        results.append({
                            "workspace_id": data.get("workspace_id", p.name),
                            "name": data.get("name", p.name),
                            "created_at": data.get("created_at", ""),
                            "last_activity": data.get("last_activity", ""),
                            "document_count": len(data.get("documents", [])),
                        })
                except Exception:
                    pass
        return results

    def create_workspace(self, workspace_id: str | None = None, name: str = "My Documents") -> dict[str, Any]:
        ws_id = workspace_id or f"ws_{uuid.uuid4().hex[:12]}"
        return self.get_or_create_workspace(ws_id, name=name)

    def delete_workspace(self, workspace_id: str) -> bool:
        """
        Workspace-scoped deletion.
        Deletes all temporary files, extracted chunks, embeddings, conversations, and metadata.
        Safe and idempotent: never modifies outside root_dir, ignores already-deleted folders.
        """
        try:
            ws_dir = self._get_ws_dir(workspace_id)
            if ws_dir.exists():
                shutil.rmtree(ws_dir, ignore_errors=True)
                return True
            return False
        except Exception as exc:
            logger.error("Error deleting workspace %s: %s", workspace_id, exc)
            return False

    def cleanup_expired_workspaces(self, ttl_seconds: int | None = None) -> list[str]:
        """
        Scan all temporary user workspaces and delete those with no activity for > TTL.
        NEVER touches data/benchmark/, data/processed/, data/metadata/, or data/raw/.
        """
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        cleaned: list[str] = []
        resolved_root = self.root_dir.resolve()

        try:
            for p in self.root_dir.iterdir():
                if not p.is_dir():
                    continue

                # Strict boundary check: ensure p is directly inside root_dir
                if p.resolve().parent != resolved_root:
                    logger.warning("Skipping suspect directory outside root: %s", p)
                    continue

                ws_id = p.name
                if self.is_workspace_expired(ws_id, ttl_seconds=ttl):
                    logger.info("workspace_expired workspace_id=%s", ws_id)
                    deleted = self.delete_workspace(ws_id)
                    if deleted:
                        logger.info("workspace_cleanup_completed workspace_id=%s", ws_id)
                        cleaned.append(ws_id)
        except Exception as exc:
            logger.error("Error during workspace cleanup sweep: %s", exc)

        return cleaned

    # Aliases for backward compatibility
    get_collection = get_workspace
    create_collection = create_workspace
    list_collections = list_workspaces
    delete_collection = delete_workspace


CollectionsManager = WorkspaceManager
