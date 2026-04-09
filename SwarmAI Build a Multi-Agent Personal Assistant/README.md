# SwarmAI — Multi-Agent Personal Assistant

> **End-to-end Agentic AI system** that interprets natural language and autonomously routes tasks across specialised AI agents — managing emails, calendars, travel planning, and real-time research through a unified conversational interface.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![GROQ](https://img.shields.io/badge/LLM-GROQ%20%7C%20Llama--3.3--70b-F55036?style=flat-square)](https://groq.com)
[![MLflow](https://img.shields.io/badge/Tracking-MLflow%20%2B%20DagsHub-0194E2?style=flat-square&logo=mlflow)](https://mlflow.org)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://mongodb.com)
[![n8n](https://img.shields.io/badge/Automation-n8n-EA4B71?style=flat-square)](https://n8n.io)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Agent Roster](#agent-roster)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Agent Routing Logic](#agent-routing-logic)
- [Compound Query Examples](#compound-query-examples)
- [Experiment Tracking](#experiment-tracking)
- [Data Persistence](#data-persistence)
- [Design Principles](#design-principles)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

---

## Overview

**SwarmAI** is a production-grade, multi-agent orchestration system built on the principles of **Agentic AI** and **Generative AI**. It takes a single natural language query — text, voice, or image — and intelligently decomposes it into subtasks, routes each to the correct specialised agent, and merges the outputs into one coherent response.

Unlike monolithic AI assistants, SwarmAI follows a **modular swarm architecture**: each agent is an independent, domain-expert system. The **Main Routing Agent** acts as an intelligent dispatcher — it never executes tasks itself; it reasons about intent, determines the correct agent sequence, and chains outputs forward.

**What makes it end-to-end agentic:**

- **Perception** — accepts multimodal input (text, voice transcription, image analysis)
- **Reasoning** — LLM-powered intent detection and routing plan generation
- **Action** — agents autonomously operate real-world APIs (Gmail, Google Calendar, SerpAPI)
- **Memory** — full conversation and agent-run persistence in MongoDB
- **Observability** — every run tracked in MLflow / DagsHub with latency metrics and outputs

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                               │
│              (Text  │  Voice  │  Image via Telegram)            │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MAIN ROUTING AGENT                            │
│                                                                 │
│  • Detects intent from natural language                         │
│  • Resolves compound queries into sequential subtasks           │
│  • Generates structured routing plan  { agents: [...] }         │
│  • Normalises all dates → ISO 8601 (Asia/Kolkata +05:30)        │
│  • Asks for clarification only when critical info is missing    │
│                                                                 │
│  Model: GROQ  llama-3.3-70b-versatile                          │
└──────┬──────────┬──────────┬──────────┬───────────────────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
  │ Email  │ │Calendar│ │ Travel │ │ Research │
  │ Agent  │ │ Agent  │ │ Agent  │ │  Agent   │
  └────┬───┘ └────┬───┘ └────┬───┘ └────┬─────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
     Gmail   G-Calendar   SerpAPI  Tavily + Wikipedia
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              OUTPUT MERGER  →  Telegram-safe Plain Text         │
└─────────────────────────────────────────────────────────────────┘
       │                         │
       ▼                         ▼
  MongoDB                     MLflow
  (Conversations              (Run metrics,
   + Agent Logs)               latency, outputs)
```

**Sequential chaining** means each agent receives the outputs of all previously executed agents as context, enabling coherent multi-step workflows like: *find flight → add to calendar → email itinerary* in a single user query.

---

## Agent Roster

### 🧭 Main Routing Agent
The orchestrator brain. Receives every user message, analyses intent, and produces a JSON routing plan specifying which agents to invoke and in what order. It never touches external APIs directly — pure reasoning and delegation.

| Property | Detail |
|---|---|
| Model | `llama-3.3-70b-versatile` via GROQ |
| Input | Raw user query (text / transcribed voice / image description) |
| Output | Structured routing plan + merged final summary |
| Timezone | ISO 8601 — Asia/Kolkata (+05:30) enforced universally |

---

### 📩 Email Agent
Autonomous Gmail operations. Handles the full email lifecycle without human intervention beyond the initial instruction.

**Capabilities:**
- Send emails with inferred or explicit subject lines
- Read, search, and summarise unread messages
- Reply to existing threads
- Delete with confirmation guard on mass operations

**Example output:**
```
Action: Email Sent
To: hr@company.com
Subject: Leave Request — Next Monday
Timestamp: 2025-11-07T09:00:00+05:30
Status: Success
— End of results —
```

---

### 📅 Calendar Agent
Full Google Calendar management with conflict detection and availability awareness.

**Capabilities:**
- Create, update, and delete events
- Check availability across date ranges
- Detect and resolve scheduling conflicts with polite alternatives
- List upcoming events by date range

**Example output:**
```
Action: Event Created
Title: Team Sync
Start: 2025-11-08T15:00:00+05:30
End:   2025-11-08T16:00:00+05:30
Status: Confirmed
— End of results —
```

---

### ✈️ Travel Agent
Real-time flight and hotel discovery via SerpAPI with intelligent defaults.

**Capabilities:**
- Flights: search by route, date, class, and number of passengers
- Hotels: search by city, check-in/out dates, star rating, and guest score
- Suggests alternative dates or airports when no results are found

**Defaults:** One-way · 1 adult · Economy · 4★+ hotels · Rating ≥ 8

**Example output:**
```
Search Results: Flights
1) Air India — DEL → BOM
   Departure: 2025-06-10T09:00:00+05:30
   Price: ₹5,200
2) IndiGo — DEL → BOM
   Departure: 2025-06-10T14:00:00+05:30
   Price: ₹5,000
— End of results —
```

---

### 🔍 Research Agent
Real-time knowledge retrieval combining Wikipedia (structured background) and Tavily Search (live updates).

**Tool selection logic:**
- **Wikipedia** → definitions, concepts, historical background
- **Tavily** → current events, trending topics, recent releases
- **Combined** → when both context and recency are required (e.g. *"latest ChatGPT updates"*)

**Example output:**
```
ChatGPT is a conversational AI system by OpenAI.
Recent updates (2025-11-07T00:00:00+05:30):
- Introduced persistent memory recall
- Faster inference response times
- Expanded voice mode availability
— End of results —
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| **LLM Inference** | [GROQ API](https://groq.com) — `llama-3.3-70b-versatile` |
| **Agent Orchestration** | Python — custom swarm router |
| **Workflow Automation** | [n8n](https://n8n.io) — visual agent workflows |
| **Email Integration** | Gmail API |
| **Calendar Integration** | Google Calendar API |
| **Travel Search** | SerpAPI (Flights + Hotels) |
| **Web Research** | Tavily Search + Wikipedia API |
| **Database** | MongoDB — conversation + agent log persistence |
| **Experiment Tracking** | MLflow + DagsHub |
| **Messaging Interface** | Telegram Bot API |
| **Input Modes** | Text · Voice (transcription) · Image (vision analysis) |

---

## Project Structure

```
SwarmAI/
│
├── SwarmAI_Colab.ipynb          # End-to-end executable notebook
│
├── workflows/                   # n8n workflow definitions (importable JSON)
│   ├── Main Workflow.json        # Main Routing Agent — Gemini powered
│   ├── Email Workflow.json       # Email Agent workflow
│   ├── Calendar Workflow.json    # Calendar Agent workflow
│   ├── Travel Agent.json         # Travel Agent workflow
│   └── Research Agent.json       # Research Agent workflow
│
├── prompt.txt                   # All agent system prompts (source of truth)
├── Swarm_Readme.md              # Architecture reference
└── README.md                    # This file
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- MongoDB instance (Atlas free tier works)
- GROQ API key — [console.groq.com](https://console.groq.com)
- DagsHub account for MLflow tracking (optional — local tracking also supported)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/swarm-ai.git
cd swarm-ai
```

### 2. Install dependencies

```bash
pip install groq pymongo mlflow dagshub requests
```

### 3. Set environment variables

```bash
export MONGO_DB_URL="mongodb+srv://..."
export GROQ_API_KEY="gsk_..."
export MLFLOW_TRACKING_URI="https://dagshub.com/username/swarm-ai.mlflow"
export MLFLOW_TRACKING_USERNAME="your-dagshub-username"
export MLFLOW_TRACKING_PASSWORD="your-dagshub-token"
```

> For local MLflow tracking (no DagsHub), set:
> ```bash
> export MLFLOW_TRACKING_URI="file://$(pwd)/mlruns"
> ```

### 4. Run the swarm

```python
from swarm import run_swarm

# Single agent
result = run_swarm("What is Retrieval Augmented Generation?")

# Two-agent chain
result = run_swarm("Research the latest AI trends and email me a summary.")

# Three-agent chain
result = run_swarm(
    "Book a flight to Tokyo on July 10, add it to my calendar, "
    "and email me the itinerary."
)
```

---

## Configuration

| Environment Variable | Required | Description |
|---|---|---|
| `MONGO_DB_URL` | ✅ | MongoDB connection string |
| `GROQ_API_KEY` | ✅ | GROQ API key for LLM inference |
| `MLFLOW_TRACKING_URI` | ✅ | MLflow tracking server URI |
| `MLFLOW_TRACKING_USERNAME` | If DagsHub | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | If DagsHub | DagsHub access token |

**Model selection** — change the default model in `call_groq()`:

```python
def call_groq(system_prompt, user_message, model="llama-3.3-70b-versatile"):
    ...
```

Supported GROQ production models as of April 2026:

| Model ID | Best For |
|---|---|
| `llama-3.3-70b-versatile` | **Default** — general purpose, agentic tasks |
| `llama-3.1-8b-instant` | High-throughput, cost-sensitive routing |
| `llama-4-scout-17b-16e-instruct` | Vision + multimodal inputs |
| `qwen/qwen3-32b` | Reasoning-heavy research tasks |

---

## Agent Routing Logic

The Main Routing Agent returns a structured JSON plan before any sub-agent is invoked:

```json
{
  "intent_summary": "Find flights to Tokyo, create a calendar event, send itinerary email",
  "agents": ["TravelAgent", "CalendarAgent", "EmailAgent"],
  "routing_order": "TravelAgent -> CalendarAgent -> EmailAgent",
  "needs_clarification": false,
  "clarification_question": ""
}
```

Agents are then executed **sequentially**. Each agent receives:
1. The original user query
2. The concatenated outputs of all previously executed agents as context

This context chaining is what enables coherent compound workflows — the Email Agent, for example, can reference the actual flight details discovered by the Travel Agent.

---

## Compound Query Examples

| User Query | Agent Sequence | Outcome |
|---|---|---|
| `"Send an email to HR about my leave."` | Email | Email sent, confirmation returned |
| `"Schedule a team sync tomorrow at 3 PM."` | Calendar | Event created with IST timestamp |
| `"Find flights Delhi → Mumbai on June 10."` | Travel | Top 3–5 options with prices |
| `"What is RAG in AI?"` | Research | Wikipedia + Tavily summary |
| `"Research OpenAI updates and email summary."` | Research → Email | Research summary emailed |
| `"Find hotels in Goa, July 5–7, add reminder."` | Travel → Calendar | Hotel options + reminder event |
| `"Book Tokyo flight July 10, calendar it, email itinerary."` | Travel → Calendar → Email | Full end-to-end execution |
| `"Check unread emails and schedule follow-ups."` | Email → Calendar | Emails surfaced, follow-up events created |

---

## Experiment Tracking

Every `run_swarm()` call is logged as an MLflow run with:

| Logged Item | Type |
|---|---|
| `query` | Parameter |
| `agents_used` | Parameter (routing order string) |
| `num_agents` | Parameter |
| `latency_sec` | Metric |
| `final_output.txt` | Artifact |
| `{AgentName}_output.txt` | Artifact (one per agent) |

View runs in the DagsHub MLflow UI or locally:

```bash
mlflow ui --backend-store-uri ./mlruns
# → http://localhost:5000
```

---

## Data Persistence

All interactions are stored in MongoDB across two collections:

**`conversations`** — one document per user interaction:
```json
{
  "timestamp": "2025-11-07T09:00:00Z",
  "query": "Book flight to Tokyo...",
  "routing_plan": { "agents": [...], "routing_order": "..." },
  "final_output": "Search Results: Flights\n1) ..."
}
```

**`agent_logs`** — one document per agent execution:
```json
{
  "timestamp": "2025-11-07T09:00:01Z",
  "agent": "TravelAgent",
  "query": "Book flight to Tokyo...",
  "output": "Search Results: Flights\n..."
}
```

This separation allows independent analysis of routing patterns, agent performance, and output quality over time.

---

## Design Principles

**Agentic Modularity** — each agent is a fully independent unit with its own system prompt, toolset, and output contract. Agents can be updated, swapped, or extended without touching the orchestrator.

**Sequential Context Chaining** — rather than broadcasting the original query to all agents in parallel, SwarmAI chains outputs forward. This produces coherent multi-step results where later agents build on earlier ones.

**Separation of Reasoning and Execution** — the Main Routing Agent performs pure reasoning (no API calls). Sub-agents perform pure execution (no routing). This clean separation makes the system debuggable, observable, and extensible.

**Timezone Uniformity** — all timestamps are normalised to ISO 8601 with Asia/Kolkata (+05:30) at the routing layer, before any agent receives the query. No agent needs to handle timezone conversion independently.

**Minimal Clarification** — the system infers defaults aggressively (one-way flight, economy class, tomorrow at 09:00, etc.) and only asks for clarification when a query is genuinely ambiguous or missing a value that cannot be inferred.

**Full Observability** — every run produces a MongoDB document and an MLflow experiment entry, enabling complete replay, debugging, and performance analysis without relying on logs.

---

## Roadmap

- [ ] Voice input pipeline (Whisper transcription → swarm)
- [ ] Image understanding via vision LLM → swarm routing
- [ ] Slack / WhatsApp interface alongside Telegram
- [ ] Agent memory: cross-session user preference learning
- [ ] Parallel agent execution for independent subtasks
- [ ] Web UI dashboard (agent trace visualisation)
- [ ] LangGraph / CrewAI backend option

---

## Contributing

Contributions are welcome. Please open an issue first to discuss the change, then submit a pull request with:

- A clear description of what was changed and why
- Updated documentation where relevant
- No breaking changes to existing agent prompt contracts without discussion

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with 🧠 Agentic AI · GROQ · MongoDB · MLflow · n8n

</div>
