# 🌸 AniBaba — AI Anime Recommender

<p align="center">
  <img src="imgs/bg.png" alt="AniBaba Banner" width="100%"/>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3100/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python"/></a>
  <a href="https://streamlit.io"><img src="https://img.shields.io/badge/Streamlit-1.52.2-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/></a>
  <a href="https://www.langchain.com/"><img src="https://img.shields.io/badge/LangChain-1.2.1-1C3C3C?logo=langchain&logoColor=white" alt="LangChain"/></a>
  <a href="https://groq.com"><img src="https://img.shields.io/badge/Groq-Qwen3--32B-F55036?logo=groq&logoColor=white" alt="Groq"/></a>
  <a href="https://www.trychroma.com/"><img src="https://img.shields.io/badge/ChromaDB-1.4.0-E85E2E?logoColor=white" alt="ChromaDB"/></a>
  <a href="https://huggingface.co/"><img src="https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?logo=huggingface&logoColor=black" alt="HuggingFace"/></a>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License"/>
</p>

---

## 📖 Overview

**AniBaba** is a production-grade AI-powered anime recommendation system built on a **Retrieval-Augmented Generation (RAG)** architecture. Users describe what kind of anime they are in the mood for in natural language, and the system retrieves semantically relevant entries from a vector database before generating rich, structured recommendations via a Groq-hosted LLM.

The system uses **tool-calling** — the LLM autonomously decides when to query the vector store, ensuring every recommendation is grounded in the actual anime dataset rather than hallucinated from model weights alone.

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│                   PROJECT SETUP                         │
│   Groq API · HuggingFace API · Virtual Environment     │
│   Logging · Custom Exception · Project Structure        │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    CORE CODE                            │
│                                                         │
│  Configuration ──► Data Loader ──► ChromaDB            │
│                                        │                │
│             Prompt Templates ◄─────────┘                │
│                    │                                    │
│                    ▼                                    │
│          Recommender Class ──► Train & Recommend        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
              Streamlit App
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   DEPLOYMENT                            │
│   Dockerfile · K8s Deploy · Code Versioning (GitHub)   │
│   GCP VM · K8s App · GitHub Integration                │
│   Grafana Cloud Monitoring                              │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

- 🔍 **Semantic Search** — HuggingFace `all-MiniLM-L6-v2` embeddings over 10,000+ anime titles
- 🤖 **Tool-Calling LLM** — Groq `qwen/qwen3-32b` autonomously retrieves context before answering
- 💬 **Conversational Chat UI** — Streamlit-based multi-turn chat interface with session history
- 📦 **Modular Architecture** — Clean separation of data ingestion, vector store, prompt, and LLM layers
- 🛡️ **Production-Ready** — Custom exception handling, structured logging, and environment-based config
- 🐳 **Containerised** — Single-command Docker build and run
- ☸️ **Kubernetes-Ready** — Deployment and LoadBalancer service manifests included
- 📊 **Observability** — Grafana Cloud monitoring via Helm on Minikube

---

## 📁 Project Structure

```
AniBaba/
├── app/
│   ├── __init__.py
│   ├── app.py                   # Streamlit entry point (production)
│   └── app2.py                  # Streamlit app with full chat UI
├── config/
│   ├── __init__.py
│   └── config.py                # API keys & model configuration
├── data/
│   ├── anime_with_synopsis.csv  # Raw dataset (Name, Genres, sypnopsis)
│   └── anime_updated.csv        # Processed dataset (combined_info)
├── imgs/
│   └── bg.png                   # Streamlit background image
├── logs/
│   └── log_YYYY-MM-DD.log       # Auto-generated daily logs
├── pipeline/
│   ├── __init__.py
│   ├── build_pipeline.py        # One-shot data ingestion + vectorstore build
│   └── pipeline.py              # Inference pipeline orchestrator
├── src/
│   ├── __init__.py
│   ├── data_loader.py           # CSV ingestion and processing
│   ├── prompt_template.py       # LangChain RAG prompt template
│   ├── recommender.py           # AnimeRecommender + tool-calling logic
│   └── vector_store.py          # ChromaDB build and load
├── utils/
│   ├── __init__.py
│   ├── bgimage.py               # Streamlit background helper
│   ├── custom_exception.py      # Structured exception with traceback info
│   └── logger.py                # Logging configuration
├── .dockerignore
├── .env                         # API keys (not committed — see .gitignore)
├── .gitignore
├── Dockerfile
├── llmops-k8s.yaml              # Kubernetes Deployment + Service manifest
├── requirements.txt
├── setup.py
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com) (free tier available)
- A [HuggingFace token](https://huggingface.co/settings/tokens) (for embedding model access)

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/anibaba.git
cd anibaba
```

### 2. Create a Virtual Environment

```bash
python -m venv animeenv
source animeenv/bin/activate        # Linux / macOS
animeenv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -e .
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

### 5. Build the Vector Database

Run this once to process the raw CSV and populate ChromaDB:

```bash
python pipeline/build_pipeline.py
```

This will:
1. Load `data/anime_with_synopsis.csv`
2. Create `combined_info` from Title + Synopsis + Genres
3. Embed all entries with `all-MiniLM-L6-v2`
4. Persist the vector store to `chroma_db/`

### 6. Run the Streamlit App

```bash
streamlit run app/app2.py
```

Navigate to `http://localhost:8501` and start chatting.

---

## 🐳 Docker

### Build

```bash
docker build -t llmops-app:latest .
```

### Run

```bash
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_key \
  -e HF_TOKEN=your_token \
  llmops-app:latest
```

Navigate to `http://localhost:8501`.

---

## ☸️ Kubernetes Deployment (Minikube / GCP)

### 1. Point Docker to Minikube's daemon

```bash
eval $(minikube docker-env)
```

### 2. Build the image inside Minikube

```bash
docker build -t llmops-app:latest .
```

### 3. Create the secrets

```bash
kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY="your_groq_api_key" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN="your_hf_token"
```

### 4. Apply the manifest

```bash
kubectl apply -f llmops-k8s.yaml
```

### 5. Expose the service

```bash
# Terminal 1
minikube tunnel

# Terminal 2
kubectl port-forward svc/llmops-service 8501:80 --address 0.0.0.0
```

### 6. Verify pods are running

```bash
kubectl get pods
kubectl get svc
```

Navigate to `http://<EXTERNAL-IP>:8501`.

---

## 📊 Monitoring with Grafana Cloud

### Setup

```bash
# Create the monitoring namespace
kubectl create ns monitoring

# Add the Grafana Helm chart repo
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

### Deploy the K8s monitoring stack

```bash
helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring \
  grafana/k8s-monitoring \
  --namespace monitoring \
  --create-namespace \
  --values values.yaml
```

### Verify

```bash
kubectl get pods -n monitoring
```

All pods should show `Running`. Navigate to your Grafana Cloud dashboard to view cluster metrics.

---

## 🔬 Core Components

### `AnimeDataLoader` — `src/data_loader.py`
Reads `anime_with_synopsis.csv`, validates required columns (`Name`, `Genres`, `sypnopsis`), and constructs a `combined_info` field used for embedding.

### `VectorStoreBuilder` — `src/vector_store.py`
Loads the processed CSV via `CSVLoader`, chunks documents with `RecursiveCharacterTextSplitter` (chunk size: 1000), and builds/loads a persistent ChromaDB vector store using `all-MiniLM-L6-v2` embeddings.

### `get_anime_prompt` — `src/prompt_template.py`
Returns a `PromptTemplate` that instructs the LLM to provide exactly three structured recommendations — each with a title, synopsis, and preference-match explanation.

### `AnimeRecommender` — `src/recommender.py`
Binds the `anime_retriever_tool` to the Groq LLM using LangChain's tool-calling interface. The LLM autonomously calls the retriever when needed, then synthesises the retrieved context into a final response.

### `AnimeRecommendationPipeline` — `pipeline/pipeline.py`
Orchestrates `VectorStoreBuilder` + `AnimeRecommender` under a single interface with full logging and custom exception propagation.

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq — `qwen/qwen3-32b` |
| Embeddings | HuggingFace — `all-MiniLM-L6-v2` |
| Vector Store | ChromaDB 1.4.0 |
| LLM Framework | LangChain 1.2.1 |
| Frontend | Streamlit 1.52.2 |
| Containerisation | Docker (python:3.10-slim) |
| Orchestration | Kubernetes (Minikube / GCP) |
| Monitoring | Grafana Cloud + Helm |
| Language | Python 3.10+ |

---

## 🗂️ Dataset

The system expects a CSV file at `data/anime_with_synopsis.csv` with the following columns:

| Column | Description |
|---|---|
| `Name` | Anime title |
| `Genres` | Comma-separated genre tags |
| `sypnopsis` | Plot summary |

A compatible dataset is available on Kaggle:  
[Anime Recommendation Database 2020](https://www.kaggle.com/datasets/hernan4444/anime-recommendation-database-2020)

---

## ⚙️ Configuration

All configuration lives in `config/config.py` and is populated from the `.env` file:

```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_TOKEN     = os.getenv("HF_TOKEN")
MODEL_NAME   = "groq:qwen/qwen3-32b"
```

To switch LLM providers or models, change `MODEL_NAME` to any model supported by `langchain.chat_models.init_chat_model`.

---

## 📝 Logging

Logs are written daily to `logs/log_YYYY-MM-DD.log` and capture pipeline initialisation, query events, and errors:

```
2026-01-10 14:32:01 - INFO  - Initializing Recommendation Pipeline
2026-01-10 14:32:04 - INFO  - Pipeline initialized successfully
2026-01-10 14:32:10 - INFO  - Received query: anime like Attack on Titan
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch — `git checkout -b feature/your-feature`
3. Commit your changes — `git commit -m "feat: add your feature"`
4. Push to the branch — `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Divesh — DataGuru**  
Built with ❤️ for anime fans and MLOps practitioners.

---

<p align="center">
  <i>If this project helped you, please consider giving it a ⭐</i>
</p>
