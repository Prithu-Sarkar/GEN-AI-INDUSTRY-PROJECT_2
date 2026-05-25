# Source Code Analyzer

> A Retrieval-Augmented Generation (RAG) system that transforms any GitHub repository into an interactive, natural-language knowledge base — backed by a production-ready Flask API, FAISS vector search, and GROQ-hosted LLaMA inference.

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Notebook](#running-the-notebook)
  - [Flask API Reference](#flask-api-reference)
  - [Web Interface](#web-interface)
- [Core Components](#core-components)
  - [AST-Aware Code Chunking](#ast-aware-code-chunking)
  - [Vector Indexing Pipeline](#vector-indexing-pipeline)
  - [RAG Chain Design](#rag-chain-design)
  - [Tavily Fallback Search](#tavily-fallback-search)
- [API Endpoints](#api-endpoints)
- [Token Budget & Performance](#token-budget--performance)
- [Caching Strategy](#caching-strategy)
- [Security & Git Safety](#security--git-safety)
- [Environment Variables](#environment-variables)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

Source Code Analyzer solves a fundamental problem in software engineering: **understanding large, undocumented codebases takes days**. This system reduces that to seconds.

A developer provides a public GitHub repository URL. The system shallow-clones the repository, walks every Python source file, and uses Python's `ast` module to extract semantically complete code units — classes, functions, and module-level blocks — preserving their logical boundaries. These chunks are embedded into a FAISS vector store and made queryable through a conversational RAG chain backed by GROQ's `llama-3.1-8b-instant` model.

The result is a multi-turn chat interface where engineers can ask architectural questions, trace function behaviour, understand dependencies, and explore unfamiliar codebases — all in plain English, with answers grounded in the actual source code.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
│          Web UI (HTML/JS)  ·  REST Client  ·  Notebook REPL        │
└───────────────────────────────┬─────────────────────────────────────┘
                                │  HTTP
┌───────────────────────────────▼─────────────────────────────────────┐
│                        FLASK REST API                               │
│   /api/load    /api/chat    /api/reset    /api/health               │
└──────────┬──────────────────────────────────────┬───────────────────┘
           │                                      │
┌──────────▼──────────┐                ┌──────────▼──────────────────┐
│   INGESTION PIPELINE │                │     INFERENCE PIPELINE      │
│                      │                │                             │
│  GitHub Repo Clone   │                │  ConversationalRetrieval    │
│  AST Chunker (ast)   │                │  Chain (LangChain 0.1)      │
│  HuggingFace Embed   │                │                             │
│  FAISS Index Build   │                │  ┌────────────────────┐    │
│  Disk Persistence    │                │  │  GROQ LLM          │    │
└──────────┬──────────┘                │  │  llama-3.1-8b-inst │    │
           │                           │  └────────────────────┘    │
┌──────────▼──────────┐                │                             │
│   FAISS VECTOR DB    │◄───MMR─────────│  Retriever (k=6, MMR)      │
│   (disk-persisted)   │                │  Memory (window k=6)       │
└─────────────────────┘                │                             │
                                       │  ┌────────────────────┐    │
                                       │  │  Tavily Web Search │    │
                                       │  │  (low-conf fallback)│    │
                                       │  └────────────────────┘    │
                                       └────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| AI Framework | LangChain | 0.1.20 |
| LLM Inference | GROQ — `llama-3.1-8b-instant` | Latest |
| Vector Database | FAISS (CPU) | 1.8.0 |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` | sentence-transformers 3.0.1 |
| Web Search | Tavily Search API | 0.3.3 |
| Backend / API | Flask + Flask-CORS | 3.0.3 |
| Data Source | GitHub (public repositories) | via GitPython 3.1.43 |
| Runtime | Python | 3.10+ |

---

## Project Structure

```
source-code-analyzer/
│
├── source_code_analyzer.ipynb   # Main notebook — all pipeline stages
├── README.md                    # This file
├── .gitignore                   # Excludes .env, __pycache__, outputs
│
└── (runtime-generated, git-ignored)
    ├── /tmp/src_analyzer_repos/   # Shallow-cloned repositories
    └── /tmp/src_analyzer_faiss/   # Persisted FAISS indexes
```

---

## Prerequisites

- Python 3.10 or higher
- `pip` package manager
- A GROQ API key — [console.groq.com](https://console.groq.com)
- A Tavily API key — [tavily.com](https://tavily.com)
- Internet access (for repository cloning and LLM inference)

---

## Installation

**1. Clone this repository**

```bash
git clone https://github.com/your-org/source-code-analyzer.git
cd source-code-analyzer
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

**3. Install dependencies**

All dependencies are installed in Cell 1 of the notebook. To install them manually:

```bash
pip install \
  langchain==0.1.20 \
  langchain-community==0.0.38 \
  langchain-groq==0.1.3 \
  faiss-cpu==1.8.0 \
  flask==3.0.3 \
  flask-cors==4.0.1 \
  gitpython==3.1.43 \
  tavily-python==0.3.3 \
  sentence-transformers==3.0.1 \
  tiktoken==0.7.0
```

---

## Configuration

Create a `.env` file in the project root (this file is git-ignored):

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Export environment variables before launching the notebook:

```bash
export GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

If neither method is used, Cell 2 of the notebook will prompt for keys via `getpass()` — input is hidden and never stored in cell output.

---

## Usage

### Running the Notebook

Open the notebook in Jupyter or any compatible environment:

```bash
jupyter notebook source_code_analyzer.ipynb
```

Run cells sequentially from top to bottom. Each cell is independently documented. The expected execution order is:

| Cell | Action | Expected Output |
|------|--------|----------------|
| 1 | Install packages | `✅ All packages installed` |
| 2 | Load API keys | `✅ Keys configured` |
| 3 | Clone repository | `✅ Clone complete` |
| 4 | Chunk Python files | `📦 Indexed N chunks` |
| 5 | Build FAISS index | `✅ FAISS index saved` |
| 6 | Initialise LLM + Tavily | `LLM test: LLM OK` |
| 7 | Build RAG chain | `✅ RAG chain with memory is ready` |
| 8 | Notebook chat REPL | Interactive prompt |
| 9 | Start Flask server | `✅ Flask API running at :5050` |
| 10 | API smoke tests | `✅ All API tests passed` |
| 11 | Register web UI route | `🌐 Web UI available` |
| 12 | Checkpoint summary | All indicators green |

---

### Flask API Reference

Once Cell 9 has been executed, the REST API is live at `http://localhost:5050`.

#### Load a Repository

```bash
curl -X POST http://localhost:5050/api/load \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/pallets/flask"}'
```

```json
{
  "status": "ok",
  "repo_url": "https://github.com/pallets/flask",
  "chunk_count": 843,
  "message": "Repository indexed successfully (843 chunks)."
}
```

#### Ask a Question

```bash
curl -X POST http://localhost:5050/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How does Flask handle request routing?"}'
```

```json
{
  "answer": "Flask's routing is handled by the Werkzeug URL routing map ...",
  "sources": [
    "/tmp/src_analyzer_repos/flask/src/flask/app.py",
    "/tmp/src_analyzer_repos/flask/src/flask/routing.py"
  ],
  "tavily_results": null
}
```

#### Reset Conversation Memory

```bash
curl -X POST http://localhost:5050/api/reset
```

#### Health Check

```bash
curl http://localhost:5050/api/health
```

---

### Web Interface

After Cell 11 executes, navigate to:

```
http://localhost:5050
```

The interface provides a two-panel layout: a repository loader and a multi-turn chat panel. All API calls are made client-side via `fetch`. The UI is self-contained in a single HTML response — no build step or external CDN dependency required.

---

## Core Components

### AST-Aware Code Chunking

Standard recursive character splitters break code mid-function, destroying semantic context. This system uses Python's built-in `ast` module to parse source files into a concrete syntax tree and extract:

- **`ast.ClassDef`** nodes — entire class bodies, including all methods
- **`ast.FunctionDef` / `ast.AsyncFunctionDef`** nodes — individual function and coroutine definitions
- **Module-level fallback** — line-grouped blocks for imports, constants, and top-level statements

Each chunk is capped at **3,000 characters** (~750 tokens) before embedding. Chunks exceeding this limit are truncated with an explicit `# ... [truncated]` marker so the LLM is aware of the truncation.

Duplicate chunks (arising from AST and module-level overlap) are deduplicated by content hash before indexing.

```python
# Each CodeChunk carries rich metadata for source attribution
@dataclass
class CodeChunk:
    content:    str
    file_path:  str
    chunk_type: str    # 'class' | 'function' | 'module'
    name:       str
    start_line: int
    end_line:   int
    metadata:   dict
```

### Vector Indexing Pipeline

Chunks are converted to LangChain `Document` objects and embedded using `sentence-transformers/all-MiniLM-L6-v2` — a 384-dimensional model that runs entirely on CPU with no API dependency. The resulting FAISS index is persisted to disk and reloaded on subsequent runs, making repeat analysis of the same repository near-instant.

Retrieval uses **Maximum Marginal Relevance (MMR)** with `k=6, fetch_k=20`. MMR balances relevance with diversity, preventing the retriever from returning six near-identical chunks from the same function.

### RAG Chain Design

The system uses LangChain's `ConversationalRetrievalChain`, which provides:

**Condense step** — a dedicated prompt rephrases follow-up questions into standalone queries before retrieval, ensuring conversational context is preserved across turns without polluting the semantic search.

**Answer step** — a grounded system prompt instructs the LLM to answer exclusively from retrieved source code, reference specific file and function names, and explicitly acknowledge when the context is insufficient.

**Memory** — a `ConversationBufferWindowMemory` retains the last 6 exchange pairs (~12 messages). This is sufficient for multi-turn technical deep-dives while staying well within the LLM's context window.

### Tavily Fallback Search

When the LLM signals low confidence (detected via phrase matching on responses containing "I don't know", "not found", "cannot find", etc.), the system automatically queries Tavily's web search API and appends results to the API response. This handles questions about external libraries, documentation, or context that exists outside the repository itself.

---

## API Endpoints

| Method | Path | Description | Body |
|--------|------|-------------|------|
| `GET` | `/api/health` | Liveness check, reports indexed state | — |
| `POST` | `/api/load` | Clone repo and build vector index | `{"repo_url": str, "force_rebuild": bool}` |
| `POST` | `/api/chat` | Submit a question, get a grounded answer | `{"question": str, "tavily": bool}` |
| `POST` | `/api/reset` | Clear conversation memory | — |
| `GET` | `/` | Serve the web interface | — |

All endpoints return JSON. Error responses carry an `"error"` key with a human-readable message and an appropriate HTTP status code (400, 422, 500).

---

## Token Budget & Performance

The GROQ `llama-3.1-8b-instant` model has a 128k token input context. The system is conservatively configured to stay well within safe operating limits:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `max_tokens` (response) | 1,024 | Sufficient for technical answers; avoids runaway generation |
| Chunk size cap | 3,000 chars ≈ 750 tokens | Keeps individual chunks well below per-chunk limits |
| MMR `k` | 6 chunks | ~4,500 tokens of context per query |
| Memory window | 6 turns | ~1,200 tokens of history |
| **Total context budget** | ~7,200 tokens | Leaves substantial headroom in the 128k window |

---

## Caching Strategy

The system implements two layers of disk-based caching to avoid redundant work:

**Repository cache** — shallow clones are stored at `$TMPDIR/src_analyzer_repos/<repo-name>/`. Re-loading the same URL reuses the existing clone unless `force_reclone=True` is passed.

**FAISS cache** — vector indexes are persisted at `$TMPDIR/src_analyzer_faiss/<repo-name>/`. A pre-built index is loaded directly on subsequent runs, bypassing the embedding step entirely.

To invalidate both caches and rebuild from scratch, pass `"force_rebuild": true` in the `/api/load` request body.

---

## Security & Git Safety

This repository is designed to be safe to commit to version control without modification:

- **No secrets in source** — API keys are loaded exclusively from environment variables or runtime `getpass()` prompts.
- **No cell outputs committed** — notebook outputs should be cleared before committing (`Kernel → Restart & Clear Output`).
- **No credentials in logs** — Flask routes do not echo request bodies containing sensitive data.

Recommended `.gitignore` entries:

```gitignore
.env
*.env
.env.*
__pycache__/
*.pyc
*.pyo
.ipynb_checkpoints/
*.egg-info/
dist/
build/
.venv/
venv/
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ Yes | GROQ platform API key for LLM inference |
| `TAVILY_API_KEY` | ✅ Yes | Tavily Search API key for web fallback |

---

## Limitations

- **Python only** — the AST chunker targets `.py` files exclusively. JavaScript, TypeScript, Java, and other languages fall back to plain text splitting if extended manually.
- **Public repositories** — the cloner uses unauthenticated HTTPS. Private repositories require a GitHub personal access token injected into the URL or via `GIT_ASKPASS`.
- **Single repository per server instance** — the Flask server holds one active index in memory. Multi-tenant usage requires process isolation or a shared vector store backend (e.g. Pinecone, Weaviate).
- **Ephemeral FAISS index** — the server-side `_state` dictionary is in-process. A server restart clears the active index; the persisted disk cache must be reloaded via `/api/load`.
- **Embedding model accuracy** — `all-MiniLM-L6-v2` is optimised for speed and produces good general-purpose embeddings. Code-specific embedding models (e.g. `CodeBERT`, `UniXcoder`) will yield higher precision for large, diverse codebases.

---

## Roadmap

- [ ] Multi-language support (JavaScript, TypeScript, Java, Go) via Tree-sitter
- [ ] GitHub authentication for private repository access
- [ ] Streaming LLM responses via Server-Sent Events
- [ ] Persistent multi-session state with SQLite or Redis
- [ ] Docker packaging with `docker-compose` for one-command deployment
- [ ] Code-specialised embedding model integration (`CodeBERT`, `UniXcoder`)
- [ ] Structured output mode — return cited line numbers with each answer
- [ ] Configurable chunking strategies via query parameter

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
