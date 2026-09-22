# Advanced Hybrid RAG System

An evaluation-first, production-ready **Hybrid Retrieval-Augmented Generation (RAG)** platform. What started as a rigorously benchmarked, multi-stage retrieval experiment on OpenStack documentation has evolved into a full-stack, containerized application with ephemeral user workspaces, conversational follow-ups, strict source grounding, and dynamic latency optimizations.

---

## 📌 Executive Overview

Most RAG implementations stop at *"I embedded text into vectors and asked an LLM."* This system is built on rigorous measurement, failure analysis, and real-world system design:

1. **Multi-Stage Hybrid Retrieval**: Semantic search (Dense Vectors) fused with lexical search (BM25) via **Reciprocal Rank Fusion (RRF)**, followed by a **Cross-Encoder Neural Reranker** (`ms-marco-MiniLM-L-6-v2`) to pull exact evidence to rank 1.
2. **Evaluation-Driven Design**: Benchmarked against a frozen 100-question multi-hop test set, achieving a **+25% MRR@10 lift** and diagnosing exact candidate-recall ceilings.
3. **Full-Stack Application**: A FastAPI backend and modern React (Vite) frontend with drag-and-drop ingestion of `PDF`, `Markdown`, `TXT`, and `HTML`.
4. **Conversational Multi-Turn Contextualization**: Automatically rewrites ambiguous follow-up questions (e.g., *"What were the prerequisites for that?"*) into standalone queries before searching the index.
5. **Strictly Grounded Generation**: Answers synthesized by **Gemini 3.1 Pro** using strict prompt boundaries. All claims are backed by verifiable inline bracketed citations (`[1]`, `[2]`).
6. **Performance & Profiling**: Monotonic stage-level latency instrumentation allows for dynamic toggling of the heavy PyTorch Cross-Encoder (`ENABLE_RERANKER=false`) to maintain low latency on restricted cloud hardware.

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
 │   (Gemini 3.1 Pro with strict context sandbox│
 │       & inline citation verification)        │
 └────────────────────────┬─────────────────────┘
                          ▼
 ┌──────────────────────────────────────────────┐
 │   Interactive Answer + Clickable Citations   │
 └──────────────────────────────────────────────┘
```

---

## 📊 Version-Wise Evaluation & Benchmarks

The core retrieval architecture was iteratively developed and measured against a hand-verified, 100-question multi-hop benchmark over 141 OpenStack documents (1,495 chunks).

### Stage-by-Stage Progression

| Pipeline Stage | Any-Gold@10 | All-Gold@10 (Strict) | Coverage@10 | MRR@10 | Key Takeaway |
|---|:---:|:---:|:---:|:---:|---|
| **V1 Dense Baseline** | 77.9% | 61.1% | 69.8% | 0.533 | Strong semantic baseline; misses exact acronyms/IDs. |
| **V2-A BM25 (Lexical)** | 76.8% | 57.9% | 67.4% | 0.517 | Lower alone, but recovers 8 exact-term queries dense missed. |
| **V2-B Hybrid (RRF)** | 84.2% | 63.2% | 74.4% | 0.559 | Fuses rank positions; outperforms both parents across all metrics. |
| **V2-C Hybrid + Cross-Encoder**| **87.4%** | **68.4%** | **78.9%** | **0.665** | **+25% MRR lift**; cross-attention pulls exact answers to rank 1. |

> **Metric Definitions:**
> - **Any-Gold@10:** Finds *at least one* required gold chunk in the top 10.
> - **All-Gold@10 (Strict):** Finds *every single required gold chunk* in the top 10 (critical for multi-hop questions).
> - **MRR@10:** Mean Reciprocal Rank (how close to rank 1 the first correct chunk is).

### Failure Analysis: The Multi-Hop Recall Collapse
Our evaluation revealed that finding *some* relevant information isn't the primary challenge of RAG; **complete evidence retrieval is**. 
When comparing Single-Hop vs. Multi-Hop questions using our final V2-C architecture:

| Question Hop-Count | Any-Gold@10 (Finds 1 chunk) | All-Gold@10 (Finds ALL required chunks) |
|---|:---:|:---:|
| **1-Hop** | 90.0% | 90.0% |
| **2-Hop** | 80.0% | 40.0% |
| **3+-Hop** | 80.0% | 10.0% |

**Diagnostic Insight:** Out of 30 strict failures, 22 were candidate-recall ceilings. A single query vector points at one semantic region, meaning it reliably surfaces 1 or 2 hops but buries the rest outside the top 100. *This proves that single-vector candidate recall, not reranking depth, is the true bottleneck for complex reasoning in RAG systems.*

---

## ⚡ Core Engineering Features

- **Document Ingestion & Ephemeral Workspaces**:
  - Token-aware chunking (`tiktoken cl100k_base`, 500 tokens, 100 overlap).
  - Workspaces are ephemeral: isolated data indices automatically expire and are purged by a background `asyncio` TTL task.
- **Conversational Follow-Up Contextualizer**:
  - Tracks dialogue turns and detects pronouns or references (`"it"`, `"that"`, `"elaborate"`).
  - Automatically rewrites ambiguous questions into standalone queries before hitting the Jina embeddings API.
- **Strictly Grounded Synthesis**:
  - LLM prompt contracts treat retrieved documents as read-only data blocks (`<document>`), guarding against prompt injection.
  - Generates verifiable inline citations (`[1]`, `[2]`). Hallucinated or dangling citations are caught and logged.
- **Stage-Level Latency Instrumentation & Profiling**:
  - Every stage of the pipeline (Contextualization, Dense, BM25, RRF, Cross-Encoder, Gemini API) is profiled.
  - Dynamic CPU constraint gating via the `ENABLE_RERANKER=false` environment variable allows production environments to bypass heavy PyTorch Cross-Encoder inference when deployed to low-tier cloud instances, falling back safely to the fast RRF baseline.

---

## 🛠️ Technology Stack

- **Backend Architecture**: Python 3.10+, FastAPI, Uvicorn, Pydantic v2.
- **Retrieval Engine**: `jina-embeddings-v3` (Dense), `rank-bm25` (Sparse), Custom Reciprocal Rank Fusion ($k=60$).
- **Reranker**: PyTorch `sentence-transformers` (`cross-encoder/ms-marco-MiniLM-L-6-v2`).
- **Generation LLM**: Google Gemini 3.1 Pro API.
- **Frontend**: React 19, Vite, Framer Motion, Vanilla CSS Modules.
- **Deployment**: Docker, Render.

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
│   └── document_processor.py         # PDF / MD / TXT / HTML parser & chunker
│
├── src/                              # Benchmark & Offline Retrieval Engine
│   ├── ingestion/                    # OpenStack corpus chunker & loader
│   └── retrieval/                    # Retrieval stages (dense, bm25, hybrid, reranker, eval)
│
├── frontend/                         # React Frontend Application
│   ├── src/components/               # Header, Sidebar, Chat, Citations, EmptyState
│   └── src/lib/api.js                # API client with timeout & error handling
│
├── data/
│   ├── benchmark/                    # 100-question multi-hop benchmark & evaluations
│   └── user_documents/               # Active user workspaces, uploads, and indices
│
├── v1_report.md                      # Detailed V1 retrieval analysis
├── v2_report.md                      # Detailed V2 benchmark report
├── render.yaml                       # Render deployment configuration
└── Dockerfile                        # Multi-stage production container
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** & `npm`
- **Google Gemini API Key**
- **Jina API Key**

### 1. Environment Setup

```bash
git clone https://github.com/your-username/hybrid-rag.git
cd hybrid-rag
cp .env.example .env
```
Add your API keys to `.env`:
```ini
GOOGLE_API_KEY=your_gemini_api_key_here
JINA_API_KEY=your_jina_api_key_here
ENABLE_RERANKER=true
```

### 2. Backend Setup (FastAPI)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Frontend Setup (React + Vite)

```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## ☁️ Deployment to Render

This project is configured for deployment as a containerized web service via Docker. 

1. Connect your repository to Render.
2. Select **New Web Service** and deploy using the existing `render.yaml` or `Dockerfile`.
3. Set the following environment variables in your Render dashboard:
   - `JINA_API_KEY`
   - `GOOGLE_API_KEY`
   - `ENABLE_RERANKER` (Set to `false` if deploying on Render's Free/Starter tiers, which lack the CPU power for fast PyTorch neural inference).

*The Dockerfile builds both the Vite frontend and FastAPI backend into a unified image, downloading the Cross-Encoder weights at build time to prevent cold-start penalties.*

---

## 📄 License
This project is licensed under the MIT License.
