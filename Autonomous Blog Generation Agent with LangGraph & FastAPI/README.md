<div align="center">

# 🤖 Autonomous Blog Generation Agent

### *An end-to-end agentic pipeline for intelligent, multi-lingual blog creation*

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-≥0.2-1C3D5A?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![LangChain](https://img.shields.io/badge/LangChain-≥1.2-1C3D5A?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1_8b-F55036?style=for-the-badge)](https://groq.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![MLflow](https://img.shields.io/badge/MLflow-DagsHub-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

> **Generate high-quality, SEO-optimised blog posts in English, Hindi, and French — fully autonomously — using a stateful LangGraph agent exposed via a production-ready FastAPI service.**

<br/>

[Features](#-features) · [Architecture](#-architecture) · [Project Structure](#-project-structure) · [Quick Start](#-quick-start) · [API Reference](#-api-reference) · [Deployment](#-deployment) · [Colab Notebook](#-google-colab-notebook) · [MLflow Tracking](#-mlflow--dagshub-tracking) · [Author](#-author)

</div>

---

## ✨ Features

- 🧠 **Agentic Blog Generation** — multi-step LangGraph state machine that creates title → content → (optional) translation in a fully orchestrated pipeline
- 🌐 **Multi-lingual Output** — native support for English, Hindi, and French with tone-aware, culturally adapted translation
- ⚡ **Groq LLaMA 3.1 8b Instant** — blazing-fast inference with structured output via LangChain's `.with_structured_output()`
- 🔁 **Conditional Routing** — intelligent graph routing that branches to the correct translation node based on the requested language
- 🌐 **FastAPI REST Service** — production-ready HTTP API with a single POST endpoint to generate blogs on demand
- 💾 **MongoDB Persistence** — all generated blogs are stored in MongoDB Atlas with timestamps and metadata
- 📊 **MLflow Experiment Tracking** — every run is tracked on DagsHub with parameters, metrics, and output artifacts
- 📓 **Google Colab Notebook** — fully self-contained `.ipynb` to run the entire pipeline without any local setup

---

## 🏗 Architecture

```
                        ┌─────────────────────────────────────────┐
                        │            FastAPI Service               │
                        │         POST /blogs                      │
                        └───────────────┬─────────────────────────┘
                                        │
                        ┌───────────────▼─────────────────────────┐
                        │          GraphBuilder                    │
                        │   setup_graph(usecase="topic"|"language")│
                        └───────────────┬─────────────────────────┘
                                        │
              ┌─────────────────────────▼──────────────────────────┐
              │                  LangGraph StateMachine             │
              │                                                     │
              │    [START]                                          │
              │       │                                             │
              │       ▼                                             │
              │  ┌─────────────────┐                               │
              │  │ title_creation  │  ← Groq LLaMA 3.1 8b Instant  │
              │  └────────┬────────┘                               │
              │           │                                         │
              │           ▼                                         │
              │  ┌──────────────────────┐                          │
              │  │  content_generation  │  ← Groq LLaMA 3.1 8b    │
              │  └──────────┬───────────┘                          │
              │             │                                       │
              │     ┌───────▼──────┐   (language graph only)       │
              │     │    route     │                                │
              │     └──────┬───────┘                               │
              │            │                                        │
              │     ┌──────▼───────────────────────┐               │
              │     │   route_decision (conditional)│               │
              │     └──────┬──────────────┬─────────┘              │
              │            │              │                         │
              │     ┌──────▼──────┐ ┌────▼───────────┐            │
              │     │   hindi_    │ │    french_      │            │
              │     │ translation │ │  translation    │            │
              │     └──────┬──────┘ └────┬────────────┘            │
              │            └──────┬───────┘                         │
              │                   ▼                                 │
              │               [END]                                 │
              └─────────────────────────────────────────────────────┘
                                        │
              ┌─────────────────────────▼──────────────────────────┐
              │             Outputs                                 │
              │   ┌─────────────┐   ┌──────────┐  ┌───────────┐   │
              │   │   MongoDB   │   │  MLflow  │  │ JSON / MD │   │
              │   │    Atlas    │   │  DagsHub │  │  Artifacts│   │
              │   └─────────────┘   └──────────┘  └───────────┘   │
              └─────────────────────────────────────────────────────┘
```

### Graph Topologies

| Usecase | Nodes | Trigger |
|---|---|---|
| `topic` | `title_creation → content_generation` | `POST /blogs` with `topic` only |
| `language` | `title_creation → content_generation → route → [hindi/french]_translation` | `POST /blogs` with `topic` + `language` |

---

## 📁 Project Structure

```
autonomous-blog-agent/
│
├── app.py                          # FastAPI application & /blogs endpoint
├── main.py                         # Entry point (CLI placeholder)
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Project metadata (uv/pyproject config)
├── langgraph.json                  # LangGraph Studio configuration
├── request.json                    # Sample API request payloads
├── .env                            # Environment variables (not committed)
│
├── src/
│   ├── __init__.py
│   │
│   ├── states/
│   │   ├── __init__.py
│   │   └── blogstate.py            # BlogState (TypedDict) + Blog (Pydantic)
│   │
│   ├── llms/
│   │   ├── __init__.py
│   │   └── groqllm.py              # GroqLLM wrapper (llama-3.1-8b-instant)
│   │
│   ├── nodes/
│   │   ├── __init__.py
│   │   └── blog_node.py            # BlogNode: title, content, translation, routing
│   │
│   └── graphs/
│       ├── __init__.py
│       └── graph_builder.py        # GraphBuilder: builds & compiles both graphs
│
└── autonomous_blog_agent.ipynb     # Google Colab notebook (full pipeline)
```

---

## ⚙️ Quick Start

### Prerequisites

- Python 3.11+
- [Groq API Key](https://console.groq.com)
- [MongoDB Atlas](https://cloud.mongodb.com) connection string
- [DagsHub](https://dagshub.com) account (optional, for MLflow tracking)

### 1. Clone the Repository

```bash
git clone https://github.com/PrithuSarkar/autonomous-blog-agent.git
cd autonomous-blog-agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or with `uv` (recommended for speed):

```bash
pip install uv
uv sync
```

### 4. Configure Environment Variables

Copy the example env file and fill in your credentials:

```bash
cp _copy.env .env
```

Edit `.env`:

```env
# Groq
GROQ_API_KEY=your_groq_api_key_here

# LangSmith (optional — for LangGraph Studio tracing)
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_PROJECT=autonomous-blog-agent

# MongoDB
MONGO_DB_URL=mongodb+srv://<user>:<password>@cluster.mongodb.net/

# MLflow / DagsHub
MLFLOW_TRACKING_URI=https://dagshub.com/<username>/<repo>.mlflow
MLFLOW_TRACKING_USERNAME=your_dagshub_username
MLFLOW_TRACKING_PASSWORD=your_dagshub_token
```

### 5. Run the FastAPI Server

```bash
python app.py
```

The API will be live at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## 🌐 API Reference

### `POST /blogs`

Generate a blog post autonomously.

#### Request Body

| Field | Type | Required | Description |
|---|---|---|---|
| `topic` | `string` | ✅ Yes | The topic for the blog post |
| `language` | `string` | ❌ Optional | Target language: `hindi` or `french` |

#### Example 1 — English blog (topic only)

```bash
curl -X POST http://localhost:8000/blogs \
  -H "Content-Type: application/json" \
  -d '{"topic": "Agentic AI"}'
```

#### Example 2 — French translation

```bash
curl -X POST http://localhost:8000/blogs \
  -H "Content-Type: application/json" \
  -d '{"topic": "Agentic AI", "language": "french"}'
```

#### Example 3 — Hindi translation

```bash
curl -X POST http://localhost:8000/blogs \
  -H "Content-Type: application/json" \
  -d '{"topic": "Agentic AI", "language": "hindi"}'
```

#### Response Schema

```json
{
  "data": {
    "topic": "Agentic AI",
    "blog": {
      "title": "# The Rise of Agentic AI: ...",
      "content": "## Introduction\n\n..."
    },
    "current_language": "french"
  }
}
```

#### Supported Languages

| Value | Output Language |
|---|---|
| *(omitted)* | English (default) |
| `hindi` | Hindi |
| `french` | French |

---

## 🚀 Deployment

### Option A — Local / On-Premises (Uvicorn)

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Use `--workers 4` for production (remove `--reload`):

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Option B — Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

Build and run:

```bash
docker build -t blog-agent .
docker run -p 8000:8000 --env-file .env blog-agent
```

### Option C — AWS EC2 (Ubuntu)

**1. Launch an EC2 instance** (Ubuntu 22.04, `t3.medium` or higher recommended).

**2. SSH into the instance and install dependencies:**

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx

git clone https://github.com/PrithuSarkar/autonomous-blog-agent.git
cd autonomous-blog-agent
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

**3. Set environment variables:**

```bash
sudo nano /etc/environment
# Add all key=value pairs from your .env file
```

**4. Create a systemd service for auto-restart:**

```ini
# /etc/systemd/system/blog-agent.service
[Unit]
Description=Autonomous Blog Generation Agent
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/autonomous-blog-agent
EnvironmentFile=/home/ubuntu/autonomous-blog-agent/.env
ExecStart=/home/ubuntu/autonomous-blog-agent/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable blog-agent
sudo systemctl start blog-agent
sudo systemctl status blog-agent
```

**5. Configure Nginx as a reverse proxy:**

```nginx
# /etc/nginx/sites-available/blog-agent
server {
    listen 80;
    server_name your-ec2-public-ip-or-domain;

    location / {
        proxy_pass         http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection keep-alive;
        proxy_set_header   Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header   X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/blog-agent /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
```

**6. Open EC2 Security Group ports:** `80` (HTTP) and `443` (HTTPS if using SSL).

**7. (Optional) Add HTTPS with Certbot:**

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

### Option D — AWS EC2 with Docker Compose

```yaml
# docker-compose.yml
version: "3.9"
services:
  blog-agent:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
```

```bash
docker compose up -d
```

---

## 📓 Google Colab Notebook

A fully self-contained notebook (`autonomous_blog_agent.ipynb`) is included for running the entire pipeline in Google Colab — **no local setup required**.

### Colab Secrets required

Add the following in **Colab → 🔑 Secrets** (left sidebar) before running:

| Secret Name | Description |
|---|---|
| `GROQ_API_KEY` | Groq Cloud API key |
| `MONGO_DB_URL` | MongoDB Atlas connection string |
| `MLFLOW_TRACKING_URI` | DagsHub MLflow tracking URI |
| `MLFLOW_TRACKING_USERNAME` | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | DagsHub access token |

### Notebook Phases

| Phase | Description |
|---|---|
| **0** | Install packages & load Colab secrets |
| **1** | State definitions (`BlogState`, `Blog`) |
| **2** | LLM initialisation (Groq) |
| **3** | `BlogNode` — all node methods |
| **4** | `GraphBuilder` — compile both graphs |
| **5** | Run topic-only graph (English) |
| **6** | Run language graph (Hindi + French) |
| **7** | MLflow experiment tracking |
| **8** | MongoDB persistence |
| **9** | Save all outputs → zip → download |

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PrithuSarkar/autonomous-blog-agent/blob/main/autonomous_blog_agent.ipynb)

---

## 📊 MLflow / DagsHub Tracking

Every blog-generation run is automatically logged with:

| Logged Item | Details |
|---|---|
| **Parameters** | `topic`, `language`, `usecase`, `model` |
| **Metrics** | `title_length`, `content_length`, `timestamp` |
| **Artifacts** | Generated `.md` blog file, `.json` output |

To view experiments locally:

```bash
mlflow ui --port 5000
# Open http://localhost:5000
```

Or view them directly on your [DagsHub repository](https://dagshub.com) under the **Experiments** tab.

---

## 🗄 MongoDB Schema

All blogs are persisted to the `blog_agent_db.blogs` collection:

```json
{
  "_id":        "ObjectId(...)",
  "usecase":    "language",
  "topic":      "Agentic AI",
  "language":   "french",
  "title":      "L'essor de l'IA Agentique ...",
  "content":    "## Introduction\n\n...",
  "created_at": "2025-06-13T10:30:00.000Z"
}
```

---

## 🧩 Module Overview

### `src/states/blogstate.py`

Defines the shared state schema for the LangGraph pipeline.

```python
class Blog(BaseModel):
    title:   str   # Blog post title
    content: str   # Full Markdown blog content

class BlogState(TypedDict):
    topic:            str   # Input topic
    blog:             dict  # Current Blog dict
    current_language: str   # Target translation language
```

### `src/llms/groqllm.py`

Thin wrapper to instantiate the Groq LLM:

```python
groq = GroqLLM()
llm  = groq.get_llm()   # Returns ChatGroq(model="llama-3.1-8b-instant")
```

### `src/nodes/blog_node.py`

All node callables consumed by the graph:

| Method | Role |
|---|---|
| `title_creation(state)` | LangGraph node — generates title |
| `content_generation(state)` | LangGraph node — generates content |
| `translation(state)` | LangGraph node — translates blog |
| `route(state)` | LangGraph node — passes language downstream |
| `route_decision(state)` | Conditional edge function — returns branch name |

### `src/graphs/graph_builder.py`

Builds and compiles both graph topologies:

```python
builder = GraphBuilder(llm)

topic_graph    = builder.setup_graph(usecase="topic")
language_graph = builder.setup_graph(usecase="language")
```

---

## 📦 Dependencies

```
langchain>=1.2
langgraph>=0.2
langchain-core>=0.2
langchain-community>=0.2
langchain-groq>=0.1
fastapi
uvicorn
pymongo
mlflow
dagshub
pydantic
python-dotenv
```

Install all:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Groq Cloud API key |
| `MONGO_DB_URL` | ✅ | MongoDB Atlas connection URI |
| `LANGCHAIN_API_KEY` | ⚠️ Optional | LangSmith tracing key |
| `LANGCHAIN_PROJECT` | ⚠️ Optional | LangSmith project name |
| `MLFLOW_TRACKING_URI` | ⚠️ Optional | MLflow / DagsHub URI |
| `MLFLOW_TRACKING_USERNAME` | ⚠️ Optional | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | ⚠️ Optional | DagsHub token |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Prithu Sarkar**

[![GitHub](https://img.shields.io/badge/GitHub-PrithuSarkar-181717?style=for-the-badge&logo=github)](https://github.com/PrithuSarkar)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Prithu_Sarkar-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/prithu-sarkar)

---

<div align="center">

*Built with ❤️ using LangGraph · FastAPI · Groq · MongoDB · MLflow*

⭐ **Star this repo if you found it helpful!** ⭐

</div>
