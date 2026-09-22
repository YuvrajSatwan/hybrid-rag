# HYBRID-RAG

An evaluation-first, production-ready **Hybrid Retrieval-Augmented Generation (RAG)** platform featuring a two-stage retrieval engine (Dense + BM25 + Cross-Encoder Reranking), dynamic multi-format document ingestion, conversational follow-ups, and a modern React web interface with strict source grounding.

---

## 📌 Overview

Most RAG implementations stop at *"I embedded text into vectors and asked an LLM."* **HYBRID-RAG** is built on rigorous retrieval measurement and real-world system design:

1. **Measured Two-Stage Retrieval**: Dense vector search captures semantic intent; BM25 captures exact identifiers and keywords. They are fused using **Reciprocal Rank Fusion (RRF)** and reranked using a **Cross-Encoder neural model** (`ms-marco-MiniLM-L-6-v2`).
2. **Document Ingestion & Workspace Isolation**: Upload and index your own documents (`PDF`, `Markdown`, `TXT`, `HTML`). Text is extracted, token-chunked, embedded, and stored with strict workspace isolation.
3. **Conversational Multi-Turn Follow-Ups**: The built-in **Query Contextualizer** inspects chat history to rewrite ambiguous questions (e.g., *"What were the prerequisites for that?"* or *"Tell me about the second project"*) into standalone retrieval queries without polluting unrelated topics.
4. **Strictly Grounded Generation**: Answers are synthesized using Google Gemini with strict prompt boundaries. All claims are backed by verifiable inline bracketed citations (`[1]`, `[2]`), complete with chunk snippets, section headers, and page numbers.
5. **Rigorous 100-Question Benchmark**: Evaluated against a frozen, hand-verified 100-question multi-hop benchmark over 141 OpenStack documents, achieving **+25% MRR@10 lift** and diagnosing exact candidate-recall ceilings.

> **Note on Evaluation Assets vs. Product**:
> OpenStack was used as the fixed evaluation corpus during development to measure and validate the retrieval architecture. The raw corpus and generated indexes are intentionally not included in the public repository or production deployments. The deployed application instead dynamically supports user-provided documents with ephemeral, temporary session workspaces.

---

## 🏗️ Architecture

```
                               ┌──────────────────────────────────────────────┐
                               │             USER DOCUMENTS                   │
                               │  (PDF, Markdown, TXT, HTML)                  │
                               └──────────────────────┬───────────────────────┘
                                                      │
                                                      ▼ Ingestion
                                      ┌───────────────────────────────┐
                                      │   Structure-Aware Token       │
                                      │   Chunking (tiktoken cl100k)  │
                                      └───────────────┬───────────────┘
                                                      ▼
                                      ┌───────────────────────────────┐
                                      │ Jina v3 Embeddings & BM25     │
                                      │ Per-Workspace Indexing        │
                                      └───────────────┬───────────────┘
                                                      │
 ┌─────────────────────────┐                          │
 │ User Question / Chat    │                          │
 └────────────┬────────────┘                          │
              ▼                                       │
 ┌─────────────────────────┐                          │
 │  Query Contextualizer   │                          │
 │ (Rewrites follow-ups    │                          │
 │  based on conversation) │                          │
 └────────────┬────────────┘                          │
              ▼ Standalone Query                      │
 ┌──────────────────────────────────────────────┐     │
 │            TWO-STAGE RETRIEVAL ENGINE        │     │
 │                                              │     │
 │   ┌─────────────────┐   ┌────────────────┐   │     │
 │   │  Dense Cosine   │   │  Okapi BM25    │   │     │
 │   │    (Top 100)    │   │   (Top 100)    │   │     │
 │   └────────┬────────┘   └────────┬───────┘   │     │
 │            └───────────┬─────────┘           │◄────┘
 │                        ▼                     │
 │             Reciprocal Rank Fusion           │
 │                  (Top 30)                    │
 │                        ▼                     │
 │          Cross-Encoder Neural Rerank         │
 │          (ms-marco-MiniLM-L-6-v2)            │
 │                        ▼                     │
 │                 Top 5 - 10 Chunks            │
 └────────────────────────┬─────────────────────┘
                          ▼
 ┌──────────────────────────────────────────────┐
 │         GROUNDED ANSWER GENERATION           │
 │     (Gemini with strict context sandbox      │
 │       & inline citation verification)        │
 └────────────────────────┬─────────────────────┘
                          ▼
 ┌──────────────────────────────────────────────┐
 │   Interactive Answer + Clickable Citations   │
 └──────────────────────────────────────────────┘
```

---

## 📊 Benchmark & Key Findings

We systematically evaluated single-stage dense retrieval against multi-stage hybrid retrieval using a frozen 100-question benchmark with hand-verified gold chunk sets:

### 1. The Multi-Hop Recall Collapse
Dense retrieval alone finds *at least one* relevant chunk reliably, but collapses when a question requires *multiple distinct pieces of evidence*:

| Question Requirement | Single-Hop (1 chunk) | Two-Hop (2 chunks) | Multi-Hop (3+ chunks) |
|---|:---:|:---:|:---:|
| **Any-Gold@10** *(Finds at least one)* | 78.0% | 76.0% | 80.0% |
| **All-Gold@10** *(Finds all required)* | **78.0%** | **36.0%** | **20.0%** |

### 2. Stage-by-Stage Progression (V1 → V2)

| Pipeline Stage | Any-Gold@10 | All-Gold@10 (Strict) | Coverage@10 | MRR@10 | Key Takeaway |
|---|:---:|:---:|:---:|:---:|---|
| **V1 Dense** (`jina-embeddings-v3`) | 77.9% | 61.1% | 69.8% | 0.533 | Strong semantic baseline; misses exact acronyms/IDs. |
| **V2-A BM25** (Lexical) | 76.8% | 57.9% | 67.4% | 0.517 | Lower alone, but recovers 8 exact-term queries dense missed. |
| **V2-B Hybrid** (Dense + BM25, RRF) | 84.2% | 63.2% | 74.4% | 0.559 | Fuses rank positions; outperforms both parents across all metrics. |
| **V2-C Hybrid + Cross-Encoder** | **87.4%** | **68.4%** | **78.9%** | **0.665** | **+25% MRR lift**; cross-attention pulls exact answers to rank 1. |

> **Diagnostic Insight**: Cross-encoder reranking dramatically improves precision and top-1 ranking. However, for 3+-hop questions, **22 of 30 failures were candidate-recall ceilings** (the required chunk was never in the initial top-30 pool). This proves that single-vector candidate recall, not reranking, is the true bottleneck for complex reasoning.

---

## ⚡ Core Features

- **Document Ingestion Engine**:
  - Drag-and-drop file upload for **PDF, Markdown (.md), TXT, and HTML**.
  - Token-aware chunking (500 tokens, 100 token overlap) preserving paragraph and section integrity.
  - Automatic workspace directories under `data/user_documents/<workspace_id>/` with independent chunk indices.
- **Conversational Follow-Up Contextualizer**:
  - Tracks dialogue turns and detects pronouns or references (`"it"`, `"that"`, `"the second one"`, `"elaborate"`).
  - Automatically rewrites ambiguous questions into standalone queries before searching the index.
  - Leaves standalone questions and topic switches untouched to prevent query contamination.
- **Strictly Grounded Synthesis**:
  - LLM prompt contracts treat retrieved documents as read-only data blocks (`<document>`), guarding against prompt injection.
  - Generates verifiable inline citations (`[1]`, `[2]`). Hallucinated or dangling citations are detected and flagged.
- **Modern Web Interface**:
  - React + Vite application with dark/light themes.
  - Live document management sidebar with optimistic upload progress.
  - Interactive citation chips that highlight source excerpts, document name, and page numbers on click.

---

## 📁 Repository Structure

```
hybrid-rag/
├── app/                              # FastAPI Backend Application
│   ├── main.py                       # REST API endpoints & server lifecycle
│   ├── pipeline.py                   # Orchestration: Contextualize → Retrieve → Generate
│   ├── generator.py                  # Grounded LLM generation & citation extraction
│   ├── contextualizer.py             # Multi-turn conversational query rewriting
│   ├── collections_manager.py        # Workspace & user document storage manager
│   ├── personal_retriever.py         # Dynamic per-workspace hybrid search engine
│   ├── document_processor.py         # PDF / MD / TXT / HTML parser & chunker
│   ├── conversation_manager.py       # Session persistence
│   └── schemas.py                    # Pydantic request / response contracts
│
├── src/                              # Benchmark & Offline Retrieval Engine
│   ├── ingestion/                    # OpenStack corpus chunker & loader
│   └── retrieval/                    # Retrieval stages (dense, bm25, hybrid, reranker, eval)
│
├── frontend/                         # React Frontend Application
│   ├── src/
│   │   ├── components/               # Header, Sidebar, Chat, Citations, EmptyState
│   │   ├── lib/api.js                # API client with timeout & error handling
│   │   ├── App.jsx                   # Main application state & polling
│   │   └── index.css                 # Global design system & theme variables
│   ├── package.json
│   └── vite.config.js
│
├── data/
│   ├── benchmark/                    # 100-question multi-hop benchmark & evaluations
│   ├── processed/                    # Pre-indexed OpenStack corpus (1,495 chunks)
│   └── user_documents/               # Active user workspaces, uploads, and indices
│
├── docs/                             # Engineering design records & interview notes
├── requirements.txt                  # Backend Python dependencies
├── v1_report.md                      # Detailed V1 retrieval analysis
└── v2_report.md                      # Detailed V2 benchmark report
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** & `npm`
- **Google Gemini API Key** (for generation and conversational contextualization)
- *(Optional)* **Jina API Key** (for embedding custom user documents or queries not in the offline cache)

---

### 1. Environment Setup

Clone the repository and create your `.env` configuration in the project root:

```bash
# Clone the repository
git clone https://github.com/your-username/hybrid-rag.git
cd hybrid-rag

# Create environment configuration
cp .env.example .env
```

Add your API keys to `.env`:

```ini
GOOGLE_API_KEY=your_gemini_api_key_here
JINA_API_KEY=your_jina_api_key_here
```

---

### 2. Backend Setup (FastAPI)

Create a Python virtual environment, install dependencies, and start the Uvicorn server:

```bash
# Create and activate virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at `http://127.0.0.1:8000` with interactive Swagger docs at `http://127.0.0.1:8000/docs`.

---

### 3. Frontend Setup (React + Vite)

In a new terminal window:

```bash
cd frontend

# Install packages
npm install

# Start Vite development server
npm run dev
```

Open `http://localhost:5173` in your browser.

---

### 4. Running the Retrieval Benchmark

To run the standalone benchmark evaluations against the frozen 100-question test set:

```bash
# Evaluate BM25 Lexical Baseline (V2-A)
python -m src.retrieval.bm25

# Evaluate Hybrid Dense + BM25 with RRF (V2-B)
python -m src.retrieval.hybrid

# Evaluate Two-Stage Hybrid + Cross-Encoder Reranker (V2-C)
python -m src.retrieval.reranker
```

Results and failure analysis will be printed to stdout and saved under `data/benchmark/evaluation/`.

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/workspaces/{workspace_id}/query` | Ask a question against indexed documents with conversational follow-up support. |
| `POST` | `/api/workspaces/{workspace_id}/documents/upload` | Upload and index documents (`multipart/form-data`: PDF, MD, TXT, HTML). |
| `GET` | `/api/workspaces/{workspace_id}` | Fetch workspace metadata, document status, chunk counts, and timestamps. |
| `DELETE` | `/api/workspaces/{workspace_id}/documents/{document_id}` | Remove a document and prune its chunks and embeddings from the index. |
| `GET` | `/api/workspaces/{workspace_id}/conversations/{conv_id}` | Retrieve stored conversation history. |
| `DELETE` | `/api/workspaces/{workspace_id}/conversations/{conv_id}` | Clear conversation history. |
| `GET` | `/api/health` | Health check endpoint returning index size and system status. |

---

## 🛠️ Technology Stack

- **Backend**: FastAPI, Uvicorn, Pydantic v2, Python 3.10+
- **Retrieval & Reranking**: 
  - `rank-bm25` (Okapi BM25)
  - `sentence-transformers` (`cross-encoder/ms-marco-MiniLM-L-6-v2`)
  - `jina-embeddings-v3` (Dense semantic search)
  - Custom Reciprocal Rank Fusion (RRF, $k=60$)
- **Document Ingestion**: `pypdf`, `tiktoken` (`cl100k_base` token-aware chunking)
- **Generation & LLM**: Google Gemini API (`gemini-3.5-flash-lite`), strict zero-shot citation prompt
- **Frontend**: React 19, Vite, Vanilla CSS Modules, Framer Motion

---

---

## ⏳ Temporary Workspace Data & Ephemeral Storage

HYBRID-RAG treats user-uploaded documents and conversations as **ephemeral session data**, rather than permanent cloud storage:

```
Session Starts  ──►  Workspace Created  ──►  Upload Documents  ──►  Chunks / Embeddings / BM25 Indexed
                                                                              │
                                                                              ▼
Workspace Purged  ◄──  Server Cleanup Sweep  ◄──  TTL Expired  ◄──  Q&A / Conversation
```

- **Session Scoping**: Uploaded documents (`PDF`, `Markdown`, `TXT`, `HTML`), extracted text, chunks, vector embeddings, in-memory BM25 indices, and multi-turn conversation logs are isolated strictly under `data/user_documents/<workspace_id>/`.
- **Automatic TTL Expiration**: Inactive workspaces automatically expire after `WORKSPACE_TTL_SECONDS` (default: `3600` seconds / 1 hour). The TTL is configurable via an environment variable.
- **Server-Side Cleanup**: A non-blocking periodic background task (and opportunistic request-time sweep) automatically purges all temporary files, indices, and conversation history for expired workspaces.
- **Client Session Lifecycle**: The frontend uses browser `sessionStorage` for workspace and conversation identifiers. Closing the browser tab terminates the session identity; refreshing an active page preserves it. If a session expires on the server, the frontend cleanly reinitializes a fresh workspace.
- **Explicit "New Session" Action**: Users can click "New Session" in the header to immediately wipe the current workspace on the backend and start fresh.
- **Permanent Corpus Isolation**: The reference OpenStack benchmark corpus (`data/processed/`, `data/benchmark/`, `data/metadata/`, `data/raw/`) is read-only, separate, and never touched or modified by user workspace cleanup sweeps.
- **Privacy Notice**: This demonstration application does not retain user-uploaded files indefinitely and is not intended for long-term document archival.

---

## 🚀 Deployment to Render

HYBRID-RAG is configured for seamless deployment as two separate, isolated Render services:

### 1. Backend: Render Web Service
- **Service Type**: Web Service
- **Runtime**: Python 3.11
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path**: `/api/health`
- **Environment Variables**:
  - `WORKSPACE_TTL_SECONDS`: `3600` (optional, default: 3600)
  - `WORKSPACE_CLEANUP_INTERVAL_SECONDS`: `60` (optional, default: 60)
  - `JINA_API_KEY`: Your Jina AI API key
  - `GOOGLE_API_KEY`: Your Google Gemini API key

> Alternatively, deploy using the included [Dockerfile](file:///y:/AI%20Eng%20Stuff/Projects/SIMPLE-RAG/Dockerfile), which pre-downloads the cross-encoder model and installs CPU-only PyTorch for fast builds and cold-start prevention.

### 2. Frontend: Render Static Site
- **Service Type**: Static Site
- **Root Directory**: `frontend`
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `dist`
- **Rewrite / Redirect Rules**:
  - **Type**: Rewrite
  - **Source**: `/*`
  - **Destination**: `/index.html` (Single-Page Application fallback)
- **Environment Variables**:
  - `VITE_API_BASE_URL`: `https://<your-backend-service>.onrender.com` (URL of deployed backend Web Service)

---

## 📄 License

This project is licensed under the MIT License.

