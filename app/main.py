"""
HYBRID-RAG FastAPI application.

Launch from the project root directory:

    uvicorn app.main:app --reload --port 8000

The working directory MUST be the project root so that the V2 retrieval
modules can resolve their relative data paths (data/processed/*, etc.).
"""
from __future__ import annotations

import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.collections_manager import (
    WORKSPACE_CLEANUP_INTERVAL_SECONDS,
    WorkspaceManager,
    sanitize_filename,
)
from app.document_processor import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_BYTES,
    process_and_index_document,
)
from app.conversation_manager import ConversationManager
from app.pipeline import run_query
from app.schemas import (
    ConversationDetail,
    DocumentItem,
    ErrorResponse,
    QueryRequest,
    QueryResponse,
    WorkspaceCreate,
    WorkspaceDetail,
    WorkspaceSummary,
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Environment & Workspace Manager
# ---------------------------------------------------------------------------

load_dotenv()
ws_mgr = WorkspaceManager()
coll_mgr = ws_mgr


def get_conv_mgr() -> ConversationManager:
    """Return a ConversationManager bound to the current WorkspaceManager root directory."""
    return ConversationManager(root_dir=ws_mgr.root_dir)


conv_mgr = get_conv_mgr()

# ---------------------------------------------------------------------------
# Lifespan — load retriever once at startup + background cleanup task
# ---------------------------------------------------------------------------

async def _periodic_cleanup():
    """
    Lightweight background task to periodically evict expired workspaces.
    Runs in a worker thread so it never blocks the async event loop.
    """
    while True:
        try:
            await asyncio.sleep(WORKSPACE_CLEANUP_INTERVAL_SECONDS)
            cleaned = await asyncio.to_thread(ws_mgr.cleanup_expired_workspaces)
            if cleaned:
                logger.info("Periodic cleanup removed %d expired workspace(s): %s", len(cleaned), cleaned)
        except asyncio.CancelledError:
            break
        except Exception as exc:
            logger.error("Error in background cleanup loop: %s", exc)


class _WorkspaceRerankerWrapper:
    """Lightweight wrapper holding the shared CrossEncoder neural model for user workspaces."""
    def __init__(self, model):
        self.model = model


def has_openstack_corpus() -> bool:
    """Check if the optional development benchmark corpus exists on local disk."""
    chunks_path = Path("data/processed/chunks.jsonl")
    embs_path = Path("data/processed/embeddings.jsonl")
    return chunks_path.exists() and embs_path.exists()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initializes the shared CrossEncoder neural reranker model once at startup.
    Reused across all dynamic user workspaces.
    If the optional local OpenStack benchmark corpus exists (development mode),
    it is loaded for benchmark evaluations; otherwise, the server starts cleanly
    in standalone product mode.
    """
    logger.info("Initializing neural cross-encoder model for workspace retrieval…")
    from sentence_transformers import CrossEncoder  # noqa: PLC0415
    from src.retrieval.reranker import RERANK_MODEL  # noqa: PLC0415

    cross_encoder = CrossEncoder(RERANK_MODEL)
    logger.info("Cross-encoder model '%s' loaded and ready in memory", RERANK_MODEL)

    if has_openstack_corpus():
        try:
            logger.info("Local OpenStack evaluation corpus detected — building benchmark retriever…")
            from src.retrieval.reranker import build_retriever  # noqa: PLC0415

            retriever, chunks = build_retriever()
            app.state.retriever = retriever
            app.state.chunks = chunks
            logger.info(
                "OpenStack benchmark retriever ready — %d chunks indexed",
                len(retriever.chunks),
            )
        except Exception as exc:
            logger.warning("Could not load local OpenStack evaluation corpus: %s", exc)
            app.state.retriever = _WorkspaceRerankerWrapper(cross_encoder)
            app.state.chunks = {}
    else:
        logger.info("Starting in standalone product mode (ephemeral user workspace retrieval ready)")
        app.state.retriever = _WorkspaceRerankerWrapper(cross_encoder)
        app.state.chunks = {}

    # Run initial cleanup sweep on startup
    await asyncio.to_thread(ws_mgr.cleanup_expired_workspaces)

    # Start non-blocking periodic background cleanup
    cleanup_task = asyncio.create_task(_periodic_cleanup())

    yield

    logger.info("Shutting down HYBRID-RAG")
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="HYBRID-RAG",
    description="Generic AI document assistant with grounded answers and citations.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Safe default app state for standalone testing where lifespan isn't explicitly entered
app.state.retriever = _WorkspaceRerankerWrapper(None)
app.state.chunks = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Query Routes
# ---------------------------------------------------------------------------

@app.post("/api/workspaces/{workspace_id}/query", response_model=QueryResponse)
@app.post("/api/query", response_model=QueryResponse)
@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest, request: Request, workspace_id: str | None = None):
    """
    Run RAG query against the isolated user workspace documents.
    """
    if not req.query.strip():
        raise HTTPException(status_code=422, detail="Query cannot be empty.")

    target_ws = workspace_id or req.workspace_id or req.collection_id or "default"

    # Enforce workspace expiration check for personal document workspaces
    if target_ws != "openstack":
        meta = ws_mgr.get_workspace(target_ws)
        if not meta:
            raise HTTPException(
                status_code=404,
                detail=f"Workspace '{target_ws}' has expired or does not exist.",
            )
        ws_mgr.touch_workspace(target_ws)

    try:
        result = run_query(
            query=req.query.strip(),
            retriever=request.app.state.retriever,
            chunks=request.app.state.chunks,
            workspace_id=target_ws,
            conversation_id=req.conversation_id,
            top_k=req.top_k,
            ws_mgr=ws_mgr,
        )
        return result
    except RuntimeError as exc:
        logger.error("Pipeline error: %s", exc)
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected error in query endpoint")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your query.",
        ) from exc


# ---------------------------------------------------------------------------
# Conversation History API
# ---------------------------------------------------------------------------

@app.get(
    "/api/workspaces/{workspace_id}/conversations/{conversation_id}",
    response_model=ConversationDetail,
)
async def get_conversation_endpoint(workspace_id: str = "default", conversation_id: str = "default"):
    """Fetch stored conversation thread and messages for a workspace session."""
    if not ws_mgr.get_workspace(workspace_id):
        raise HTTPException(
            status_code=404,
            detail=f"Workspace '{workspace_id}' has expired or does not exist.",
        )
    ws_mgr.touch_workspace(workspace_id)
    record = get_conv_mgr().get_conversation(workspace_id, conversation_id)
    if not record:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    return record


@app.delete("/api/workspaces/{workspace_id}/conversations/{conversation_id}")
async def delete_conversation_endpoint(workspace_id: str = "default", conversation_id: str = "default"):
    """Clear/delete a conversation session."""
    get_conv_mgr().delete_conversation(workspace_id, conversation_id)
    return {"status": "deleted", "conversation_id": conversation_id}


# ---------------------------------------------------------------------------
# Workspace API
# ---------------------------------------------------------------------------

@app.post("/api/workspaces", response_model=WorkspaceDetail)
@app.post("/api/collections", response_model=WorkspaceDetail)
async def create_workspace_endpoint(body: WorkspaceCreate):
    """Create a new document workspace."""
    meta = ws_mgr.create_workspace(name=body.name)
    return meta


@app.get("/api/workspaces", response_model=list[WorkspaceSummary])
@app.get("/api/collections", response_model=list[WorkspaceSummary])
async def list_workspaces_endpoint():
    """List all available workspaces."""
    return ws_mgr.list_workspaces()


@app.get("/api/workspace", response_model=WorkspaceDetail)
async def get_default_workspace_endpoint():
    """Get metadata and document list for the default workspace."""
    return ws_mgr.get_or_create_workspace("default")


@app.get("/api/workspaces/{workspace_id}", response_model=WorkspaceDetail)
@app.get("/api/collections/{collection_id}", response_model=WorkspaceDetail)
async def get_workspace_endpoint(workspace_id: str = "default", collection_id: str | None = None):
    """Get metadata and document list for a specific workspace."""
    target_id = collection_id or workspace_id
    if target_id == "default":
        meta = ws_mgr.get_workspace("default")
        if not meta:
            return ws_mgr.get_or_create_workspace("default")
        return meta
    meta = ws_mgr.get_workspace(target_id)
    if not meta:
        raise HTTPException(
            status_code=404,
            detail=f"Workspace '{target_id}' has expired or does not exist.",
        )
    return meta


@app.delete("/api/workspaces/{workspace_id}")
@app.delete("/api/collections/{collection_id}")
async def delete_workspace_endpoint(workspace_id: str = "default", collection_id: str | None = None):
    """Delete a workspace and all its temporary indexed data."""
    target_id = collection_id or workspace_id
    ok = ws_mgr.delete_workspace(target_id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Workspace '{target_id}' not found.")
    logger.info("workspace_cleanup_completed workspace_id=%s", target_id)
    return {"status": "deleted", "workspace_id": target_id}


# ---------------------------------------------------------------------------
# Documents Upload & Management API
# ---------------------------------------------------------------------------

@app.post("/api/workspaces/{workspace_id}/documents/upload")
@app.post("/api/workspace/documents/upload")
@app.post("/api/collections/{collection_id}/documents/upload")
async def upload_documents_endpoint(
    workspace_id: str = "default",
    collection_id: str | None = None,
    files: list[UploadFile] = File(...),
):
    """
    Upload one or more documents (PDF, Markdown, TXT, HTML) to a workspace.
    Validates file format and size, extracts text, chunks, embeds, and indexes.
    """
    target_id = collection_id or workspace_id
    meta = ws_mgr.get_workspace(target_id)
    if not meta:
        if target_id == "default":
            meta = ws_mgr.get_or_create_workspace(target_id)
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Workspace '{target_id}' has expired or does not exist.",
            )

    ws_dir = ws_mgr._get_ws_dir(target_id)
    results = []

    for file in files:
        filename = file.filename or "uploaded_document"
        ext = Path(filename).suffix.lower()

        # Validation 1: Format
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{ext}' for file '{filename}'. Supported formats: PDF, Markdown (.md), TXT, HTML.",
            )

        # Read content
        content = await file.read()

        # Validation 2: File size
        if len(content) > MAX_FILE_SIZE_BYTES:
            max_mb = MAX_FILE_SIZE_BYTES // (1024 * 1024)
            raise HTTPException(
                status_code=400,
                detail=f"File '{filename}' exceeds the maximum allowed size of {max_mb} MB.",
            )

        if len(content) == 0:
            raise HTTPException(
                status_code=400,
                detail=f"File '{filename}' is empty.",
            )

        # Save document file & record entry
        file_type = ext.lstrip(".")
        doc_entry = ws_mgr.save_document_file(
            workspace_id=target_id,
            filename=filename,
            content=content,
            file_type=file_type,
        )

        doc_id = doc_entry["document_id"]
        stored_name = doc_entry["stored_filename"]

        # Ingestion pipeline: Text extraction → Chunking → Embedding → Indexing
        try:
            ws_mgr.update_document_status(target_id, doc_id, "Indexing")
            chunk_count = process_and_index_document(
                coll_dir=ws_dir,
                document_id=doc_id,
                stored_filename=stored_name,
                display_filename=doc_entry["filename"],
            )
            ws_mgr.update_document_status(target_id, doc_id, "Ready", chunk_count=chunk_count)
            doc_entry["status"] = "Ready"
            doc_entry["chunk_count"] = chunk_count
        except Exception as exc:
            logger.exception("Failed to process document %s (%s)", doc_id, filename)
            ws_mgr.update_document_status(target_id, doc_id, "Failed", error=str(exc))
            doc_entry["status"] = "Failed"
            doc_entry["error"] = str(exc)

        results.append(doc_entry)

    # Touch workspace activity after upload
    ws_mgr.touch_workspace(target_id)
    return {"uploaded": results}


@app.get("/api/workspaces/{workspace_id}/documents", response_model=list[DocumentItem])
@app.get("/api/workspace/documents", response_model=list[DocumentItem])
@app.get("/api/collections/{collection_id}/documents", response_model=list[DocumentItem])
async def list_documents_endpoint(workspace_id: str = "default", collection_id: str | None = None):
    """List all documents in a workspace."""
    target_id = collection_id or workspace_id
    meta = ws_mgr.get_workspace(target_id)
    if not meta:
        if target_id == "default":
            meta = ws_mgr.get_or_create_workspace(target_id)
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Workspace '{target_id}' has expired or does not exist.",
            )
    return meta.get("documents", [])


@app.delete("/api/workspaces/{workspace_id}/documents/{document_id}")
@app.delete("/api/workspace/documents/{document_id}")
@app.delete("/api/collections/{collection_id}/documents/{document_id}")
async def delete_document_endpoint(
    document_id: str,
    workspace_id: str = "default",
    collection_id: str | None = None,
):
    """
    Delete a document from a workspace and remove its chunks and embeddings from the index.
    """
    target_id = collection_id or workspace_id
    if not ws_mgr.get_workspace(target_id):
        raise HTTPException(
            status_code=404,
            detail=f"Workspace '{target_id}' has expired or does not exist.",
        )
    ok = ws_mgr.delete_document(target_id, document_id)
    if not ok:
        raise HTTPException(
            status_code=404,
            detail=f"Document '{document_id}' not found in workspace '{target_id}'.",
        )
    ws_mgr.touch_workspace(target_id)
    return {"status": "deleted", "document_id": document_id}


@app.get("/health")
@app.get("/api/health")
async def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Custom error handler
# ---------------------------------------------------------------------------

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=f"HTTP {exc.status_code}",
            detail=exc.detail,
        ).model_dump(),
    )


# ---------------------------------------------------------------------------
# Static files — frontend served last so API routes take precedence
# ---------------------------------------------------------------------------

FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")
elif FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
else:
    logger.warning("Neither frontend/dist nor frontend/ directory found — UI will not be served")


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
