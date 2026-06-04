# AI-Powered Customer Support Agent

An intelligent customer support copilot that generates contextual draft replies using a LangGraph ReAct agent, FAISS-backed RAG, per-customer memory, and LangChain tool-calling — all on a fully open-source, locally-run stack.

---

## Features

- **LangGraph ReAct Agent** — multi-step reasoning with tool-calling loops and automatic fallback chain
- **Retrieval-Augmented Generation** — FAISS vector store over banking policy documents for grounded responses
- **Per-Customer Memory** — FAISS-backed memory store that learns from accepted draft resolutions
- **LangChain Tools** — `lookup_customer_plan` (SLA/billing) and `lookup_open_ticket_load` (SQLite), with optional Tavily web search
- **Dual-Model Strategy** — `llama-3.1-8b-instant` for fast agent loops; `llama-3.3-70b-versatile` for fallback synthesis
- **Three-Layer Fallback** — ReAct agent → LLM synthesis → deterministic template (never returns empty)
- **Full Audit Trail** — every draft stores a structured `context_used` dict with signals, KB hits, memory hits, and tool traces
- **SQLite Persistence** — customers, tickets, and drafts stored relationally with FK constraints and auto-updated timestamps

---

## Tech Stack

| Layer | Library | Version |
|---|---|---|
| Agent framework | `langgraph` | `>=0.2.0` |
| LLM client | `langchain-groq` | `>=0.2.0` |
| Core abstractions | `langchain-core` | `>=0.3.0` |
| Community tools | `langchain-community` | `>=0.3.0` |
| Text splitting | `langchain-text-splitters` | `>=0.3.0` |
| LangChain base | `langchain` | `>=1.2.0` |
| Vector DB (RAG + Memory) | `faiss-cpu` | `>=1.8.0` |
| Embeddings | `sentence-transformers` | `>=3.0.0` |
| Embedding model | `all-MiniLM-L6-v2` | — |
| SQL database | `sqlite3` | stdlib |
| Config | `pydantic-settings` | `>=2.3.0` |

> No paid vector database or cloud storage required. All vector indexes persist to local disk.

---

## Project Structure

```
customer_support_agent/
├── src/
│   ├── core/
│   │   └── settings.py               # Pydantic-Settings v2 config singleton
│   ├── integrations/
│   │   ├── memory/
│   │   │   └── faiss_memory.py       # Per-customer FAISS memory store
│   │   ├── rag/
│   │   │   └── faiss_kb.py           # FAISS knowledge-base RAG service
│   │   └── tools/
│   │       └── support_tools.py      # LangChain @tool definitions
│   ├── repositories/
│   │   └── sqlite/
│   │       ├── base.py               # SQLite helpers + schema DDL
│   │       ├── customers.py
│   │       ├── tickets.py
│   │       └── drafts.py
│   ├── services/
│   │   ├── copilot_service.py        # LangGraph ReAct agent orchestrator
│   │   ├── draft_service.py          # Draft generation + acceptance workflow
│   │   └── knowledge_service.py      # KB ingestion wrapper
│   └── schemas/
├── knowledge_base/                   # Markdown policy documents (RAG source)
│   ├── banking-atm-cash-withdrawal-faq.md
│   ├── banking-charges-and-minimum-balance.md
│   ├── banking-kyc-and-account-update-rules.md
│   └── saving-account-rule.md
├── data/
│   ├── support.db                    # SQLite database
│   ├── faiss_rag/                    # Persisted RAG FAISS index
│   └── faiss_mem/                    # Persisted per-customer memory indexes
├── outputs/                          # Phase output JSON files
├── DEPLOYMENT.md                     # EC2 deployment guide
└── AI_Customer_Support_Agent_Colab.ipynb
```

---

## API Keys

| Variable | Purpose | Required |
|---|---|---|
| `GROQ_API_KEY` | LLM inference via Groq | **Yes** |
| `TAVILY_API_KEY` | Web-search tool inside the ReAct agent | No |

Obtain a free `GROQ_API_KEY` at [console.groq.com](https://console.groq.com).  
Obtain a `TAVILY_API_KEY` at [tavily.com](https://tavily.com).

---

## Quickstart (Notebook)

1. Open `AI_Customer_Support_Agent_Colab.ipynb` in any Jupyter-compatible environment.
2. Add `GROQ_API_KEY` (and optionally `TAVILY_API_KEY`) to your environment secrets.
3. Run all cells top-to-bottom. Each phase writes its source files, then executes them.

Phases run in order:

| Phase | Action |
|---|---|
| 0 | Install packages + load API keys |
| 1 | Create folder structure |
| 2 | Write `settings.py` + initialise SQLite schema |
| 3 | Write knowledge-base markdown files |
| 4 | Build FAISS RAG index, verify search |
| 5 | Build FAISS memory store, smoke-test |
| 6 | Define LangChain tools, test invocation |
| 7 | Build `SupportCopilot` with LangGraph ReAct agent |
| 8 | Write repository layer (customers / tickets / drafts) |
| 9 | Write service layer (DraftService / KnowledgeService) |
| 10 | End-to-end demo: create ticket → generate AI draft |
| 11 | Accept draft → persist memory → probe memory search |
| 12 | Write `DEPLOYMENT.md` |
| 13 | Zip all outputs and download |

---

## Draft Generation Pipeline

```
Ticket + Customer
       │
       ├─► FAISS Memory Search    (customer history, per-email + per-company scope)
       ├─► FAISS RAG Search       (policy documents, top-k chunks)
       │
       ▼
  System Prompt  (memory block + KB block, token-budgeted)
  User Prompt    (ticket subject, description, priority)
       │
       ▼
  LangGraph ReAct Agent  ──► lookup_customer_plan
  (llama-3.1-8b-instant)  ──► lookup_open_ticket_load
                           ──► TavilySearchResults (optional)
       │
       ▼
  Draft Extraction  ──► if empty ──► LLM Fallback (llama-3.3-70b-versatile)
                                 ──► if empty ──► Deterministic Template
       │
       ▼
  Draft + context_used  ──► SQLite drafts table
       │
  On Accept ──► FAISS Memory Write (resolution persisted for future tickets)
```

---

## LangChain 1.2+ Import Reference

All imports use canonical paths from LangChain 1.2 and above. No legacy `langchain.` top-level imports are used.

```python
# Text splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Tool decorator
from langchain_core.tools import tool

# Message types
from langchain_core.messages import (
    AIMessage, HumanMessage, SystemMessage, ToolMessage, BaseMessage
)

# LLM client
from langchain_groq import ChatGroq

# Community tools
from langchain_community.tools.tavily_search import TavilySearchResults

# LangGraph agent + checkpoint
from langgraph.prebuilt          import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
```

---

## Configuration

All settings are managed in `src/core/settings.py` via `pydantic-settings`. Override any value using environment variables or a `.env` file.

| Setting | Default | Description |
|---|---|---|
| `groq_model_instant` | `llama-3.1-8b-instant` | Model used for agent tool-calling loop |
| `groq_model_versatile` | `llama-3.3-70b-versatile` | Model used for fallback synthesis |
| `max_tokens_per_call` | `1024` | Token cap per Groq API call |
| `embedding_model` | `all-MiniLM-L6-v2` | Local sentence-transformer model |
| `rag_chunk_size` | `800` | Characters per RAG chunk |
| `rag_chunk_overlap` | `120` | Chunk overlap for context continuity |
| `rag_top_k` | `4` | KB chunks retrieved per query |
| `mem_top_k` | `5` | Memory hits retrieved per query |

---

## Deployment

See [`DEPLOYMENT.md`](./DEPLOYMENT.md) for a complete step-by-step guide to deploying on AWS EC2 (Ubuntu 22.04, no Docker).

Summary of steps:

1. Launch EC2 instance (t3.small, Ubuntu 22.04)
2. Install Python 3.11 and create a virtual environment
3. Install dependencies with the version pins above
4. Set `GROQ_API_KEY` and `TAVILY_API_KEY` in a `.env` file (`chmod 600`)
5. Initialise the SQLite schema and ingest knowledge-base documents
6. Run the application under `systemd` for auto-restart on failure
7. Optionally add Nginx + Let's Encrypt for HTTPS

---

## Database Schema

```sql
customers  (id, email UNIQUE, name, company, created_at)
tickets    (id, customer_id FK, subject, description, status, priority, created_at, updated_at)
drafts     (id, ticket_id FK, content, context_used JSON, status, created_at)
```

`status` values — tickets: `open | resolved | closed`  
`status` values — drafts: `pending | accepted | discarded | failed`

---

## Memory Scoping

Each customer's memory is indexed under two scopes, allowing the agent to retrieve both personal history and company-wide resolution patterns:

- **Per-email** — `alice@acme.com`
- **Per-company** — `company::acme` (shared across all contacts from the same organisation)

---

## License

MIT
