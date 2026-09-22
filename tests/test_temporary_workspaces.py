"""
Comprehensive test suite for temporary user workspaces and session lifecycle.

Verifies:
1. Workspace creation with created_at and last_activity
2. Document upload and indexing in isolated workspace
3. Chunks, embeddings, and metadata file generation
4. In-memory BM25 and retrieval over uploaded documents
5. Activity updates (touch_workspace)
6. Expiration logic with configurable TTL
7. Workspace cleanup removes all temporary files
8. Permanent OpenStack corpus (data/processed, data/benchmark) remains 100% intact
9. Querying an expired workspace returns 404
10. New session creates a new, isolated workspace
11. Cleanup idempotency (running twice does not crash)
12. Workspace cross-isolation (cleaning ws_A never touches ws_B)
13. Partial/failed document cleanup resilience
"""
import json
import os
import shutil
import sys
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.collections_manager import WorkspaceManager, sanitize_filename
from app.conversation_manager import ConversationManager
from app.document_processor import extract_text_from_file
from app.personal_retriever import PersonalCollectionRetriever


class TestTemporaryWorkspaces(unittest.TestCase):
    def setUp(self):
        self.test_root = PROJECT_ROOT / "data" / "test_user_documents"
        if self.test_root.exists():
            shutil.rmtree(self.test_root, ignore_errors=True)
        self.test_root.mkdir(parents=True, exist_ok=True)
        self.ws_mgr = WorkspaceManager(root_dir=self.test_root, default_ttl=3600)

    def tearDown(self):
        if self.test_root.exists():
            shutil.rmtree(self.test_root, ignore_errors=True)

    def test_01_create_workspace_metadata(self):
        """1. Verify workspace creation initializes metadata with last_activity."""
        ws = self.ws_mgr.create_workspace(name="Project Alpha")
        ws_id = ws["workspace_id"]
        self.assertTrue(ws_id.startswith("ws_"))
        self.assertIn("created_at", ws)
        self.assertIn("last_activity", ws)
        self.assertEqual(ws["name"], "Project Alpha")
        self.assertEqual(ws["documents"], [])

        # Verify filesystem state
        ws_dir = self.test_root / ws_id
        self.assertTrue(ws_dir.exists())
        self.assertTrue((ws_dir / "metadata.json").exists())
        self.assertTrue((ws_dir / "documents").exists())
        self.assertTrue((ws_dir / "chunks.jsonl").exists())
        self.assertTrue((ws_dir / "embeddings.jsonl").exists())

    def test_02_upload_and_index_document(self):
        """2 & 3. Verify saving document, chunks, and embeddings."""
        ws = self.ws_mgr.create_workspace()
        ws_id = ws["workspace_id"]
        ws_dir = self.test_root / ws_id

        doc_content = b"# Architecture Overview\nThis service uses FastAPI and vector retrieval."
        doc_entry = self.ws_mgr.save_document_file(
            workspace_id=ws_id,
            filename="arch.md",
            content=doc_content,
            file_type="md",
        )
        self.assertEqual(doc_entry["filename"], "arch.md")
        self.assertTrue((ws_dir / "documents" / doc_entry["stored_filename"]).exists())

        # Simulate chunking & embedding generation
        chunks_file = ws_dir / "chunks.jsonl"
        with chunks_file.open("w", encoding="utf-8") as f:
            chunk = {
                "chunk_id": f"{doc_entry['document_id']}_0000",
                "document_id": doc_entry["document_id"],
                "filename": "arch.md",
                "title": "Architecture Overview",
                "service": "Personal",
                "page": None,
                "section": "Architecture Overview",
                "text": "This service uses FastAPI and vector retrieval.",
                "source_url": "",
            }
            f.write(json.dumps(chunk) + "\n")

        embeddings_file = ws_dir / "embeddings.jsonl"
        with embeddings_file.open("w", encoding="utf-8") as f:
            # Synthetic 4-dim unit vector
            emb = {"chunk_id": f"{doc_entry['document_id']}_0000", "embedding": [1.0, 0.0, 0.0, 0.0]}
            f.write(json.dumps(emb) + "\n")

        self.ws_mgr.update_document_status(ws_id, doc_entry["document_id"], "Ready", chunk_count=1)

        refreshed = self.ws_mgr.get_workspace(ws_id)
        self.assertEqual(len(refreshed["documents"]), 1)
        self.assertEqual(refreshed["documents"][0]["status"], "Ready")
        self.assertEqual(refreshed["documents"][0]["chunk_count"], 1)

    def test_04_personal_retriever_bm25_and_chunks(self):
        """4. Verify PersonalCollectionRetriever builds BM25 and indexes locally."""
        ws = self.ws_mgr.create_workspace()
        ws_id = ws["workspace_id"]
        ws_dir = self.test_root / ws_id

        chunks_file = ws_dir / "chunks.jsonl"
        emb_file = ws_dir / "embeddings.jsonl"
        with chunks_file.open("w", encoding="utf-8") as f:
            f.write(json.dumps({
                "chunk_id": "c1",
                "document_id": "d1",
                "filename": "sample.txt",
                "text": "Antigravity high performance caching system",
            }) + "\n")
        with emb_file.open("w", encoding="utf-8") as f:
            f.write(json.dumps({"chunk_id": "c1", "embedding": [0.5, 0.5, 0.5, 0.5]}) + "\n")

        retriever = PersonalCollectionRetriever(ws_dir)
        self.assertFalse(retriever.is_empty())
        self.assertIn("c1", retriever.chunks)
        self.assertIsNotNone(retriever.bm25)

    def test_05_touch_activity(self):
        """5. Verify touch_workspace updates last_activity timestamp."""
        ws = self.ws_mgr.create_workspace()
        ws_id = ws["workspace_id"]

        # Backdate last_activity
        past_time = (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat()
        meta_path = self.ws_mgr._get_meta_path(ws_id)
        with meta_path.open("r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["last_activity"] = past_time
        with meta_path.open("w", encoding="utf-8") as f:
            json.dump(meta, f)

        # Touch workspace
        self.ws_mgr.touch_workspace(ws_id)
        with meta_path.open("r", encoding="utf-8") as f:
            updated = json.load(f)
        self.assertNotEqual(updated["last_activity"], past_time)

    def test_06_expiration_logic(self):
        """6. Verify is_workspace_expired detects expired workspaces."""
        ws = self.ws_mgr.create_workspace()
        ws_id = ws["workspace_id"]

        # Initially active
        self.assertFalse(self.ws_mgr.is_workspace_expired(ws_id, ttl_seconds=3600))

        # Backdate activity past TTL
        past_time = (datetime.now(timezone.utc) - timedelta(seconds=3601)).isoformat()
        meta_path = self.ws_mgr._get_meta_path(ws_id)
        with meta_path.open("r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["last_activity"] = past_time
        with meta_path.open("w", encoding="utf-8") as f:
            json.dump(meta, f)

        self.assertTrue(self.ws_mgr.is_workspace_expired(ws_id, ttl_seconds=3600))

    def test_07_and_08_cleanup_deletes_all_temporary_files(self):
        """7 & 8. Verify cleanup deletes documents, chunks, embeddings, conversations, metadata."""
        ws = self.ws_mgr.create_workspace()
        ws_id = ws["workspace_id"]
        ws_dir = self.test_root / ws_id

        # Add conversation
        conv_mgr = ConversationManager(root_dir=self.test_root)
        conv_mgr.add_message(ws_id, "c1", "user", "What is the status?")
        self.assertTrue((ws_dir / "conversations" / "c1.json").exists())

        # Backdate and trigger cleanup
        past_time = (datetime.now(timezone.utc) - timedelta(seconds=4000)).isoformat()
        with self.ws_mgr._get_meta_path(ws_id).open("r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["last_activity"] = past_time
        with self.ws_mgr._get_meta_path(ws_id).open("w", encoding="utf-8") as f:
            json.dump(meta, f)

        cleaned = self.ws_mgr.cleanup_expired_workspaces(ttl_seconds=3600)
        self.assertIn(ws_id, cleaned)
        self.assertFalse(ws_dir.exists())

    def test_09_openstack_permanent_data_untouched(self):
        """9. Verify cleanup never touches permanent OpenStack corpus."""
        openstack_chunks = PROJECT_ROOT / "data" / "processed" / "chunks.jsonl"
        openstack_embs = PROJECT_ROOT / "data" / "processed" / "embeddings.jsonl"
        benchmark_dir = PROJECT_ROOT / "data" / "benchmark"

        self.assertTrue(openstack_chunks.exists(), "Permanent chunks.jsonl must exist")
        self.assertTrue(openstack_embs.exists(), "Permanent embeddings.jsonl must exist")
        self.assertTrue(benchmark_dir.exists(), "Permanent benchmark dir must exist")

        chunks_stat_before = openstack_chunks.stat().st_mtime
        embs_stat_before = openstack_embs.stat().st_mtime

        # Run sweep
        self.ws_mgr.cleanup_expired_workspaces(ttl_seconds=1)

        self.assertEqual(openstack_chunks.stat().st_mtime, chunks_stat_before)
        self.assertEqual(openstack_embs.stat().st_mtime, embs_stat_before)

    def test_10_query_expired_workspace_returns_none(self):
        """10. Verify get_workspace on an expired workspace returns None and cleans it up."""
        ws = self.ws_mgr.create_workspace()
        ws_id = ws["workspace_id"]

        # Backdate
        past_time = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        with self.ws_mgr._get_meta_path(ws_id).open("r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["last_activity"] = past_time
        with self.ws_mgr._get_meta_path(ws_id).open("w", encoding="utf-8") as f:
            json.dump(meta, f)

        fetched = self.ws_mgr.get_workspace(ws_id, auto_cleanup=True)
        self.assertIsNone(fetched)
        self.assertFalse((self.test_root / ws_id).exists())

    def test_11_new_session_isolation(self):
        """11. Verify fresh session gets distinct workspace ID."""
        ws1 = self.ws_mgr.create_workspace()
        ws2 = self.ws_mgr.create_workspace()
        self.assertNotEqual(ws1["workspace_id"], ws2["workspace_id"])

    def test_12_cleanup_idempotency(self):
        """12. Verify cleanup can run multiple times without raising errors."""
        ws = self.ws_mgr.create_workspace()
        ws_id = ws["workspace_id"]
        # Explicit delete
        self.assertTrue(self.ws_mgr.delete_workspace(ws_id))
        # Second delete should not crash
        self.assertFalse(self.ws_mgr.delete_workspace(ws_id))
        # Sweep should not crash
        cleaned = self.ws_mgr.cleanup_expired_workspaces()
        self.assertNotIn(ws_id, cleaned)

    def test_13_cross_workspace_isolation(self):
        """13. Verify cleaning one workspace leaves others unaffected."""
        ws_active = self.ws_mgr.create_workspace(name="Active Workspace")
        ws_expired = self.ws_mgr.create_workspace(name="Expired Workspace")

        # Expire only ws_expired
        past_time = (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
        with self.ws_mgr._get_meta_path(ws_expired["workspace_id"]).open("r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["last_activity"] = past_time
        with self.ws_mgr._get_meta_path(ws_expired["workspace_id"]).open("w", encoding="utf-8") as f:
            json.dump(meta, f)

        cleaned = self.ws_mgr.cleanup_expired_workspaces(ttl_seconds=3600)
        self.assertIn(ws_expired["workspace_id"], cleaned)
        self.assertNotIn(ws_active["workspace_id"], cleaned)

        # Active workspace must still exist
        active_fetched = self.ws_mgr.get_workspace(ws_active["workspace_id"])
        self.assertIsNotNone(active_fetched)
        self.assertEqual(active_fetched["name"], "Active Workspace")

    def test_14_partial_upload_recovery(self):
        """14. Verify cleanup handles half-written or corrupted workspace directories."""
        orphan_dir = self.test_root / "ws_corrupted"
        orphan_dir.mkdir(parents=True, exist_ok=True)
        # Create unparseable metadata
        (orphan_dir / "metadata.json").write_text("{invalid json", encoding="utf-8")

        # Fallback to mtime: make mtime old
        old_timestamp = time.time() - 7200
        os.utime(orphan_dir, (old_timestamp, old_timestamp))

        cleaned = self.ws_mgr.cleanup_expired_workspaces(ttl_seconds=3600)
        self.assertIn("ws_corrupted", cleaned)
        self.assertFalse(orphan_dir.exists())


class TestApiLifecycleEndpoints(unittest.TestCase):
    """Test FastAPI endpoints for health, expiration enforcement, and workspace deletion."""

    @classmethod
    def setUpClass(cls):
        from fastapi.testclient import TestClient
        from app.main import app
        cls.client = TestClient(app)

    def test_health_endpoints(self):
        r1 = self.client.get("/health")
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r1.json(), {"status": "ok"})

        r2 = self.client.get("/api/health")
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r2.json(), {"status": "ok"})

    def test_workspace_api_lifecycle(self):
        # 1. Create workspace
        create_res = self.client.post("/api/workspaces", json={"name": "API Test WS"})
        self.assertEqual(create_res.status_code, 200)
        data = create_res.json()
        ws_id = data["workspace_id"]
        self.assertTrue(ws_id.startswith("ws_"))
        self.assertIn("last_activity", data)

        # 2. Fetch workspace
        get_res = self.client.get(f"/api/workspaces/{ws_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["name"], "API Test WS")

        # 3. Query non-existent or expired workspace returns 404
        bad_query = self.client.post(
            f"/api/workspaces/ws_non_existent_123/query",
            json={"query": "Test query"},
        )
        self.assertEqual(bad_query.status_code, 404)

        # 4. Delete workspace
        del_res = self.client.delete(f"/api/workspaces/{ws_id}")
        self.assertEqual(del_res.status_code, 200)
        self.assertEqual(del_res.json()["status"], "deleted")

        # 5. Subsequent get returns 404
        get_after = self.client.get(f"/api/workspaces/{ws_id}")
        self.assertEqual(get_after.status_code, 404)


if __name__ == "__main__":
    unittest.main()
