# Knowledge Intelligence System

> A production-grade Retrieval-Augmented Generation (RAG) pipeline for multi-format document ingestion, semantic search, and conversational question answering — backed by a persistent vector store, MongoDB audit layer, and full MLflow experiment tracking.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Installation](#installation)
- [Pipeline Phases](#pipeline-phases)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Experiment Tracking](#experiment-tracking)
- [Data Persistence](#data-persistence)
- [Production Readiness Checklist](#production-readiness-checklist)
- [Export and Checkpointing](#export-and-checkpointing)
- [Configuration Reference](#configuration-reference)
- [Supported Document Formats](#supported-document-formats)
- [Troubleshooting](#troubleshooting)
- [Credentials Reference](#credentials-reference)

---

## Overview

The **Knowledge Intelligence System (KIS)** is an end-to-end RAG pipeline designed for production deployment. It ingests heterogeneous document corpora, indexes them in a persistent FAISS vector store using HuggingFace sentence embeddings, and exposes a conversational Q&A interface powered by Groq's `llama-3.1` model family via LangChain.

Every query and ingestion event is audited in MongoDB with automatic TTL-based expiration, and all experiment parameters and metrics are tracked in MLflow — optionally backed by a DagsHub remote tracking server.

The system is designed for **graceful degradation**: if MongoDB or MLflow are unavailable, the core ingestion and Q&A pipeline continues to operate in offline mode without interruption.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Knowledge Intelligence System                 │
│                                                                   │
│   Documents (PDF / TXT / MD)                                      │
│          │                                                        │
│          ▼                                                        │
│   ┌─────────────────┐     ┌──────────────────────────────┐       │
│   │ DocumentProcessor│────▶│  FAISS Vector Store           │       │
│   │ (Chunking/Split) │     │  (HuggingFace Embeddings)     │       │
│   └─────────────────┘     └──────────────┬───────────────┘       │
│                                           │ Retrieval             │
│   User Query ─────────────────────────────▼                       │
│                            ┌──────────────────────────────┐       │
│                            │  LLM Service (Groq / llama)  │       │
│                            │  RAG Chain (LangChain 1.2+)  │       │
│                            └──────────────┬───────────────┘       │
│                                           │                       │
│         ┌─────────────────────────────────┤                       │
│         ▼                                 ▼                       │
│   ┌───────────┐                   ┌───────────────┐               │
│   │  MongoDB  │                   │    MLflow     │               │
│   │ (Audit /  │                   │  (Tracking /  │               │
│   │  History) │                   │   Metrics)    │               │
│   └───────────┘                   └───────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| LLM Backend | Groq API — `llama-3.1-70b-versatile` / `llama-3.1-8b-instant` |
| Orchestration | LangChain ≥ 1.2 (`langchain-core`, `langchain-community`, `langchain-groq`) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` via HuggingFace |
| Vector Store | FAISS (local persistent index) |
| Document Loading | LangChain `PyPDFLoader`, `TextLoader` |
| Text Splitting | `RecursiveCharacterTextSplitter` |
| Metadata & Audit | MongoDB Atlas via `pymongo` |
| Experiment Tracking | MLflow + DagsHub remote (optional local `file://` backend) |
| Configuration | Python `dataclasses` + environment variables |
| Runtime | Python 3.10+ |

---

## Project Structure

```
project/
├── app/
│   ├── config.py                   # SystemConfig dataclass
│   ├── models/
│   │   ├── __init__.py
│   │   └── vector_store.py         # FAISS wrapper with persistence
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_processor.py   # Document loading and chunking
│   │   └── llm_service.py          # Groq RAG chain
│   └── utils/
│       └── __init__.py
├── data/                           # Sample / input documents
├── outputs/                        # Query results (JSON)
├── checkpoints/                    # System state snapshots
├── logs/                           # Operational event logs
├── vector_db/                      # Persisted FAISS index
├── requirements.txt
└── README.md
```

---

## Prerequisites

- Python 3.10 or higher
- A [Groq API key](https://console.groq.com) (free tier available)
- A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) connection string (optional — system operates without it)
- A [DagsHub](https://dagshub.com) account with an MLflow tracking server (optional — falls back to local `file://` storage)

---

## Environment Configuration

All credentials are loaded from environment variables. Create a `.env` file in the project root or export them directly in your shell:

```bash
# Required
export GROQ_API_KEY="gsk_..."

# Optional — system operates in offline mode without these
export MONGO_DB_URL="mongodb+srv://user:password@cluster.mongodb.net/"

# Optional — falls back to local file-based MLflow if not set
export MLFLOW_TRACKING_URI="https://dagshub.com/<username>/<repo>.mlflow"
export MLFLOW_TRACKING_USERNAME="<dagshub_username>"
export MLFLOW_TRACKING_PASSWORD="<dagshub_token>"

# Optional — defaults to ./vector_db
export VECTOR_DB_PATH="vector_db"
```

> **Security note:** Credentials are never logged in plaintext. The `SystemConfig.safe_dict()` method masks all sensitive fields before any logging or serialisation call.

---

## Installation

```bash
git clone https://github.com/<your-org>/knowledge-intelligence-system.git
cd knowledge-intelligence-system

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### `requirements.txt`

```
langchain
langchain-core
langchain-community
langchain-groq
langchain-text-splitters
faiss-cpu
sentence-transformers
pypdf
pymongo
pandas
numpy
tqdm
mlflow
pydantic
```

---

## Pipeline Phases

The system is organised into discrete, independently testable phases:

| Phase | Name | Responsibility |
|---|---|---|
| 0 | Environment & Secrets | Load credentials; configure MLflow backend |
| 1 | Dependency Installation | Validate and install all required packages |
| 2 | Configuration & Logging | Instantiate `SystemConfig`; initialise coloured logger |
| 3 | Vector Store | Build or load FAISS index; configure HuggingFace embeddings |
| 4 | Document Processor | Load PDF / TXT / MD files; split into overlapping chunks |
| 5 | LLM Service | Construct conversational RAG chain over Groq `llama-3.1` |
| 6 | MongoDB Integration | Persist document metadata, query history, and system events |
| 7 | MLflow Tracking | Log parameters, latency metrics, and run artifacts |
| 8 | Orchestrator | `KnowledgeSystem` facade — single entry point for ingest and query |
| 9 | Demo: Ingest & Query | Create sample documents, ingest, and execute test queries |
| 10 | Checkpoint & Export | Snapshot system state; export results JSON; generate ZIP archive |
| 11 | Production Readiness | Automated 7-point health check across all system components |

---

## Quick Start

```python
from app.config import SystemConfig
from app.models.vector_store import VectorStore
from app.services.document_processor import DocumentProcessor
from app.services.llm_service import LLMService

# Initialise
cfg          = SystemConfig.from_env()
doc_proc     = DocumentProcessor(cfg)
vector_store = VectorStore(cfg)

# Ingest a document
chunks = doc_proc.process("data/my_report.pdf")
vector_store.add_documents(chunks)

# Query
llm_svc = LLMService(vector_store, cfg)
result  = llm_svc.ask("What are the key findings?")

print(result["answer"])
print(f"Latency: {result['duration_s']}s")
```

---

## API Reference

### `KnowledgeSystem`

High-level orchestration facade. Wires all services together and provides a three-method public API.

#### `ks.ingest(path: str) -> dict`

Load, chunk, embed, and index a document. Also persists metadata to MongoDB and logs ingestion metrics to MLflow.

```python
result = ks.ingest("data/research_paper.pdf")
# {
#   "status": "ok",
#   "file": "research_paper.pdf",
#   "chunks": 42,
#   "duration_s": 3.14,
#   "ts": "2025-01-01T12:00:00"
# }
```

#### `ks.query(question: str) -> dict`

Retrieve semantically relevant chunks and generate a grounded answer. Appends the exchange to MongoDB query history.

```python
result = ks.query("What methodology was used?")
# {
#   "answer": "...",
#   "model": "llama-3.1-8b-instant",
#   "duration_s": 0.82
# }
```

#### `ks.status() -> dict`

Return a live health snapshot of all subsystems.

```python
status = ks.status()
# {
#   "vector_store": {"doc_count": 120},
#   "memory": {"turns": 3},
#   "mongodb": {"documents": 5, "queries": 23, "logs": 41},
#   "ts": "2025-01-01T12:00:00"
# }
```

### `VectorStore`

| Method | Signature | Description |
|---|---|---|
| `add_documents` | `(docs: List[Document]) -> dict` | Batch-ingest chunks and persist the index |
| `similarity_search` | `(query: str, k: int = None) -> List[Document]` | Top-k semantic retrieval |
| `as_retriever` | `() -> Retriever` | LangChain-compatible retriever interface |
| `stats` | `() -> dict` | Returns `{doc_count: int}` |

### `DocumentProcessor`

| Method | Signature | Description |
|---|---|---|
| `process` | `(path: str) -> List[Document]` | Load and split a document into chunks |

---

## Experiment Tracking

MLflow tracks every ingestion and query run. The following are logged automatically:

**Parameters (at run start)**

- `model_name`
- `embedding_model`
- `chunk_size`, `chunk_overlap`
- `similarity_k`
- `temperature`, `max_tokens`

**Metrics (per operation)**

- `ingest_chunks` — number of chunks created
- `ingest_duration_s` — ingestion wall-clock time
- `query_duration_s` — end-to-end query latency
- `memory_turns` — number of turns in the active conversation

To view experiments locally:

```bash
mlflow ui --backend-store-uri file://./mlruns
# Open http://localhost:5000
```

To disable remote tracking and use a local backend:

```python
USE_DAGSHUB = False  # in the environment setup phase
```

---

## Data Persistence

### Vector Store

The FAISS index is persisted to `./vector_db/` after every `add_documents` call. On subsequent runs the index is automatically loaded from disk — no re-ingestion required.

### MongoDB Collections

| Collection | Purpose | TTL |
|---|---|---|
| `documents` | One record per ingested file (upsert on filename) | None — permanent |
| `queries` | Full question / answer history with latency | 30 days |
| `system_logs` | Operational events (startup, errors, health checks) | 7 days |

TTL indexes are created automatically on first connection. All MongoDB operations fail silently and return `False` when the database is unreachable — the pipeline continues in offline mode.

---

## Production Readiness Checklist

An automated 7-point checklist is available via `run_checklist()`:

```
══════════════════════════════════════════════
🔍  PRODUCTION READINESS CHECKLIST
══════════════════════════════════════════════
  ✅  Groq API key
  ✅  MongoDB URL
  ✅  Vector Store (120 docs)
  ✅  LLM (llama-3.1-8b-instant)
  ✅  MongoDB (online)
  ✅  MLflow Tracking URI
  ✅  Filesystem write
  ✅  Disk space (18.4 GB free)
──────────────────────────────────────────────
Result: 🟢 READY  (8/8 checks passed)
══════════════════════════════════════════════
```

Grades: `🟢 READY` (all pass) · `🟡 PARTIAL` (≥ 5 pass) · `🔴 ISSUES` (< 5 pass)

---

## Export and Checkpointing

**Checkpoint** (JSON snapshot of config + system state):

```
checkpoints/ckpt_YYYYMMDD_HHMMSS.json
```

**Query results** (JSON array of all Q&A responses):

```
outputs/query_results.json
outputs/real_pdf_query_results.json
```

**Full project archive** (ZIP containing all source files, outputs, checkpoints, logs, and data):

```bash
# Generated automatically by Phase 10
knowledge_system_export.zip
```

---

## Configuration Reference

All options are available on the `SystemConfig` dataclass and can be overridden via environment variables or direct instantiation.

| Parameter | Default | Description |
|---|---|---|
| `vector_db_path` | `"vector_db"` | Local path for FAISS index persistence |
| `mongo_db_url` | `""` | MongoDB connection string |
| `groq_api_key` | `""` | Groq API key |
| `model_name` | `"llama-3.1-8b-instant"` | Groq model identifier |
| `embedding_model` | `"sentence-transformers/all-MiniLM-L6-v2"` | HuggingFace embedding model |
| `chunk_size` | `1000` | Maximum characters per document chunk |
| `chunk_overlap` | `200` | Overlap between consecutive chunks (characters) |
| `similarity_k` | `4` | Number of chunks retrieved per query |
| `temperature` | `0.7` | LLM sampling temperature |
| `max_tokens` | `512` | Maximum tokens in LLM response |

---

## Supported Document Formats

| Format | Extension | Loader |
|---|---|---|
| PDF | `.pdf` | `PyPDFLoader` |
| Plain text | `.txt` | `TextLoader` |
| Markdown | `.md` | `TextLoader` |

To add support for additional formats (DOCX, HTML, CSV, etc.), extend `DocumentProcessor.SUPPORTED` and add the corresponding LangChain loader in `_load()`.

---

## Troubleshooting

**`ValueError: Vector database is empty`**
The FAISS index has not been initialised. Call `ks.ingest(path)` with at least one document before issuing queries.

**`GROQ_API_KEY MISSING ✗` at startup**
Ensure the environment variable is exported before launching the pipeline. Verify with `echo $GROQ_API_KEY`.

**MongoDB offline mode**
The system continues to function without MongoDB. Query history and document metadata will not be persisted. Check that `MONGO_DB_URL` is set and the Atlas cluster IP allowlist includes your current address.

**MLflow `RestException` or connection refused**
Set `USE_DAGSHUB = False` to fall back to a local `file://` backend, or verify that `MLFLOW_TRACKING_URI`, `MLFLOW_TRACKING_USERNAME`, and `MLFLOW_TRACKING_PASSWORD` are all correctly set.

**`allow_dangerous_deserialization` warning**
This flag is required when loading a pre-built FAISS index from disk. The index is generated and owned by this system; the warning can be safely acknowledged in trusted environments.

---

## Credentials Reference

| Variable | Obtain from |
|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) |
| `MONGO_DB_URL` | [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas) |
| `MLFLOW_TRACKING_URI` | [dagshub.com](https://dagshub.com) — project → MLflow tab |
| `MLFLOW_TRACKING_USERNAME` | DagsHub profile username |
| `MLFLOW_TRACKING_PASSWORD` | DagsHub access token (Settings → Tokens) |

---

## License

Distributed under the MIT License. See `LICENSE` for details.
