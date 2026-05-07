# Automated Candidate Interview & Evaluation System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-≥1.2-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3-F55036?style=for-the-badge&logo=groq&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Free_Local-FF6B35?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

**An end-to-end AI-powered interview pipeline that autonomously conducts, evaluates, and reports on technical candidate interviews using a multi-agent LLM architecture.**

</div>

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Pipeline Phases](#pipeline-phases)
- [API Reference](#api-reference)
- [System Design Decisions](#system-design-decisions)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The **Automated Candidate Interview & Evaluation System** is a production-grade, multi-agent AI pipeline designed to streamline the technical screening process. It replaces manual first-round interviews with a structured, consistent, and bias-reduced evaluation loop powered by large language models.

The system orchestrates three specialised agents — an **Interviewer**, a **Candidate Proxy**, and an **Evaluator** — working in sequence to conduct role-specific interviews, provide per-answer coaching feedback, and generate a comprehensive final hiring report with a score and recommendation.

### Key Capabilities

- **Multi-Agent Orchestration** — Separate LLM agents for interviewing and evaluation, each with independent system prompts and token budgets
- **Role-Adaptive Questioning** — Dynamically tailors questions to the target job position across technical, problem-solving, and cultural-fit dimensions
- **Semantic Candidate Search** — ChromaDB vector store enables similarity-based retrieval of candidate profiles using free local embeddings
- **LangChain RAG Pipeline** — Retrieval-Augmented Generation allows context-aware Q&A over candidate profile collections
- **Resume Analysis Chain** — LCEL-based LangChain chain parses and scores resume excerpts against job requirements
- **Memory Observability** — Mem0 integration tracks how candidate preferences and data evolve across sessions
- **Structured I/O Validation** — Pydantic v2 models enforce strict type validation on all inputs and outputs
- **Query Intelligence** — Built-in query validation, stop-word removal, and synonym normalisation layer
- **Structured Logging** — Dual-handler logging (console + file) with configurable verbosity levels
- **Phase-by-Phase Output** — Every pipeline stage saves a JSON artifact for auditability and downstream processing

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Interview Pipeline                           │
│                                                                 │
│  ┌──────────────┐    ┌───────────────┐    ┌─────────────────┐  │
│  │  Interviewer │───▶│   Candidate   │───▶│    Evaluator    │  │
│  │   Agent      │    │    Proxy      │    │     Agent       │  │
│  │ (Instant LLM)│    │  (User/Auto)  │    │ (Versatile LLM) │  │
│  └──────────────┘    └───────────────┘    └─────────────────┘  │
│         │                                         │             │
│         ▼                                         ▼             │
│  ┌──────────────┐                       ┌─────────────────┐    │
│  │  3 Questions │                       │  Final Report   │    │
│  │  (Tech/PS/CF)│                       │  Score + Hire?  │    │
│  └──────────────┘                       └─────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Supporting Infrastructure                    │
│                                                                 │
│  ChromaDB ──── Semantic Profile Search ──── LangChain RAG      │
│  Mem0      ──── Memory Observability   ──── History Tracking   │
│  Pydantic  ──── I/O Validation         ──── Schema Enforcement │
│  LangChain ──── Resume Analysis Chain  ──── LCEL Pipelines     │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Roles

| Agent | Model | Role | Token Budget |
|---|---|---|---|
| Interviewer | `llama-3.1-8b-instant` | Generates role-specific questions | 300 |
| Evaluator (per-answer) | `llama-3.3-70b-versatile` | Provides real-time coaching feedback | 500 |
| Final Evaluator | `llama-3.3-70b-versatile` | Generates hire/no-hire report with score | 500 |
| Resume Analyzer | `llama-3.1-8b-instant` | Parses resume and returns structured JSON | 400 |
| RAG QA | `llama-3.3-70b-versatile` | Answers questions over candidate profiles | 300 |

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM Provider** | [Groq](https://groq.com) | Ultra-fast inference via GroqCloud API |
| **LLM Models** | LLaMA 3.1 8B Instant, LLaMA 3.3 70B Versatile | Speed/quality balance per task |
| **Orchestration** | [LangChain ≥ 1.2](https://python.langchain.com) | LCEL chains, prompts, RAG pipelines |
| **Vector Database** | [ChromaDB](https://trychroma.com) | Free, persistent local vector store |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` | Free local sentence embeddings |
| **Memory** | [Mem0](https://mem0.ai) | Cross-session memory with observability |
| **Validation** | [Pydantic v2](https://docs.pydantic.dev) | Strict I/O schema enforcement |
| **Web Layer** | FastAPI + WebSockets | Real-time interview streaming interface |
| **Frontend** | HTML / CSS / JavaScript | Chat-style interview UI |
| **Logging** | Python `logging` | Dual-channel structured logging |

---

## Project Structure

```
automated_interview_system/
│
├── main.py                          # Pipeline orchestrator — runs all phases
├── app.py                           # FastAPI server with WebSocket interview endpoint
├── agent_core.py                    # Groq multi-agent definitions and call wrappers
├── agent_test.py                    # Standalone agent smoke-test runner
├── requirements.txt                 # Python package dependencies
│
├── utilities/
│   ├── __init__.py
│   ├── pydantic_models.py           # SearchRequest / SearchResponse Pydantic v2 models
│   ├── query_validation_transformation.py  # Query sanitisation and normalisation
│   ├── logging_example.py           # App logger factory (console + file handlers)
│   └── mem0_example.py             # Mem0 memory add / update / search / history demo
│
├── static/
│   ├── script.js                    # WebSocket client logic for interview UI
│   └── style.css                    # Chat interface styling
│
├── db/                              # ChromaDB persistent storage (auto-created)
│
├── outputs/                         # Phase output artifacts (auto-created)
│   ├── phase3_pydantic.json
│   ├── phase4_query.json
│   ├── phase5_logging.json
│   ├── phase6_chromadb.json
│   ├── phase7_langchain.json
│   ├── phase8_interview.json
│   ├── phase9_mem0.json
│   ├── phase10_rag.json
│   └── SUMMARY_REPORT.json
│
└── logs/                            # Application logs (auto-created)
    └── utility_logging_example.log
```

---

## Prerequisites

- Python **3.10 or higher**
- A **Groq API key** — free tier available at [console.groq.com](https://console.groq.com)
- *(Optional)* A **Mem0 API key** for cloud memory features — [app.mem0.ai](https://app.mem0.ai)

> ChromaDB and all embeddings run entirely locally — no additional API keys are required for vector storage or semantic search.

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-org/automated-interview-system.git
cd automated-interview-system
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**Full dependency list:**

```
groq
langchain>=0.1.20
langchain-core>=0.1.52
langchain-groq>=0.1.3
langchain-community>=0.0.38
langchain-chroma>=0.1.1
chromadb>=0.4.22
pydantic>=2.0,<3.0
mem0ai
sentence-transformers
python-dotenv
nest_asyncio
fastapi
uvicorn[standard]
websockets
```

---

## Configuration

Create a `.env` file in the project root:

```env
# Required
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional — enables cloud memory features
MEM0_API_KEY=your_mem0_api_key_here
```

The system reads these at startup via `python-dotenv`. Never commit your `.env` file — it is already listed in `.gitignore`.

---

## Usage

### Run the Full Pipeline

Executes all phases sequentially and saves JSON output artifacts:

```bash
python main.py
```

### Start the Web Interview Server

Launches the FastAPI server with a real-time WebSocket-powered interview interface:

```bash
uvicorn app:app --reload --port 8000
```

Then open `http://localhost:8000` in your browser, enter a job position, and begin the interview.

### Run the Agent in Terminal Mode

Runs an interactive terminal-based interview session:

```bash
python agent_test.py
```

---

## Pipeline Phases

The system executes the following phases in order, each producing a JSON output artifact:

| Phase | Module | Description | Output |
|---|---|---|---|
| **3** | `pydantic_models.py` | Validates `SearchRequest` and builds `SearchResponse` | `phase3_pydantic.json` |
| **4** | `query_validation_transformation.py` | Sanitises, normalises, and transforms queries | `phase4_query.json` |
| **5** | `logging_example.py` | Initialises dual-handler logging and runs demo | `phase5_logging.json` |
| **6** | ChromaDB | Embeds and stores candidate profiles; runs semantic search | `phase6_chromadb.json` |
| **7** | LangChain LCEL | Resume analysis chain using `ChatPromptTemplate` + `StrOutputParser` | `phase7_langchain.json` |
| **8** | `agent_core.py` | Full 3-question multi-agent interview with per-answer feedback and final report | `phase8_interview.json` |
| **9** | `mem0_example.py` | Stores preferences, triggers updates, retrieves memory history | `phase9_mem0.json` |
| **10** | LangChain RAG | Retrieval-Augmented Q&A over ChromaDB candidate profile collection | `phase10_rag.json` |
| **11** | — | Consolidates all phase results into a single summary | `SUMMARY_REPORT.json` |

---

## API Reference

### WebSocket — `/ws/interview`

Establishes a real-time interview session.

**Query Parameter:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pos` | `string` | `"AI Engineer"` | The job position for the interview |

**Message Protocol:**

| Direction | Prefix | Description |
|---|---|---|
| Server → Client | `SYSTEM_INFO:` | Informational status messages |
| Server → Client | `SYSTEM_TURN:USER` | Signals that candidate input is expected |
| Server → Client | `SYSTEM_END:` | Interview concluded; includes stop reason |
| Server → Client | `Interviewer:` | Interviewer message content |
| Server → Client | `Evaluator:` | Evaluator feedback content |
| Client → Server | *(plain text)* | Candidate's answer |

### REST — `GET /`

Returns the interview UI HTML page.

---

## System Design Decisions

**Why Groq over OpenAI?**
Groq provides significantly faster inference at competitive cost. `llama-3.1-8b-instant` is used where speed matters (interviewer, resume parser) and `llama-3.3-70b-versatile` where reasoning depth is needed (evaluator, RAG).

**Why ChromaDB?**
ChromaDB runs fully locally with zero configuration and no API key, making it ideal for persistent vector storage without external dependencies or cost. It integrates natively with LangChain via `langchain-chroma`.

**Why separate Interviewer and Evaluator agents?**
Separating concerns ensures the interviewer stays focused on eliciting responses without being distracted by coaching logic. The evaluator operates on isolated question/answer pairs, producing cleaner, more consistent feedback.

**Why Pydantic v2?**
Pydantic v2 provides faster validation, better error messages, and full compatibility with the LangChain ecosystem. All external I/O passes through validated models to prevent malformed data propagating through the pipeline.

**Token budget rationale:**
Groq's free tier enforces requests-per-minute limits. Token budgets are set conservatively (`instant`: 300–400, `versatile`: 500) to maximise throughput across the multi-step pipeline without hitting rate limits.

---

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes with clear, descriptive messages
4. Open a pull request with a summary of changes and any relevant context

Please ensure all new modules include type annotations, docstrings, and logging hooks consistent with the existing codebase.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full terms.

---

<div align="center">

Built with [Groq](https://groq.com) · [LangChain](https://python.langchain.com) · [ChromaDB](https://trychroma.com) · [Mem0](https://mem0.ai)

</div>
