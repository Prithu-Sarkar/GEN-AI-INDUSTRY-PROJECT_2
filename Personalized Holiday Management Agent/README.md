<div align="center">

<img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/LangChain-≥1.2-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white"/>
<img src="https://img.shields.io/badge/Groq-LLaMA%203.1-F55036?style=for-the-badge&logo=meta&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/MLflow-Tracking-0194E2?style=for-the-badge&logo=mlflow&logoColor=white"/>
<img src="https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white"/>
<img src="https://img.shields.io/badge/Mem0-Memory%20Layer-8B5CF6?style=for-the-badge&logoColor=white"/>
<img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white"/>

<br/><br/>

# 🏖️ Personalized Holiday Management Agent

### *An autonomous, multi-agent AI system for intelligent, hallucination-resistant travel planning*

<br/>

> *"From a single sentence prompt to a fully verified, day-by-day itinerary — powered by specialized AI agents working in concert."*

<br/>

[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/Prithu-Sarkar/GEN-AI-INDUSTRY-PROJECT_2)
[![DagsHub](https://img.shields.io/badge/Experiment%20Tracking-DagsHub-FC8200?style=flat-square&logo=dagshub&logoColor=white)](https://dagshub.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-blue?style=flat-square)](https://pep8.org/)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Pipeline Walkthrough](#-pipeline-walkthrough)
- [Getting Started](#-getting-started)
- [Environment Variables & API Keys](#-environment-variables--api-keys)
- [Running the API](#-running-the-api)
- [Experiment Tracking with MLflow](#-experiment-tracking-with-mlflow)
- [Long-Term Memory with Mem0](#-long-term-memory-with-mem0)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌍 Overview

**Personalized Holiday Management Agent** is a production-grade, multi-agent AI system that transforms a single natural-language travel request into a verified, structured, and personalized day-by-day itinerary.

Standard LLM chatbots suffer from a fundamental flaw in travel planning: they fabricate hotel names, invent opening hours, and hallucinate train schedules. This system solves that problem by enforcing a strict **separation of concerns** across specialized agents — a Planner that thinks strategically and a Researcher that verifies every fact before it reaches the final output.

The system is built around a shared **AgentState** object that flows through the entire pipeline, capturing every intermediate output, message history, and metadata for full observability. Every run is tracked in **MLflow on DagsHub**, every user preference persists across sessions via **Mem0**, and every data contract is enforced at runtime by **Pydantic v2**.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **Multi-Agent Pipeline** | Planner → Researcher agents with clean state hand-offs |
| 🚫 **Hallucination Prevention** | Researcher verifies every fact before the final output is written |
| 🧠 **Long-Term Memory** | Mem0 + ChromaDB remembers user preferences across sessions |
| 📐 **Pydantic Validation** | Every input and output is schema-validated at runtime |
| 🔍 **Query Transformation** | Stop-word removal, synonym expansion, and cache-key generation |
| 📊 **MLflow Experiment Tracking** | Every run logs parameters, metrics, and artifacts to DagsHub |
| 📋 **Structured Logging** | Dual-output logger (console + file) with full audit trails |
| ⚡ **FastAPI REST Interface** | Production-ready async API with Swagger auto-documentation |
| 🔄 **CI/CD via GitHub Actions** | Automated test and deploy pipeline on every push |
| 🌐 **Groq Inference** | `llama-3.1-8b-instant` — fast, cost-effective, free-tier friendly |

---

## 🏗️ Architecture

The system follows a **Sequential Multi-Agent Pattern** with a central shared state object acting as the single source of truth across all agents.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER REQUEST (Natural Language)                  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 1 — Input Layer                                                  │
│  ┌─────────────────────┐   ┌──────────────────────────────────────┐    │
│  │  Pydantic Validator  │──▶│  Query Transformation Pipeline       │    │
│  │  (TripPlanRequest)   │   │  normalize → clean → cache_signature │    │
│  └─────────────────────┘   └──────────────────────────────────────┘    │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 2 — Memory Retrieval                                             │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Mem0 (ChromaDB + Groq)                                        │    │
│  │  Semantic search of past user preferences → inject into prompt │    │
│  └────────────────────────────────────────────────────────────────┘    │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 3 — Agent Pipeline (AgentState flows through all steps)          │
│                                                                         │
│   ┌──────────────────────────────────────────────────────────────┐     │
│   │  AGENT 1: PLANNER  (Strategy Layer)                          │     │
│   │  • Groq llama-3.1-8b-instant via LangChain ≥1.2             │     │
│   │  • Input:  request + user_memory                             │     │
│   │  • Output: state.draft_plan  (day-by-day skeleton)           │     │
│   └────────────────────────────┬─────────────────────────────────┘     │
│                                │ AgentState                             │
│   ┌────────────────────────────▼─────────────────────────────────┐     │
│   │  AGENT 2: RESEARCHER  (Data Verification Layer)              │     │
│   │  • Groq llama-3.1-8b-instant via LangChain ≥1.2             │     │
│   │  • Input:  state.draft_plan                                  │     │
│   │  • Output: state.final_output  (enriched Markdown guide)     │     │
│   └──────────────────────────────────────────────────────────────┘     │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 4 — Observability & Storage                                      │
│  ┌──────────────────┐   ┌──────────────────┐   ┌───────────────────┐   │
│  │  MLflow / DagsHub │   │  MongoDB Atlas   │   │  Structured Logger│   │
│  │  params + metrics │   │  user sessions   │   │  full audit trail │   │
│  └──────────────────┘   └──────────────────┘   └───────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │   FastAPI REST Response        │
                    │   Formatted Markdown Itinerary │
                    └───────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM** | Groq `llama-3.1-8b-instant` | Fast, cost-effective inference for both agents |
| **Orchestration** | LangChain ≥ 1.2 | Prompt templates, chains, output parsers |
| **Memory** | Mem0 + ChromaDB | Long-term, semantic user preference memory |
| **Validation** | Pydantic v2 | Runtime schema enforcement on all I/O |
| **API Server** | FastAPI + Uvicorn | Async REST API with auto-generated Swagger docs |
| **Experiment Tracking** | MLflow + DagsHub | Parameter, metric, and artifact logging per run |
| **Database** | MongoDB Atlas | Persistent user session and trip storage |
| **Logging** | Python `logging` | Dual-output (console + file) structured audit trail |
| **CI/CD** | GitHub Actions | Automated test, lint, and deploy on push |
| **Packaging** | `setuptools` | Installable `holiday_management` Python package |

---

## 📁 Project Structure

```
Personalized-Holiday-Management-Agent/
│
├── 📦 holiday_management/              # Core installable package
│   ├── config/
│   │   └── settings.py                # Centralised env config (single source of truth)
│   ├── agents/
│   │   ├── planner.py                 # Agent 1: Strategy skeleton itinerary
│   │   └── researcher.py              # Agent 2: Fact verification & enrichment
│   ├── teams/
│   │   └── holiday_team.py            # Orchestrates agent pipeline + Mem0
│   └── utils/
│       ├── state.py                   # AgentState dataclass (shared across all agents)
│       └── utils.py                   # Format helpers, timer decorator, safe dict access
│
├── 🧰 all-utils/
│   ├── main.py                        # Utility module entry point
│   ├── requirements.txt               # Utility-specific dependencies
│   └── utilities/
│       ├── pydantic_models.py         # SearchRequest / SearchResponse / TripPlanRequest
│       ├── query_validation_transformation.py  # Query cleaning pipeline
│       ├── logging_example.py         # Reusable dual-output logger factory
│       └── mem0_example.py            # Mem0 observability demo
│
├── 📊 phase_outputs/                  # Per-phase artefact outputs (gitignored blobs)
│   ├── phase1_pydantic_output.txt
│   ├── phase2_query_transform_output.json
│   ├── phase3_logging_output.log
│   ├── phase4_mem0_output.txt
│   ├── phase7_draft_plan.md
│   └── phase7_final_itinerary.md
│
├── 🌐 static/
│   └── styles.css                     # Frontend styles for the web UI
│
├── app.py                             # FastAPI application entry point
├── main.py                            # CLI runner (asyncio)
├── setup.py                           # Package installation config
├── requirements.txt                   # Project-level dependencies
├── .gitignore                         # Excludes __pycache__, .ipynb_checkpoints, db/, mlruns/
└── README.md                          # You are here
```

---

## 🔄 Pipeline Walkthrough

### Step 1 — Input Validation
Every request is validated against the `TripPlanRequest` Pydantic model before any LLM call is made. Invalid inputs (empty queries, out-of-range durations, unknown budget tiers) raise a `ValidationError` immediately — the LLM never sees malformed data.

### Step 2 — Query Transformation
The raw user query is passed through a three-stage transformation pipeline:
- **Normalize** — lowercase, collapse whitespace
- **Clean** — remove stop-words, apply synonym map (`holiday → vacation`, `cheap → budget`)
- **Signature** — generate a deterministic cache key for semantic deduplication

### Step 3 — Memory Retrieval (Mem0)
Before the Planner runs, the system performs a semantic search over the user's past preferences stored in ChromaDB via Mem0. The top-matching memory snippet is injected directly into the Planner's prompt, enabling genuine personalization across sessions without any manual state management.

### Step 4 — Planner Agent
The Planner is the **strategic layer**. It receives the validated request and the user's memory context, then generates a geographically logical day-by-day skeleton itinerary. Activities are grouped by proximity. Day 1 is intentionally light (arrival day). No prices or opening times are fabricated at this stage.

### Step 5 — Researcher Agent
The Researcher is the **verification layer**. It takes the Planner's skeleton and enriches each activity with realistic practical details: best visit time, cost bracket, and traveller tips. In production, this agent connects to live APIs (Google Places, TripAdvisor). The Researcher is explicitly forbidden from inventing specific URLs or phone numbers.

### Step 6 — MLflow Logging
Every pipeline execution is logged as an MLflow run on DagsHub with:
- **Parameters** — model name, temperature, max tokens, destination, duration
- **Metrics** — output character counts, message counts, latency
- **Artifacts** — the draft plan and final itinerary Markdown files

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A [Groq API key](https://console.groq.com) (free tier available)
- A [MongoDB Atlas](https://cloud.mongodb.com) cluster (free M0 tier available)
- A [DagsHub](https://dagshub.com) account for experiment tracking

### 1. Clone the Repository

```bash
git clone https://github.com/Prithu-Sarkar/GEN-AI-INDUSTRY-PROJECT_2.git
cd GEN-AI-INDUSTRY-PROJECT_2
```

### 2. Create a Virtual Environment

```bash
conda create -n holiday_agent python=3.12 -y
conda activate holiday_agent
```

Or with `venv`:

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .                  # install holiday_management as a local package
```

### 4. Configure Environment Variables

Copy the example env file and fill in your credentials:

```bash
cp .env.example .env
```

See the [Environment Variables](#-environment-variables--api-keys) section for the full list.

---

## 🔑 Environment Variables & API Keys

Create a `.env` file in the project root with the following variables:

```dotenv
# ── LLM (Groq) ────────────────────────────────────────────────────────────────
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ── Database (MongoDB Atlas) ──────────────────────────────────────────────────
MONGO_DB_URL=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true

# ── Experiment Tracking (DagsHub / MLflow) ────────────────────────────────────
MLFLOW_TRACKING_URI=https://dagshub.com/<username>/<repo>.mlflow
MLFLOW_TRACKING_USERNAME=<your_dagshub_username>
MLFLOW_TRACKING_PASSWORD=<your_dagshub_token>
```

### Full API Key Reference

| Key | Required | Free Tier | Description |
|---|---|---|---|
| `GROQ_API_KEY` | ✅ **Yes** | ✅ Yes | Powers both LLM agents and Mem0 memory reasoning |
| `MONGO_DB_URL` | ✅ **Yes** | ✅ Yes (M0) | MongoDB Atlas connection string for session storage |
| `MLFLOW_TRACKING_URI` | ✅ **Yes** | ✅ Yes | DagsHub MLflow remote tracking server URI |
| `MLFLOW_TRACKING_USERNAME` | ✅ **Yes** | ✅ Yes | DagsHub account username |
| `MLFLOW_TRACKING_PASSWORD` | ✅ **Yes** | ✅ Yes | DagsHub access token |
| `MEM0_API_KEY` | ⚠️ Optional | ✅ Yes | Only required if using Mem0 cloud instead of local ChromaDB |
| `GITHUB_TOKEN` | ⚠️ CI/CD only | ✅ Yes | Personal Access Token for automated GitHub pushes |

---

## 🌐 Running the API

### Start the FastAPI Server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the web UI (HTML interface) |
| `POST` | `/plan` | Submit a trip planning request |
| `GET` | `/docs` | Interactive Swagger UI |
| `GET` | `/redoc` | ReDoc API documentation |

### Example Request

```bash
curl -X POST "http://localhost:8000/plan" \
  -H "Content-Type: application/json" \
  -d '{"content": "I want a 5-day trip to Paris focused on art and food", "source": "User"}'
```

### Example Response

```json
{
  "messages": [
    {
      "source": "planner",
      "content": "## Day 1 — Arrival & Montmartre\n- Settle into accommodation near Montmartre\n- Evening stroll to Sacré-Cœur..."
    },
    {
      "source": "researcher",
      "content": "## Day 1 — Arrival & Montmartre\n\n**Sacré-Cœur Basilica**\n- Best time: Early morning (8–10am) to beat crowds\n- Cost: Free entry..."
    }
  ]
}
```

### CLI Runner

For direct terminal execution without the API:

```bash
python main.py
```

---

## 📊 Experiment Tracking with MLflow

Every pipeline run is automatically logged to your DagsHub MLflow workspace.

```
Experiment: Holiday_Management_Agent
│
├── Run: paris_5day_trip
│   ├── params/
│   │   ├── model           = llama-3.1-8b-instant
│   │   ├── temperature     = 0.3
│   │   ├── max_tokens      = 1024
│   │   ├── destination     = Paris
│   │   └── duration_days   = 5
│   ├── metrics/
│   │   ├── draft_plan_chars    = 1842
│   │   ├── final_output_chars  = 3571
│   │   └── message_count       = 2
│   └── artifacts/
│       ├── phase7_draft_plan.md
│       └── phase7_final_itinerary.md
```

To view experiments locally:

```bash
mlflow ui --backend-store-uri ./mlruns
# Open: http://localhost:5000
```

---

## 🧠 Long-Term Memory with Mem0

The system uses **Mem0** backed by a local **ChromaDB** vector store to persist and retrieve user preferences across all sessions. No user needs to re-state their preferences on every new request.

**How it works:**

```python
# First session — user states a preference
memory.add("I prefer mountain hiking and cold climates.", user_id="traveller_001")

# Second session (weeks later) — agent retrieves it automatically
memory.search("What kind of trip suits this user?", filters={"user_id": "traveller_001"})
# → "mountain hiking and cold climates" is injected into the Planner's prompt
```

**Memory evolution is fully observable** — every `ADD`, `UPDATE`, and `DELETE` event is stored with timestamps and is queryable via `memory.history(memory_id=...)`.

---

## 🔄 CI/CD Pipeline

This project uses **GitHub Actions** for continuous integration and deployment.

### Workflow Triggers

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

### Pipeline Stages

```
Push to main
    │
    ▼
┌─────────────────┐
│   Lint & Format  │  ruff / black / isort
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Unit Tests     │  pytest (agents, validators, state)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Integration    │  End-to-end pipeline with mock LLM
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Deploy API     │  (configurable — cloud target)
└─────────────────┘
```

---

## 🗺️ Roadmap

- [x] Sequential multi-agent pipeline (Planner → Researcher)
- [x] Pydantic v2 input/output validation
- [x] Query transformation & normalization pipeline
- [x] Structured logging (console + file)
- [x] Mem0 long-term user memory (ChromaDB + Groq)
- [x] MLflow experiment tracking on DagsHub
- [x] FastAPI REST interface
- [x] GitHub Actions CI/CD
- [ ] **Parallel Researcher** — research multiple itinerary days concurrently
- [ ] **Real-time API tools** — Google Places, Booking.com, Skyscanner integrations
- [ ] **PDF Export** — convert Markdown itinerary to styled PDF via WeasyPrint
- [ ] **Budget Optimizer Agent** — third agent that minimizes cost while preserving quality
- [ ] **Voice Interface** — Whisper STT → Agent → TTS response loop
- [ ] **LangSmith Tracing** — per-token latency profiling for chain optimization
- [ ] **Docker Deployment** — containerized multi-service setup with docker-compose

---

## 🤝 Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to your branch: `git push origin feat/your-feature-name`
5. Open a Pull Request against `main`

Please ensure all new code passes the existing test suite and follows PEP 8 style conventions.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

---

<div align="center">

Built with 🧠 multi-agent reasoning · ⚡ Groq inference · 📊 MLflow observability

**[⬆ Back to Top](#️-personalized-holiday-management-agent)**

</div>
