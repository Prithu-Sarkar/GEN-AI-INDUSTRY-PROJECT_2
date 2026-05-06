# ClinisightAI — Medical Diagnosis & Research Assistant

<p align="center">
  <img src="architecture.jpg" alt="ClinisightAI Architecture" width="720"/>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.13+"/></a>
  <a href="#"><img src="https://img.shields.io/badge/FastAPI-0.121+-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/></a>
  <a href="#"><img src="https://img.shields.io/badge/MCP-1.21+-6C47FF?style=flat-square&logo=anthropic&logoColor=white" alt="MCP"/></a>
  <a href="#"><img src="https://img.shields.io/badge/OpenAI-GPT--4-412991?style=flat-square&logo=openai&logoColor=white" alt="OpenAI GPT-4"/></a>
  <a href="#"><img src="https://img.shields.io/badge/PubMed-NCBI-326599?style=flat-square&logo=pubmed&logoColor=white" alt="PubMed"/></a>
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License"/></a>
</p>

> **ClinisightAI** is a production-ready AI-powered medical diagnosis and research assistant that combines GPT-4 clinical reasoning with real-time PubMed literature retrieval. It is exposed as both a REST API (FastAPI) and an agentic tool via the **Model Context Protocol (MCP)**, enabling seamless integration into AI agent workflows.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
  - [FastAPI Server](#fastapi-server)
  - [MCP Server](#mcp-server)
- [API Reference](#api-reference)
- [MCP Tool Reference](#mcp-tool-reference)
- [Pipeline Walkthrough](#pipeline-walkthrough)
- [Technologies](#technologies)
- [Development](#development)
- [Disclaimer](#disclaimer)

---

## Overview

ClinisightAI accepts a free-text description of a patient's symptoms and runs it through a four-stage automated pipeline:

1. **Symptom Extraction** — regex-based NLP to identify clinical symptoms in natural language
2. **LLM Diagnosis** — GPT-4 generates a structured differential diagnosis and recommended treatment approach
3. **PubMed Research** — live article retrieval via the NCBI E-utilities API with full metadata (title, authors, publication date, abstract, URL)
4. **Research Summarization** — GPT-4 synthesises retrieved abstracts into a concise clinical summary

The application is dual-mode: it serves as a standard HTTP API for programmatic integrations, and as an **MCP tool** that can be plugged directly into any MCP-compatible AI agent (Claude Desktop, custom agents, orchestration frameworks).

---

## Features

- **Natural Language Symptom Parsing** — no structured input required; accepts plain patient descriptions
- **GPT-4 Differential Diagnosis** — clinically-aware prompt engineering with cure suggestions
- **Live PubMed Integration** — fetches real articles from the NCBI E-utilities API, not a static database
- **Intelligent Fallback** — returns curated mock data when PubMed is unreachable, ensuring zero downtime
- **FastAPI REST Endpoint** — production-ready HTTP API with Pydantic input validation and auto-generated OpenAPI docs
- **MCP Server** — exposes the full pipeline as an agentic tool via the Model Context Protocol, installable in Claude Desktop with a single command
- **Modular Architecture** — each pipeline stage is an independent, importable Python module
- **Environment-Based Config** — all secrets managed via `.env`, never hardcoded

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client / Agent                       │
│              (HTTP Client  |  MCP-compatible Agent)         │
└──────────────────────┬──────────────────┬───────────────────┘
                       │                  │
              REST POST /diagnosis    MCP Tool Call
                       │                  │
              ┌────────▼──────────────────▼────────┐
              │           app.py / mcp_tool.py      │
              │     (FastAPI  |  FastMCP Server)     │
              └────────────────┬────────────────────┘
                               │
          ┌────────────────────▼─────────────────────┐
          │            Pipeline Orchestration          │
          └──┬──────────────┬──────────┬──────────────┘
             │              │          │
    ┌────────▼───┐  ┌───────▼────┐  ┌─▼──────────────────┐
    │  Symptom   │  │  Diagnosis │  │   PubMed Fetcher    │
    │ Extractor  │  │  (GPT-4)   │  │  (NCBI E-utilities) │
    └────────────┘  └───────┬────┘  └────────┬────────────┘
                            │                 │
                        Diagnosis         Articles
                            │                 │
                            └────────┬────────┘
                                     │
                            ┌────────▼────────┐
                            │  Summarizer     │
                            │   (GPT-4)       │
                            └─────────────────┘
                                     │
                              Final Response
                    { symptoms, diagnosis, articles, summary }
```

---

## Project Structure

```
Medical Diagnosis App/
├── app.py                          # FastAPI application — REST API server
├── mcp_tool.py                     # MCP server — agentic tool via FastMCP
├── main.py                         # Package entry point
├── pyproject.toml                  # Project metadata and dependencies (uv)
├── requirements.txt                # pip-compatible dependency list
├── architecture.jpg                # System architecture diagram
├── demo.excalidraw                 # Editable architecture diagram source
├── metadata.txt                    # Project learning outcomes & spec
├── README.md                       # This file
└── functions/
    ├── __init__.py
    ├── symptom_extractor.py        # Stage 1: NLP symptom extraction
    ├── diagnosis_symptoms.py       # Stage 2: GPT-4 differential diagnosis
    ├── pubmed_articles.py          # Stage 3: Live PubMed article retrieval
    └── summerize_pubmed.py         # Stage 4: GPT-4 research summarization
```

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | ≥ 3.13 | Required for modern type hints |
| uv | latest | Recommended package manager |
| OpenAI API Key | — | GPT-4 access required |
| Internet access | — | Required for PubMed E-utilities |

---

## Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/clinisight-ai.git
cd "clinisight-ai/Medical Diagnosis App"

# Install dependencies
uv sync
```

### Using pip

```bash
git clone https://github.com/your-org/clinisight-ai.git
cd "clinisight-ai/Medical Diagnosis App"

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and provide your credentials:

```dotenv
# Required — OpenAI API key with GPT-4 access
OPENAI_API_KEY=sk-...your-key-here...
```

> **Security:** Never commit `.env` to version control. It is included in `.gitignore` by default.

---

## Running the Application

### FastAPI Server

Start the REST API server:

```bash
# Using uv
uv run uvicorn app:app --host 0.0.0.0 --port 8080 --reload

# Using Python directly
python app.py
```

The server will be available at:

| Endpoint | URL |
|---|---|
| API base | `http://localhost:8080` |
| Interactive docs (Swagger) | `http://localhost:8080/docs` |
| ReDoc | `http://localhost:8080/redoc` |
| OpenAPI schema | `http://localhost:8080/openapi.json` |

---

### MCP Server

ClinisightAI ships with a full **Model Context Protocol** server, allowing any MCP-compatible AI agent to invoke the diagnosis pipeline as a native tool.

#### Install into Claude Desktop

```bash
mcp install mcp_tool.py
```

#### Run in development mode (with MCP Inspector)

```bash
uv run mcp dev mcp_tool.py
```

The MCP Inspector launches at `http://localhost:5173` and lets you test tool calls interactively before connecting to a live agent.

#### How it works

`mcp_tool.py` registers a single tool — `clinisight_ai` — via `FastMCP`. When an AI agent invokes this tool with a symptom description, the full four-stage pipeline runs and the structured result is returned to the agent as context.

```python
# The MCP tool signature
async def clinisight_ai(symptom_text: str) -> dict:
    """
    Analyse patient symptoms and return diagnosis + PubMed research.
    """
```

Once installed, Claude Desktop (or any MCP-compatible agent) can call this tool naturally:

> *"The patient reports headache, fever, and nausea for two days. Use ClinisightAI to analyse these symptoms."*

The agent automatically invokes `clinisight_ai`, receives the structured response, and incorporates it into its reply.

---

## API Reference

### `POST /diagnosis`

Runs the full medical diagnosis and research pipeline on a patient's symptom description.

**Request**

```http
POST /diagnosis
Content-Type: application/json
```

```json
{
  "description": "I have been experiencing a severe headache, high fever, nausea, and extreme fatigue for two days."
}
```

**Response** `200 OK`

```json
{
  "symptom": ["headache", "fever", "nausea", "fatigue"],
  "diagnosis": "Based on the presented symptoms, possible diagnoses include:\n\n1. **Viral Syndrome / Influenza** — The combination of fever, headache, fatigue, and nausea is characteristic...\n\n**Recommended approach:** ...",
  "pubmed_summary": "Recent literature suggests that febrile illness with concurrent cephalgia and constitutional symptoms in adults most commonly represents..."
}
```

**Response Fields**

| Field | Type | Description |
|---|---|---|
| `symptom` | `string[]` | Deduplicated list of extracted clinical symptoms |
| `diagnosis` | `string` | GPT-4 generated differential diagnosis and treatment suggestions |
| `pubmed_summary` | `string` | GPT-4 summary of the top 3 retrieved PubMed abstracts |

**Error Responses**

| Status | Description |
|---|---|
| `422 Unprocessable Entity` | Invalid or missing `description` field |
| `500 Internal Server Error` | LLM or upstream service failure |

**Example — cURL**

```bash
curl -X POST http://localhost:8080/diagnosis \
  -H "Content-Type: application/json" \
  -d '{"description": "Patient reports persistent back pain, fatigue, and joint pain for one week."}'
```

**Example — Python**

```python
import requests

response = requests.post(
    "http://localhost:8080/diagnosis",
    json={"description": "I have a sore throat, fever, and swollen lymph nodes."}
)
print(response.json())
```

---

## MCP Tool Reference

### `clinisight_ai`

**Description:** Analyses a patient's symptom description through the full ClinisightAI pipeline — symptom extraction, GPT-4 diagnosis, PubMed retrieval, and research summarization.

**Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `symptom_text` | `string` | ✅ | Free-text description of patient symptoms in natural language |

**Returns**

```json
{
  "symptom": ["string"],
  "diagnosis_result": "string",
  "pubmed_summary": "string"
}
```

**Usage in Claude Desktop**

After running `mcp install mcp_tool.py`, the tool appears automatically in Claude Desktop's tool palette. You can invoke it via natural language:

> *"Use ClinisightAI to evaluate these symptoms: persistent cough, shortness of breath, and chest tightness."*

---

## Pipeline Walkthrough

The following describes the internal execution flow for a single request:

```
Input: "I have a fever, headache, and I feel nauseous."
         │
         ▼
[1] symptom_extractor.extract_symptoms()
    → Regex scan against symptom vocabulary
    → Returns: ["fever", "headache", "nausea"]
         │
         ▼
[2] diagnosis_symptoms.get_diagnosis(["fever", "headache", "nausea"])
    → Constructs clinical prompt
    → Calls GPT-4: "Patient has symptoms: fever, headache, nausea. Suggest possible diagnosis and cure."
    → Returns structured diagnosis string
         │
         ▼
[3] pubmed_articles.fetch_pubmed_articles_with_metadata("fever headache nausea")
    → GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term=...
    → Retrieves up to 3 PubMed article IDs
    → GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?id=...
    → Parses XML: title, abstract, authors, publication date, URL
    → Falls back to mock data if no results found
         │
         ▼
[4] summerize_pubmed.summarize_text(abstracts[:3000])
    → Concatenates top 3 abstracts (capped at 3,000 characters)
    → Calls GPT-4: "Summarize the following medical abstract: ..."
    → Returns concise research summary
         │
         ▼
Output: { symptom, diagnosis, pubmed_summary }
```

---

## Technologies

| Category | Technology | Version |
|---|---|---|
| Language | Python | ≥ 3.13 |
| Web Framework | FastAPI | ≥ 0.121 |
| ASGI Server | Uvicorn | ≥ 0.38 |
| LLM | OpenAI GPT-4 | via `openai` ≥ 2.8 |
| AI Agent Protocol | Model Context Protocol (FastMCP) | ≥ 1.21 |
| Medical Research | NCBI PubMed E-utilities API | — |
| HTML Parsing | BeautifulSoup4 + LXML | ≥ 4.14 / ≥ 6.0 |
| HTTP Client | Requests | ≥ 2.32 |
| Config Management | python-dotenv | ≥ 1.2 |
| Package Manager | uv | latest |

---

## Development

### Running Tests

```bash
# Install dev dependencies
uv sync --dev

# Run test suite
uv run pytest tests/ -v
```

### Code Quality

```bash
# Linting
uv run ruff check .

# Type checking
uv run mypy .

# Formatting
uv run ruff format .
```

### Adding New Symptoms

The symptom vocabulary is maintained in `functions/symptom_extractor.py`. To extend it, add patterns to the regex list:

```python
symptoms = re.findall(
    r"\b(headache|fever|nausea|fatigue|pain|your_new_symptom)\b",
    text.lower()
)
```

### Extending the Pipeline

Each pipeline stage is an independent module. To add a new stage (e.g., drug interaction checking), create `functions/drug_interactions.py`, implement the function, and import it in both `app.py` and `mcp_tool.py`.

---

## Disclaimer

> **ClinisightAI is not a medical device and is not intended for clinical use.**
>
> The information generated by this application — including diagnoses, treatment suggestions, and research summaries — is produced by AI models and automated retrieval systems. It has not been validated by medical professionals and **must not be used as a substitute for professional medical advice, diagnosis, or treatment.**
>
> Always consult a qualified healthcare provider for any medical concerns. In a medical emergency, contact your local emergency services immediately.

---

<p align="center">
  Built with FastAPI · OpenAI GPT-4 · Model Context Protocol · PubMed NCBI
</p>
