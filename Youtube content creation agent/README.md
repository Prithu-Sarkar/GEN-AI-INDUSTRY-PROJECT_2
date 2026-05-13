<div align="center">

<!-- Hero Banner -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=220&section=header&text=StoryForge%20Agent&fontSize=58&fontAlignY=38&desc=YouTube%20Content%20Creation%20%E2%80%A2%20AI-Powered%20%E2%80%A2%20Multi-Agent%20Pipeline&descAlignY=60&descSize=17&fontColor=ffffff&descColor=6EE7B7"/>
  <img alt="StoryForge Agent" src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=220&section=header&text=StoryForge%20Agent&fontSize=58&fontAlignY=38&desc=YouTube%20Content%20Creation%20%E2%80%A2%20AI-Powered%20%E2%80%A2%20Multi-Agent%20Pipeline&descAlignY=60&descSize=17&fontColor=ffffff&descColor=6EE7B7"/>
</picture>

<br/>

[![LangChain](https://img.shields.io/badge/LangChain-≥%201.2-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://python.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.x-F55036?style=for-the-badge&logo=meta&logoColor=white)](https://groq.com/)
[![Tavily](https://img.shields.io/badge/Tavily-Search%20API-06B6D4?style=for-the-badge&logo=searchengin&logoColor=white)](https://tavily.com/)
[![Mem0](https://img.shields.io/badge/Mem0-Memory%20Layer-7C3AED?style=for-the-badge&logo=buffer&logoColor=white)](https://mem0.ai/)
[![MCP](https://img.shields.io/badge/MCP-FastMCP%20Server-10B981?style=for-the-badge&logo=protocol&logoColor=white)](https://modelcontextprotocol.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/yourusername/storyforge-agent?style=flat-square&color=gold)](.)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

<br/>

> **StoryForge Agent** is a production-grade, multi-agent AI pipeline that transforms any topic  
> into a polished YouTube research brief and short-form video script — in seconds.  
> Built on **LangChain ≥ 1.2**, powered by **Groq / LLaMA**, and fully exposed via **MCP tools**.

<br/>

</div>

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🏗️ System Architecture](#️-system-architecture)
- [📂 Project Structure](#-project-structure)
- [🔄 Pipeline Walkthrough](#-pipeline-walkthrough)
- [🔌 MCP Server](#-mcp-server)
- [⚙️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [📓 Notebook Execution](#-notebook-execution)
- [🔧 Configuration](#-configuration)
- [📈 Upgrading to Production](#-upgrading-to-production)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 AI Pipeline
- **Real-time web intelligence** via Tavily Search API
- **Dual-model LLM strategy** — instant vs. versatile LLaMA models calibrated to task complexity
- **Structured output** with Pydantic v2 request/response modelling
- **Query normalisation** — stop-word removal, synonym mapping, signature generation

</td>
<td width="50%">

### 🧠 Memory & Observability
- **Persistent memory layer** with Mem0 + ChromaDB / Qdrant
- **Memory evolution tracking** — full history of add → update → search
- **Dual-handler structured logging** — console (INFO) + rotating file (DEBUG)
- **Phase output archiving** — every pipeline stage serialised to disk

</td>
</tr>
<tr>
<td width="50%">

### 🔌 Interfaces
- **Streamlit web app** (`app.py`) — interactive research + script UI
- **Flask REST demo** (`flask_app.py`) — lightweight HTTP interface
- **MCP server** (`mcp_server.py`) — expose pipeline as native AI tools
- **Notebook** — reproducible, fully commented end-to-end execution

</td>
<td width="50%">

### 🏭 Production Readiness
- **Token-budget guards** per LLM call — safe for free-tier and paid plans alike
- **Graceful degradation** — raw snippets returned when LLM calls fail
- **Modular utility layer** — every component independently testable
- **ZIP output packaging** — all artefacts downloadable in one bundle

</td>
</tr>
</table>

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        StoryForge Agent — System Overview               │
│                                                                         │
│  ┌──────────────┐    ┌──────────────────────────────────────────────┐  │
│  │   Interfaces │    │               Core Pipeline                  │  │
│  │              │    │                                              │  │
│  │  Streamlit   │───▶│  Phase 1: Query Validation & Transform       │  │
│  │  Flask REST  │    │     └─ validate_query() → transform_query()  │  │
│  │  MCP Server  │    │                                              │  │
│  │  Notebook    │    │  Phase 2: Real-Time Research                 │  │
│  └──────────────┘    │     └─ Tavily Search → LLaMA-Instant        │  │
│                      │          (llama-3.1-8b-instant)              │  │
│  ┌──────────────┐    │                                              │  │
│  │  MCP Tools   │    │  Phase 3: Script Generation                  │  │
│  │              │    │     └─ LLaMA-Versatile                       │  │
│  │ get_latest_  │    │          (llama-3.3-70b-versatile)           │  │
│  │  info_mcp    │    │                                              │  │
│  │              │    │  Phase 4: Pydantic Modelling                 │  │
│  │ get_video_   │    │     └─ SearchRequest → SearchResponse        │  │
│  │  script_mcp  │    │                                              │  │
│  └──────┬───────┘    │  Phase 5: Memory Layer (Mem0)                │  │
│         │            │     └─ ChromaDB / Qdrant + Embedder          │  │
│         │            │                                              │  │
│         └───────────▶│  Phase 6: Logging & Output Archiving         │  │
│                      │     └─ Dual-handler logger → ZIP export      │  │
│                      └──────────────────────────────────────────────┘  │
│                                                                         │
│         ┌─────────────┐    ┌──────────────┐    ┌───────────────┐      │
│         │  Groq Cloud │    │ Tavily API   │    │  ChromaDB     │      │
│         │  LLaMA 3.x  │    │ Web Search   │    │  (local/free) │      │
│         └─────────────┘    └──────────────┘    └───────────────┘      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
storyforge-agent/
│
├── 📄 app.py                          # Core pipeline — LangChain + Groq
├── 📄 main.py                         # Project entry-point
├── 📄 flask_app.py                    # Flask HTTP interface
├── 📄 mcp_server.py                   # FastMCP server exposing pipeline tools
│
├── 📁 utilities/
│   ├── 📄 pydantic_models.py          # SearchRequest / SearchResponse models
│   ├── 📄 query_validation_
│   │       transformation.py          # Validate, normalise & fingerprint queries
│   ├── 📄 logging_example.py          # Dual-handler structured logger
│   └── 📄 mem0_example.py             # Mem0 memory + ChromaDB observability demo
│
├── 📁 utilities/
│   └── 📁 __pycache__/
│
├── 📓 StoryForge_YouTube_Agent.ipynb  # End-to-end notebook (all phases)
│
├── 📄 architecture.excalidraw         # System architecture diagram
├── 📄 demo.excalidraw                 # Demo flow diagram
└── 📄 README.md
```

---

## 🔄 Pipeline Walkthrough

### Phase 1 — Query Validation & Transformation

```python
from utilities.query_validation_transformation import handle_query

result = handle_query("latest generative AI advancements 2025")
# {
#   "original":   "latest generative AI advancements 2025",
#   "normalized": "recent generative ai advancements 2025",
#   "cleaned":    "recent generative ai advancements 2025",
#   "signature":  "recent_generative_ai_advancements_2025"
# }
```

Raw user input is sanitised against an allowlist regex, stripped of stop-words, and synonym-mapped before it ever reaches the LLM or search API. This eliminates ambiguity and reduces unnecessary token spend.

---

### Phase 2 — Real-Time Web Research

```python
from app import get_realtime_info

summary = get_realtime_info("recent_generative_ai_advancements_2025")
```

Under the hood:
1. **Tavily Search** (`max_results=3`) fetches the freshest web content
2. Snippets are assembled into a compact context block
3. A `ChatPromptTemplate` (LangChain ≥ 1.2) pipes into **`llama-3.1-8b-instant`** via Groq
4. `StrOutputParser` returns a clean, ~200-word human-readable summary

---

### Phase 3 — Video Script Generation

```python
from app import generate_video_script

script = generate_video_script(summary)
```

The research summary is handed to **`llama-3.3-70b-versatile`** — a higher-capability model intentionally chosen for creative tasks. The system prompt enforces a strong hook, conversational tone, and an explicit call-to-action within 100–120 words — production-ready for YouTube Shorts or Instagram Reels.

---

### Phase 4 — Pydantic Request/Response Modelling

```python
from utilities.pydantic_models import SearchRequest, build_search_response

request  = SearchRequest(user_id="user123", email="user@example.com", query=cleaned_query)
response = build_search_response(request)
```

Every pipeline invocation is wrapped in strongly-typed Pydantic v2 models, giving you built-in input validation, serialisation, and an audit trail for every search session.

---

### Phase 5 — Memory Layer (Mem0 + ChromaDB)

```python
from utilities.mem0_example import run_observability_demo

run_observability_demo()
# [1] Store preference  →  "I prefer FastAPI and AWS."
# [2] Update preference →  "Moved projects to Google Cloud."
# [3] History diff      →  ADD → UPDATE events with old/new values
# [4] Semantic search   →  "What is my deployment preference?" → current value
```

Mem0 provides a persistent, user-scoped memory graph. ChromaDB runs fully locally with zero cloud dependency. Embeddings are computed with **HuggingFace `multi-qa-MiniLM-L6-cos-v1`** — no API key required.

---

### Phase 6 — Logging & Output Archiving

```python
from utilities.logging_example import get_app_logger

logger = get_app_logger("storyforge.pipeline")
logger.info("Pipeline started for query: %s", query)
```

A dual-handler logger (stdout `INFO` + rotating file `DEBUG`) captures every stage. All phase artefacts — summary `.txt`, script `.txt`, model `.json`, query `.json`, and log — are collected and zipped for download.

---

## 🔌 MCP Server

StoryForge exposes its two core capabilities as **Model Context Protocol (MCP) tools**, making the pipeline directly callable from any MCP-compatible AI client (Claude Desktop, Cursor, VS Code with MCP extensions, etc.).

```python
# mcp_server.py
from mcp.server.fastmcp import FastMCP
from app import get_realtime_info, generate_video_script

mcp = FastMCP("StoryForge Video Script Generator")

@mcp.tool()
async def get_latest_info_mcp(query: str) -> str:
    """Fetch real-time web intelligence and return an AI-generated summary."""
    return get_realtime_info(query=query)

@mcp.tool()
async def get_video_script_mcp(query: str) -> str:
    """Research a topic and return a ready-to-use short video script."""
    real_info = get_realtime_info(query=query)
    return generate_video_script(real_info)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### MCP Tool Reference

| Tool | Input | Output | Use-case |
|------|-------|--------|----------|
| `get_latest_info_mcp` | `query: str` | `~200-word summary` | Research briefing |
| `get_video_script_mcp` | `query: str` | `100–120-word script` | Content production |

### Connecting to Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "storyforge": {
      "command": "python",
      "args": ["/absolute/path/to/storyforge-agent/mcp_server.py"],
      "env": {
        "GROQ_API_KEY": "your-groq-key",
        "TAVILY_API_KEY": "your-tavily-key"
      }
    }
  }
}
```

Then simply ask Claude: *"Research the latest AI trends and write me a YouTube Short script."*  
Claude will invoke `get_video_script_mcp` automatically.

---

## ⚙️ Tech Stack

| Layer | Current (Free Tier) | Purpose |
|---|---|---|
| **LLM — Research** | `llama-3.1-8b-instant` via Groq | Fast, low-latency summarisation |
| **LLM — Scripting** | `llama-3.3-70b-versatile` via Groq | High-quality creative generation |
| **Orchestration** | LangChain ≥ 1.2 (`langchain-groq`, `langchain-core`) | Prompt chains, parsers |
| **Web Search** | Tavily Search API (free tier) | Real-time web intelligence |
| **Memory** | Mem0 + ChromaDB (local) | Persistent user memory |
| **Embedder** | HuggingFace `multi-qa-MiniLM-L6-cos-v1` | Local semantic embeddings |
| **Validation** | Pydantic v2 | Request/response modelling |
| **MCP** | FastMCP (`mcp.server.fastmcp`) | AI tool protocol server |
| **Frontend** | Streamlit | Interactive research UI |
| **HTTP API** | Flask | REST demo interface |
| **Logging** | Python `logging` (dual-handler) | Observability |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Groq API key](https://console.groq.com/) (free)
- [Tavily API key](https://app.tavily.com/) (free)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/storyforge-agent.git
cd storyforge-agent

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Environment Variables (`.env`)

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Run the Streamlit App

```bash
streamlit run app.py
```

### Start the MCP Server

```bash
python mcp_server.py
# Listening on stdio — connect via Claude Desktop or any MCP client
```

### Run the Flask Demo

```bash
python flask_app.py
# Open http://localhost:5000
```

---

## 📓 Notebook Execution

The notebook `StoryForge_YouTube_Agent.ipynb` runs the complete 6-phase pipeline end-to-end.

**Prerequisites in your notebook environment:**

1. Store `GROQ_API_KEY` and `TAVILY_API_KEY` in your environment's secrets manager
2. Open `StoryForge_YouTube_Agent.ipynb`
3. Run **All Cells** (`Runtime → Run all` or `Kernel → Restart & Run All`)

The notebook will:
- Install all dependencies automatically
- Write all `.py` source files to disk
- Execute each phase sequentially
- Save all outputs
- Generate a ZIP bundle for download

> **Tip:** Edit the `TOPIC` variable in Step 5 to research any subject you choose.

---

## 🔧 Configuration

### Model Selection

In `app.py`, two model constants control the cost/quality tradeoff:

```python
MODEL_INSTANT   = "llama-3.1-8b-instant"     # Phase 2 — research summary
MODEL_VERSATILE = "llama-3.3-70b-versatile"   # Phase 3 — video script

MAX_TOKENS_SUMMARY = 512   # ~400 words
MAX_TOKENS_SCRIPT  = 300   # ~120 words
```

Groq free-tier token limits are respected by default. Adjust `max_tokens` values when using a paid plan.

### Memory Configuration

In `utilities/mem0_example.py`, the Mem0 config block controls the memory backend:

```python
config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "storyforge_demo",
            "path": "storyforge_agent/outputs/mem0_db",
        },
    },
    ...
}
```

---

## 📈 Upgrading to Production

StoryForge is architected for drop-in upgrades. Below is the full upgrade map — swap any layer independently without touching the rest of the pipeline.

---

### 🧠 LLM Upgrades

| Tier | Provider | Models | Benefit |
|------|----------|--------|---------|
| **Free** | Groq | `llama-3.1-8b-instant`, `llama-3.3-70b-versatile` | Fast inference, generous free quota |
| **Paid — Best Value** | [Groq](https://groq.com/pricing/) | `llama-3.1-70b`, `mixtral-8x7b-32768` | Higher throughput, priority queue |
| **Paid — Highest Quality** | [OpenAI](https://openai.com/pricing) | `gpt-4o`, `gpt-4o-mini` | State-of-the-art reasoning & creativity |
| **Paid — Multimodal** | [Anthropic](https://anthropic.com/pricing) | `claude-opus-4`, `claude-sonnet-4` | Superior instruction-following, long context |
| **Paid — Google** | [Vertex AI](https://cloud.google.com/vertex-ai) | `gemini-2.0-flash`, `gemini-2.5-pro` | Multimodal, grounding with Google Search |

**Switching LLM in LangChain is one import swap:**

```python
# Current (Groq)
from langchain_groq import ChatGroq
llm = ChatGroq(model="llama-3.3-70b-versatile")

# Upgrade to OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o", max_tokens=512)

# Upgrade to Anthropic
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-sonnet-4-20250514", max_tokens=512)
```

---

### 🔍 Search & Research Upgrades

| Tier | Provider | Key Advantage |
|------|----------|---------------|
| **Free** | [Tavily](https://tavily.com/) (free tier) | AI-native search, structured results |
| **Paid** | [Tavily Pro](https://tavily.com/pricing) | Higher rate limits, deep search mode, raw HTML extraction |
| **Paid** | [Perplexity Sonar API](https://www.perplexity.ai/hub/blog/introducing-the-sonar-pro-search-api) | Real-time search + inline citations built-in |
| **Paid** | [Exa.ai](https://exa.ai/) | Neural semantic search, auto-filtering by date and domain |
| **Paid** | [SerpAPI](https://serpapi.com/) | Google / Bing / YouTube / News results with rich metadata |
| **Enterprise** | [Bing Web Search API](https://azure.microsoft.com/en-us/products/ai-services/bing-web-search-api) | Enterprise SLA, freshness controls, safe search |

---

### 🗄️ Vector Database & Memory Upgrades

| Tier | Database | Hosted | Key Advantage |
|------|----------|--------|---------------|
| **Free (local)** | [ChromaDB](https://trychroma.com/) | Self-hosted | Zero cost, no network dependency |
| **Free cloud** | [Pinecone](https://www.pinecone.io/) (Starter) | Cloud | Managed, generous free tier |
| **Paid cloud** | [Pinecone](https://www.pinecone.io/pricing/) (Standard/Enterprise) | Cloud | Sub-millisecond ANN, metadata filtering, SOC 2 |
| **Paid cloud** | [Qdrant Cloud](https://qdrant.tech/pricing/) | Cloud + On-prem | Payload filtering, multitenancy, hybrid search |
| **Paid cloud** | [Weaviate Cloud](https://weaviate.io/pricing) | Cloud | Modular vectoriser, generative search |
| **Enterprise** | [pgvector](https://github.com/pgvector/pgvector) on PostgreSQL | Self-hosted | SQL + vector in one DB, ACID guarantees |

**Swapping to Qdrant Cloud in Mem0:**

```python
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "storyforge_prod",
            "url": "https://your-cluster.qdrant.tech",
            "api_key": os.environ["QDRANT_API_KEY"],
        },
    },
}
```

---

### 🧬 Embedder Upgrades

| Tier | Embedder | Dimensions | Notes |
|------|----------|-----------|-------|
| **Free (local)** | HuggingFace `multi-qa-MiniLM-L6-cos-v1` | 384 | Runs on CPU, no API key |
| **Paid** | [OpenAI `text-embedding-3-small`](https://openai.com/blog/new-embedding-models-and-api-updates) | 1536 | Best price/performance ratio |
| **Paid** | [OpenAI `text-embedding-3-large`](https://openai.com/blog/new-embedding-models-and-api-updates) | 3072 | Highest retrieval accuracy |
| **Paid** | [Cohere `embed-v3`](https://cohere.com/embeddings) | 1024 | Multilingual, compression-friendly |
| **Paid** | [Voyage AI `voyage-3`](https://www.voyageai.com/) | 1024 | Specialised for RAG retrieval tasks |

---

### 📋 Observability & Monitoring Upgrades

| Tier | Tool | What it adds |
|------|------|--------------|
| **Free** | Python `logging` | Structured logs to file + stdout |
| **Free** | [LangSmith](https://smith.langchain.com/) (Free tier) | LangChain tracing, latency, token costs per run |
| **Paid** | [LangSmith Plus](https://smith.langchain.com/pricing) | Team collaboration, dataset management, evaluation |
| **Paid** | [Helicone](https://helicone.ai/) | LLM request logging, cost dashboards, rate limiting |
| **Paid** | [Arize AI](https://arize.com/) | Production ML monitoring, drift detection, embeddings explorer |
| **Enterprise** | [Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/) | Full APM + LLM tracing unified |

---

### 📦 Deployment Upgrades

| Target | Stack | Notes |
|--------|-------|-------|
| **Local dev** | `streamlit run app.py` | Zero config |
| **Containerised** | Docker + `docker-compose` | Included in project (`Dockerfile` / `docker-compose.yml`) |
| **Serverless** | [AWS Lambda](https://aws.amazon.com/lambda/) + API Gateway | Cold-start friendly with LangChain slim builds |
| **PaaS** | [Railway](https://railway.app/) / [Render](https://render.com/) | One-click deploy from GitHub |
| **Managed AI** | [AWS Bedrock](https://aws.amazon.com/bedrock/) | Enterprise-grade, swap `ChatGroq` for `ChatBedrock` |
| **Enterprise** | [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service) | Private endpoint, compliance, VNet integration |

---

## 🗺️ Roadmap

- [ ] **Multi-topic batch processing** — queue N topics and generate all scripts in parallel
- [ ] **YouTube analytics integration** — ingest channel stats to bias topic selection
- [ ] **Voice-over synthesis** — pipe scripts to ElevenLabs / OpenAI TTS for audio output
- [ ] **Thumbnail prompt generation** — produce DALL·E / Midjourney prompts alongside each script
- [ ] **LangGraph orchestration** — replace linear chain with a stateful, branching agent graph
- [ ] **Async FastAPI backend** — production HTTP layer replacing Flask demo
- [ ] **Evaluation harness** — RAGAS / LangSmith evals for summary quality scoring
- [ ] **Multi-language support** — detect query language and generate scripts in-language
- [ ] **Scheduled runs** — cron-triggered pipeline with auto-export to Notion / Google Docs

---

## 🤝 Contributing

Contributions are welcome and appreciated! Please follow these steps:

1. **Fork** the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push the branch: `git push origin feature/your-feature-name`
5. Open a **Pull Request** and describe your changes

Please ensure:
- All new utility functions include docstrings
- New dependencies are added to `requirements.txt`
- Code follows PEP 8 style conventions

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,50:203a43,100:0f2027&height=100&section=footer"/>
  <img alt="footer" src="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,50:203a43,100:0f2027&height=100&section=footer"/>
</picture>

**Built with 💚 by the StoryForge team**

*If this project helped you, consider giving it a ⭐ — it helps others find it too.*

</div>
