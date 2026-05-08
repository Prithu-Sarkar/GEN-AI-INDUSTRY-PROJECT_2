# RAG Voice AI Agent

> A production-grade, real-time voice AI assistant with Retrieval-Augmented Generation (RAG), designed for enterprise call-center support automation. The agent listens to a caller in real time, retrieves grounded answers from a structured knowledge base, and responds with synthesized speech — all within a sub-second pipeline.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?style=flat-square&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![CI](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Local Development](#local-development)
- [API Reference](#api-reference)
- [RAG Pipeline](#rag-pipeline)
- [Voice Pipeline](#voice-pipeline)
- [CI/CD & Deployment](#cicd--deployment)
- [Configuration Reference](#configuration-reference)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The RAG Voice AI Agent is a full-stack system that enables human call-center agents to receive real-time AI assistance during live customer calls. When a customer asks a question, the system:

1. Transcribes speech to text via **Deepgram STT**
2. Passes the query to a **Groq LLM** (llama-3.1-8b-instant / llama-3.3-70b-versatile)
3. The LLM invokes a `search_knowledge_base` tool call
4. The **RAG service** retrieves the top-k semantically relevant chunks from **MongoDB Atlas Vector Search**
5. The LLM generates a concise, grounded answer (optimized for speech, under 30 words)
6. **ElevenLabs TTS** synthesizes the answer and streams it back to the agent

The system is multi-tenant, equipment-scoped, and designed for horizontal scale on AWS ECS.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Client Layer                                 │
│   React + Vite  │  Pipecat RTVI WebSocket Client  │  Browser Audio  │
└────────────────────────────┬────────────────────────────────────────┘
                             │ WebSocket (wss://)
┌────────────────────────────▼────────────────────────────────────────┐
│                        Backend Layer                                 │
│                                                                      │
│   FastAPI (Python 3.12)  ──────────────────────────────────────┐    │
│   ├── /api/v1/equipment   (CRUD + document ingestion)          │    │
│   └── /api/v1/stream      (WebSocket bot connect)              │    │
│                                                                 │    │
│   Pipecat Pipeline                                             │    │
│   ┌──────────┐   ┌────────────┐   ┌──────────┐   ┌────────┐  │    │
│   │ Deepgram │──▶│  Groq LLM  │──▶│   RAG    │──▶│  TTS   │  │    │
│   │   STT    │   │  + Tools   │   │ Service  │   │ (11L)  │  │    │
│   └──────────┘   └────────────┘   └──────────┘   └────────┘  │    │
└─────────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                         Data Layer                                   │
│   MongoDB Atlas (M0+)                                                │
│   ├── equipment            (equipment registry)                      │
│   ├── documents_metadata   (file metadata + embedding status)        │
│   └── document_chunks      (text chunks + 384-dim embeddings)        │
│                                                                      │
│   Atlas Vector Search Index  ──  cosine similarity over embeddings   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend Framework** | FastAPI 0.111+ (Python 3.12) |
| **LLM** | Groq API — `llama-3.1-8b-instant` / `llama-3.3-70b-versatile` |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` (384-dim, local inference) |
| **Vector Database** | MongoDB Atlas Vector Search |
| **STT** | Deepgram Nova-2 |
| **TTS** | ElevenLabs Turbo v2.5 |
| **Voice Pipeline** | Pipecat |
| **Frontend** | React 18 + Vite + TypeScript |
| **ODM / Async DB** | Motor (async MongoDB driver) |
| **Data Validation** | Pydantic v2 + pydantic-settings |
| **LangChain** | `>=0.2.0` — text splitting + embeddings (`langchain-community`, `langchain-text-splitters`) |
| **Containerization** | Docker + Docker Compose |
| **CI/CD** | GitHub Actions → Docker Hub |
| **Logging** | Loguru |

---

## Project Structure

```
rag-voice-ai-agent/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                  # Pydantic settings — all env vars
│   │   ├── database.py                # Motor async MongoDB connection
│   │   ├── bot.py                     # Pipecat pipeline + Groq LLM + tool schema
│   │   │
│   │   ├── models/
│   │   │   ├── document.py            # Document metadata model
│   │   │   ├── equipment.py           # Equipment model
│   │   │   └── rag.py                 # RAG retrieval result models
│   │   │
│   │   ├── routers/
│   │   │   ├── equipment.py           # Equipment CRUD + document upload/ingestion
│   │   │   └── stream.py              # WebSocket bot connect endpoint
│   │   │
│   │   └── services/
│   │       ├── embeddings.py          # EmbeddingService (HuggingFace, LangChain >=1.2)
│   │       ├── rag.py                 # RAGService — Atlas Vector Search + cosine fallback
│   │       └── text_extraction.py     # PDF / DOCX / TXT text extraction
│   │
│   ├── main.py                        # FastAPI app factory + lifespan
│   ├── Dockerfile
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── components/                # React UI components
│   │   ├── hooks/                     # Custom React hooks (WebSocket, audio)
│   │   ├── pages/                     # Page-level components
│   │   ├── types/                     # TypeScript interfaces
│   │   └── utils/                     # Shared utilities
│   ├── Dockerfile
│   └── vite.config.ts
│
├── .github/
│   └── workflows/
│       └── deploy.yml                 # CI/CD — test → build → push Docker Hub
│
├── infrastructure/                    # Infrastructure-as-code (optional)
├── scripts/                           # Dev/ops utility scripts
├── docker-compose.yml
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- MongoDB Atlas account (free M0 tier supported)
- Groq API key ([console.groq.com](https://console.groq.com))
- Deepgram API key ([console.deepgram.com](https://console.deepgram.com))
- ElevenLabs API key ([elevenlabs.io](https://elevenlabs.io))

---

### Environment Variables

Create a `.env` file in `backend/`:

```env
# MongoDB
MONGO_URL=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DB_NAME=live_db

# Groq LLM
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
# Options: llama-3.1-8b-instant (fast) | llama-3.3-70b-versatile (quality)
GROQ_MODEL=llama-3.1-8b-instant

# Speech-to-Text
DEEPGRAM_API_KEY=xxxxxxxxxxxxxxxxxxxx

# Text-to-Speech
ELEVENLABS_API_KEY=xxxxxxxxxxxxxxxxxxxx
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB

# Embeddings (no key needed — local HuggingFace model)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSIONS=384

# RAG
CHUNK_SIZE=800
CHUNK_OVERLAP=150
VECTOR_INDEX_NAME=vector_index
DOCUMENT_CHUNKS_COLLECTION=document_chunks

# Multi-tenancy
TENANT_ID=mvp_tenant
USER_ID=mvp_user
```

---

### Local Development

**Backend**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn main:app --reload --port 8000
```

API docs available at: `http://localhost:8000/docs`

**Frontend**

```bash
cd frontend
npm install
VITE_API_BASE_URL=http://localhost:8000/api/v1 npm run dev
```

**Docker Compose (full stack)**

```bash
docker compose up --build
```

---

### MongoDB Atlas Vector Search Index

After uploading your first document, create the vector search index on the `document_chunks` collection in Atlas UI:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 384,
      "similarity": "cosine"
    },
    {
      "type": "filter",
      "path": "equipment_id"
    },
    {
      "type": "filter",
      "path": "tenant_id"
    },
    {
      "type": "filter",
      "path": "is_disabled"
    }
  ]
}
```

> Index name must match `VECTOR_INDEX_NAME` in your `.env` (default: `vector_index`).

---

## API Reference

### Equipment

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/equipment/` | Create equipment record |
| `GET` | `/api/v1/equipment/` | List all equipment |
| `GET` | `/api/v1/equipment/{id}` | Get equipment by ID |
| `POST` | `/api/v1/equipment/{id}/documents` | Upload & ingest documents (PDF, DOCX, TXT) |
| `GET` | `/api/v1/equipment/{id}/documents` | List documents for equipment |

### Stream

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/stream/connect` | Get WebSocket URL for voice bot |
| `WS` | `/api/v1/stream/ws/{equipment_id}` | Live voice pipeline WebSocket |

### Utility

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API info |
| `GET` | `/health` | Health check |

---

## RAG Pipeline

The retrieval pipeline is implemented in `backend/app/services/rag.py` and follows this flow:

```
User query (text)
       │
       ▼
EmbeddingService.embed_text()
  └─ sentence-transformers/all-MiniLM-L6-v2
  └─ returns 384-dim float vector
       │
       ▼
MongoDB Atlas $vectorSearch
  └─ index: vector_index
  └─ path: embedding
  └─ numCandidates: k * 5
  └─ filter: { equipment_id, tenant_id, is_disabled }
  └─ returns top-k chunks with vectorSearchScore
       │
       ▼  (fallback if Atlas index not configured)
In-memory cosine similarity
  └─ numpy dot product over all chunks in collection
       │
       ▼
RetrievalResult
  └─ data: List[ChunkContent]   ← clean text for LLM
  └─ metadata: RetrievalMetadata ← scores, ids, sources
```

**Document ingestion** (triggered on file upload):

```
File upload (PDF / DOCX / TXT)
       │
       ▼
TextExtractionService.extract_text()
       │
       ▼
EmbeddingService.split_text()
  └─ RecursiveCharacterTextSplitter
  └─ chunk_size=800, chunk_overlap=150
       │
       ▼
EmbeddingService.embed_text()  [per chunk]
       │
       ▼
MongoDB insert: document_chunks collection
  └─ text, embedding, chunk_id, equipment_id, tenant_id
```

---

## Voice Pipeline

The real-time voice pipeline runs inside a **Pipecat** WebSocket server defined in `backend/app/bot.py`:

```
Browser microphone
       │  WebSocket audio frames
       ▼
Deepgram STT (Nova-2)
  └─ streaming transcription
       │  text
       ▼
Groq LLM (llama-3.1-8b-instant)
  └─ system prompt: call-center assistant persona
  └─ tool: search_knowledge_base(query)
       │  tool_call
       ▼
RAGService.retrieve()
  └─ MongoDB Atlas Vector Search
  └─ returns top-5 relevant chunks
       │  tool_result (JSON)
       ▼
Groq LLM (second pass)
  └─ grounded answer ≤ 30 words, speech-optimized
       │  text
       ▼
ElevenLabs TTS (Turbo v2.5)
  └─ streaming audio synthesis
       │  WebSocket audio frames
       ▼
Agent's browser speaker
```

**LLM System Prompt Design Principles:**
- Answers grounded exclusively in retrieved knowledge base — no hallucination
- Responses kept under 30 words for natural TTS cadence
- Prices returned as integers (no decimal formatting artifacts in speech)
- Tool call always triggered for factual queries; direct answer for conversational turns

---

## CI/CD & Deployment

### Pipeline Overview

The CI/CD pipeline is defined in `.github/workflows/deploy.yml` and runs on every push to `main`.

```
Push to main
     │
     ▼
┌─────────────┐
│    Test      │  Python 3.12 | pytest | FastAPI | all deps
└──────┬──────┘
       │ pass
       ▼
┌─────────────────────────────┐
│   Build & Push Docker Images │
│                              │
│  backend  → Docker Hub       │
│  frontend → Docker Hub       │
│                              │
│  Tags:                       │
│    :latest                   │
│    :<git-sha>                │
└─────────────────────────────┘
```

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `GROQ_API_KEY` | Groq API key (used in test runner) |
| `MONGO_URL` | MongoDB Atlas connection string |
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |

### Docker Images

| Image | Tag |
|-------|-----|
| `<username>/rag-voice-agent-backend` | `latest`, `<git-sha>` |
| `<username>/rag-voice-agent-frontend` | `latest`, `<git-sha>` |

### Production Deployment

The images are production-ready for deployment on any container orchestration platform:

**AWS ECS (recommended)**
- Backend: ECS Fargate service behind an Application Load Balancer
- Frontend: CloudFront + S3 static hosting or ECS service
- Secrets: AWS Secrets Manager → ECS task environment injection

**Other platforms**
- **Railway / Render** — point to Docker Hub image, set env vars
- **Google Cloud Run** — pull from Docker Hub, stateless container
- **Kubernetes** — standard Deployment + Service manifests

### Running in Production

```bash
# Pull latest images
docker pull <username>/rag-voice-agent-backend:latest
docker pull <username>/rag-voice-agent-frontend:latest

# Run with env file
docker run -d \
  --env-file backend/.env \
  -p 8000:8000 \
  <username>/rag-voice-agent-backend:latest

docker run -d \
  -e VITE_API_BASE_URL=https://your-api-domain.com/api/v1 \
  -p 3000:80 \
  <username>/rag-voice-agent-frontend:latest
```

---

## Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGO_URL` | — | MongoDB Atlas connection string |
| `DB_NAME` | `live_db` | MongoDB database name |
| `GROQ_API_KEY` | — | Groq API key |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | Groq model ID |
| `DEEPGRAM_API_KEY` | — | Deepgram STT key |
| `ELEVENLABS_API_KEY` | — | ElevenLabs TTS key |
| `ELEVENLABS_VOICE_ID` | `pNInz6obpgDQGcFmaJgB` | ElevenLabs voice ID |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | HuggingFace embedding model |
| `EMBEDDING_DIMENSIONS` | `384` | Embedding vector dimensions |
| `CHUNK_SIZE` | `800` | RAG chunk size (characters) |
| `CHUNK_OVERLAP` | `150` | RAG chunk overlap (characters) |
| `VECTOR_INDEX_NAME` | `vector_index` | MongoDB Atlas vector index name |
| `DOCUMENT_CHUNKS_COLLECTION` | `document_chunks` | MongoDB collection for chunks |
| `TENANT_ID` | `mvp_tenant` | Default tenant identifier |
| `USER_ID` | `mvp_user` | Default user identifier |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request against `main`

**Code standards:**
- Follow PEP 8 for Python
- Use type hints throughout
- All new services must include unit tests in `backend/tests/`
- LangChain imports must use `>=0.2.0` API (`langchain_community`, `langchain_text_splitters`)

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

---

<p align="center">Built with FastAPI · Groq · MongoDB Atlas · Pipecat · ElevenLabs · Deepgram</p>
