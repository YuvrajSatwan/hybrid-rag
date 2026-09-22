"""
Pydantic models for the HYBRID-RAG API.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    workspace_id: str | None = Field(default="default")
    collection_id: str | None = Field(default=None)
    conversation_id: str | None = Field(default=None)
    top_k: int = Field(default=10, ge=1, le=20)


class Citation(BaseModel):
    chunk_id: str
    title: str = ""
    service: str | None = None
    source_url: str = ""
    snippet: str  # first ~250 chars of chunk text
    page: int | None = None
    filename: str | None = None
    section: str | None = None


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    latency_ms: float
    workspace_id: str | None = "default"
    collection_id: str | None = None
    conversation_id: str | None = "default"


class ConversationMessage(BaseModel):
    id: str
    role: str
    content: str
    citations: list[Citation] = []
    timestamp: str
    latency_ms: float | None = None


class ConversationDetail(BaseModel):
    conversation_id: str
    workspace_id: str
    created_at: str | None = None
    updated_at: str
    messages: list[ConversationMessage]


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None


# --- Workspace & Documents Schemas ---

class WorkspaceCreate(BaseModel):
    name: str = Field(default="My Documents", min_length=1, max_length=100)


class DocumentItem(BaseModel):
    document_id: str
    filename: str
    file_type: str
    file_size: int
    uploaded_at: str
    status: str
    chunk_count: int = 0
    error: str | None = None


class WorkspaceSummary(BaseModel):
    workspace_id: str
    name: str
    created_at: str
    last_activity: str | None = None
    document_count: int = 0


class WorkspaceDetail(BaseModel):
    workspace_id: str
    name: str
    created_at: str
    last_activity: str | None = None
    documents: list[DocumentItem]


# Aliases for backward compatibility
CollectionCreate = WorkspaceCreate
CollectionSummary = WorkspaceSummary
CollectionDetail = WorkspaceDetail

