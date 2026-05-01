# Google ADK — Build AI Agents

A structured implementation of three progressively complex AI agent projects built with [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/), powered by **Groq + LLaMA** instead of Gemini. Each project introduces a distinct layer of the ADK architecture — from persistent state management to REST API integration to cloud deployment.

---

## Projects

### 0 · Persistent Storage with ADK
**Reading List Curator** — a conversational agent that manages a personal reading list with full CRUD capabilities and durable state across sessions.

- `InMemorySessionService` for ephemeral sessions
- `DatabaseSessionService` (SQLite via SQLAlchemy) for cross-run persistence
- Six tool functions operating on `ToolContext.state`: `set_user_name`, `add_item`, `list_items`, `update_item`, `annotate_item`, `remove_item`
- Event streaming via `Runner.run_async()`

### 1 · ADK API Server + Streamlit Frontend
**Simple Q&A Agent** — demonstrates the ADK REST API layer and a Streamlit client that communicates with a running agent server.

- `adk api_server` exposes `/run`, `/list-apps`, and session management endpoints
- `ADKClient` HTTP wrapper for programmatic access
- Full Streamlit app with session lifecycle management and raw event inspection
- Multi-event response parsing

### 2 · Cloud Run Capital Agent
**Capital Agent** — the minimal ADK agent structure, purpose-built to demonstrate `adk deploy cloud_run`.

- Smallest valid ADK agent (`root_agent`, no tools)
- Deployment to Google Cloud Run via `adk deploy cloud_run`
- Secret Manager integration for API key injection
- IAM configuration for authenticated and public access patterns

---

## Repository Structure

```
.
├── project_0/
│   ├── memory_agent/
│   │   ├── __init__.py
│   │   └── agent.py          # LlmAgent + 6 CRUD tools
│   ├── utils.py              # Event logger, state printer, call_agent_async
│   └── reading_list.db       # Auto-created SQLite database
│
├── project_1/
│   ├── agents/
│   │   └── simple/
│   │       ├── __init__.py
│   │       └── agent.py      # Q&A LlmAgent
│   ├── common/
│   │   └── adk_client.py     # Minimal HTTP client for ADK API server
│   └── apps/
│       └── app.py            # Streamlit frontend
│
├── project_2/
│   └── capital_agent/
│       ├── __init__.py
│       ├── agent.py          # Minimal root_agent
│       └── requirements.txt
│
└── Google_ADK_Complete_Colab.ipynb   # End-to-end walkthrough notebook
```

---

## Requirements

**Python** 3.10 or higher

```
google-adk
groq
litellm
python-dotenv
sqlalchemy
nest-asyncio
streamlit          # project_1 only
requests           # project_1 only
```

Install all at once:

```bash
pip install google-adk groq litellm python-dotenv sqlalchemy nest-asyncio streamlit requests
```

---

## Configuration

This project uses **Groq** as the LLM provider via LiteLLM's OpenAI-compatible interface, replacing the course's original Gemini dependency.

### Environment Variables

Create a `.env` file in the project root or export the following:

```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_groq_api_key_here       # LiteLLM bridge
OPENAI_API_BASE=https://api.groq.com/openai/v1
ADK_MODEL=groq/llama-3.3-70b-versatile      # or groq/llama-3.1-8b-instant
```

Obtain a Groq API key at [console.groq.com](https://console.groq.com).

### Model Reference

| Constant | Model | Recommended for |
|---|---|---|
| `INSTANT_MODEL` | `groq/llama-3.1-8b-instant` | Fast, simple factual tasks |
| `VERSATILE_MODEL` | `groq/llama-3.3-70b-versatile` | Tool use, reasoning, multi-turn |

---

## Running the Projects

### Project 0 — Persistent Storage

```bash
cd project_0
export ADK_MODEL=groq/llama-3.3-70b-versatile
python main.py
```

The agent will prompt for input interactively. State is written to `reading_list.db` and restored on subsequent runs.

To explore the agent via the ADK web UI:

```bash
adk web -v project_0/
```

---

### Project 1 — API Server + Streamlit

**Terminal 1** — start the ADK API server:

```bash
cd project_1
export ADK_MODEL=groq/llama-3.3-70b-versatile
adk api_server -v .
# Swagger UI: http://localhost:8000/docs
```

**Terminal 2** — launch the Streamlit frontend:

```bash
streamlit run project_1/apps/app.py
```

**Or test directly with curl:**

```bash
APP=simple; USER=demo; SID=session-1

# Create session
curl -s -X POST "http://localhost:8000/apps/$APP/users/$USER/sessions/$SID" \
     -H "Content-Type: application/json" -d '{}'

# Run a turn
curl -s -X POST http://localhost:8000/run \
     -H "Content-Type: application/json" \
     -d '{"app_name":"simple","user_id":"demo","session_id":"session-1",
          "new_message":{"role":"user","parts":[{"text":"What is RAG?"}]}}'
```

---

### Project 2 — Cloud Run Deployment

**Local test:**

```bash
cd project_2
export ADK_MODEL=groq/llama-3.1-8b-instant
adk web -v .
```

**Deploy to Cloud Run:**

```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1

# Store API key in Secret Manager
echo -n "$GROQ_API_KEY" | gcloud secrets create groq-api-key --data-file=-

# Deploy
adk deploy cloud_run \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=capital-service \
  --app_name=capital-agent-app \
  --with_ui \
  capital_agent
```

**Test the deployed service:**

```bash
SERVICE_URL=$(gcloud run services describe capital-service \
  --region=$GOOGLE_CLOUD_LOCATION --format="value(status.url)")

SID="session-$(date +%s)"

curl -s -X POST "$SERVICE_URL/apps/capital-agent-app/users/demo/sessions/$SID" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
     -d '{}'

curl -s -X POST "$SERVICE_URL/run" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
     -d '{"app_name":"capital-agent-app","user_id":"demo","session_id":"'$SID'",
          "new_message":{"role":"user","parts":[{"text":"Capital of India?"}]}}'
```

**Teardown:**

```bash
gcloud run services delete capital-service --region=$GOOGLE_CLOUD_LOCATION --quiet
```

---

## Architecture

```
User Input
    │
    ▼
Runner.run_async()
    │
    ▼
LlmAgent  ──────────────────────────────────────────────►  Groq API
    │                                                    (LLaMA via LiteLLM)
    ▼
Tool Functions
    │  mutate tool_context.state
    ▼
SessionService  ──►  InMemorySessionService  (ephemeral)
                 ──►  DatabaseSessionService  (SQLite / Cloud SQL)
```

For the API server path (Project 1 and Cloud Run):

```
Client  ──►  ADK API Server  ──►  Runner  ──►  LlmAgent  ──►  Groq
              POST /run
              GET  /list-apps
              POST /apps/.../sessions/...
```

---

## ADK CLI Reference

| Command | Purpose |
|---|---|
| `adk web -v .` | Launch web UI for any project containing `root_agent` |
| `adk api_server -v .` | Launch REST API server on port 8000 |
| `adk deploy cloud_run ...` | Package and deploy agent to Google Cloud Run |

---

## Colab Notebook

A complete end-to-end walkthrough of all three projects is available in `Google_ADK_Complete_Colab.ipynb`. It requires a single Colab Secret:

| Secret name | Value |
|---|---|
| `GROQ_API_KEY` | Your Groq API key |

Add via: **Runtime → Secrets → Add new secret** before running any cells.

---

## License

This project is released for educational purposes. Refer to the [Google ADK license](https://github.com/google/adk-python/blob/main/LICENSE) and [Groq Terms of Service](https://groq.com/terms-of-use/) for usage conditions.
