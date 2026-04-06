# 🛒 Flipkart AI Product Recommender

<p align="center">
  <img src="https://github.com/user-attachments/assets/c476cb8c-2635-41bf-9833-2d07e0b04039" alt="Flipkart AI Chatbot Demo" width="85%"/>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3110/"><img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white" alt="Python"/></a>
  <a href="https://flask.palletsprojects.com/"><img src="https://img.shields.io/badge/Flask-3.1.2-black?logo=flask&logoColor=white" alt="Flask"/></a>
  <a href="https://www.langchain.com/"><img src="https://img.shields.io/badge/LangChain-1.2.1-1C3C3C?logo=langchain&logoColor=white" alt="LangChain"/></a>
  <a href="https://groq.com"><img src="https://img.shields.io/badge/Groq-LLM-F55036?logoColor=white" alt="Groq"/></a>
  <a href="https://www.datastax.com/products/datastax-astra"><img src="https://img.shields.io/badge/AstraDB-Vector_DB-7B2FBE?logoColor=white" alt="AstraDB"/></a>
  <a href="https://huggingface.co/"><img src="https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?logo=huggingface&logoColor=black" alt="HuggingFace"/></a>
  <a href="https://prometheus.io/"><img src="https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus&logoColor=white" alt="Prometheus"/></a>
  <a href="https://grafana.com/"><img src="https://img.shields.io/badge/Grafana-Dashboards-F46800?logo=grafana&logoColor=white" alt="Grafana"/></a>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License"/>
</p>

---

## 📖 Overview

**Flipkart AI Product Recommender** is a production-grade RAG (Retrieval-Augmented Generation) chatbot that answers product-related queries using real Flipkart customer reviews. Users ask natural-language questions — the system retrieves semantically similar reviews from a vector database and generates structured, grounded answers via a Groq-hosted LLM.

The application is served via **Flask** with built-in **Prometheus metrics**, containerised with **Docker**, orchestrated on a **Kubernetes (Minikube)** cluster deployed on a **GCP VM**, and monitored end-to-end using **Prometheus + Grafana** dashboards.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     LOCAL PROJECT SETUP                         │
│                                                                 │
│  Project & API Setup → Configuration → Data Converter          │
│       → Data Ingestion → RAG Chain → Flask + HTML/CSS App      │
└──────────────────────────────┬──────────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
┌──────────────────────────┐   ┌───────────────────────────────┐
│  CONTAINERIZATION &      │   │      MONITORING SETUP         │
│  ORCHESTRATION           │   │                               │
│                          │   │  Prometheus Deployment ──►    │
│  Dockerfile ──►          │   │  Grafana Deployment           │
│  Kubernetes Manifest     │   └───────────────────────────────┘
└──────────────────────────┘
               │                       │
               └──────── Commit & Push ┘
                               │
        ┌──────────────────────┼────────────────────────┐
        ▼                      ▼                         ▼
┌──────────────┐   ┌───────────────────────┐   ┌─────────────────┐
│   VERSION    │   │   CLOUD DEPLOYMENT    │   │   MONITORING    │
│   CONTROL    │   │                       │   │                 │
│              │   │  GCP VM Instance  ──► │   │  Prometheus +   │
│  GitHub      │   │  Build & Deploy on    │   │  Grafana on     │
│  Versioning  │   │  Minikube K8s in VM   │   │  Deployed App   │
└──────────────┘   └───────────────────────┘   └─────────────────┘
```

---

## ✨ Features

- 🔍 **Semantic Search** — `BAAI/bge-base-en-v1.5` embeddings over Flipkart product reviews via AstraDB
- 🤖 **RAG Chain** — Groq LLM synthesises answers grounded in retrieved review context
- 💬 **Flask Chat UI** — Clean HTML/CSS chat interface with AJAX messaging
- 📊 **Prometheus Metrics** — `http_requests_total` and `model_predictions_total` counters exposed at `/metrics`
- 📈 **Grafana Dashboards** — Live visualisation of request rates and model prediction throughput
- 🐳 **Containerised** — Single-command Docker build on `python:3.11-slim`
- ☸️ **Kubernetes-Ready** — Deployment + LoadBalancer service manifests included
- 🏥 **Health Endpoint** — `/health` returns JSON status for K8s liveness probes
- 🖥️ **GCP Deployment** — Runs on GCP E2 Standard VM (16 GB RAM, 256 GB disk, Ubuntu 24.04)

---

## 📁 Project Structure

```
flipkart-product-chatbot/
├── flipkart/
│   ├── __init__.py
│   ├── config.py                  # API keys & model configuration
│   ├── data_converter.py          # CSV → LangChain Documents
│   ├── data_ingestion.py          # AstraDB vector store ingest/load
│   └── rag_agent.py               # RAG chain with retriever tool
├── frontend/
│   ├── templates/
│   │   └── index.html             # Flask chat UI
│   └── static/
│       └── style.css              # Chat interface styling
├── prometheus/
│   ├── prometheus-configmap.yaml  # Scrape config (Flask /metrics target)
│   └── prometheus-deployment.yaml # Prometheus Deployment + NodePort Service
├── grafana/
│   └── grafana-deployment.yaml   # Grafana Deployment + NodePort Service
├── data/
│   └── flipkart_product_review.csv
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── custom_exception.py
├── .env                           # API keys (not committed)
├── .dockerignore
├── .gitignore
├── app.py                         # Flask application entry point
├── streamlit_app.py               # Streamlit UI alternative
├── Dockerfile
├── flask-deployment.yaml          # K8s Deployment + LoadBalancer Service
├── requirements.txt
├── setup.py
└── README.md
```

---

## 🚀 Getting Started (Local)

### Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com) (free)
- A [HuggingFace token](https://huggingface.co/settings/tokens) (free)
- A [DataStax AstraDB](https://astra.datastax.com) account — create a free serverless vector database

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/flipkart-product-chatbot.git
cd flipkart-product-chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -e .
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
ASTRA_DB_API_ENDPOINT=your_astradb_endpoint
ASTRA_DB_APPLICATION_TOKEN=your_astradb_token
ASTRA_DB_KEYSPACE=default_keyspace
```

### 5. Ingest Data into AstraDB (Run Once)

```bash
python -m flipkart.data_ingestion
```

This embeds all reviews with `BAAI/bge-base-en-v1.5` and uploads them to AstraDB. Subsequent runs load the existing collection.

### 6. Run the Flask App

```bash
python app.py
```

Navigate to `http://localhost:5000`.

### 7. Run the Streamlit App (Alternative)

```bash
streamlit run streamlit_app.py
```

---

## 🐳 Docker

### Build

```bash
docker build -t flask-app:latest .
```

### Run

```bash
docker run -p 5000:5000 \
  -e GROQ_API_KEY=your_key \
  -e HF_TOKEN=your_token \
  -e ASTRA_DB_API_ENDPOINT=your_endpoint \
  -e ASTRA_DB_APPLICATION_TOKEN=your_token \
  -e ASTRA_DB_KEYSPACE=default_keyspace \
  flask-app:latest
```

Navigate to `http://localhost:5000`.

---

## ☸️ Kubernetes Deployment on GCP VM

### 1. Create a GCP VM Instance

In the GCP Console → **Compute Engine** → **VM Instances** → **Create Instance**:

| Setting | Value |
|---|---|
| Machine Series | E2 |
| Machine Type | e2-standard-4 (Standard, 16 GB RAM) |
| Boot Disk | Ubuntu 24.04 LTS, 256 GB |
| Networking | Enable HTTP and HTTPS traffic |

Connect via browser SSH once the instance is running.

### 2. Clone the Repository on the VM

```bash
git clone https://github.com/<your-username>/flipkart-product-chatbot.git
cd flipkart-product-chatbot
```

### 3. Install Docker on the VM

Follow the official [Docker install guide for Ubuntu](https://docs.docker.com/engine/install/ubuntu/). Then run:

```bash
docker run hello-world   # verify install

# Run Docker without sudo
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

# Enable Docker on boot
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

### 4. Install and Start Minikube

```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster (uses Docker as driver)
minikube start

# Install kubectl
sudo snap install kubectl --classic

# Verify
minikube status
kubectl get nodes
```

### 5. Build and Deploy the Flask App

```bash
# Point Docker to Minikube's daemon
eval $(minikube docker-env)

# Build image inside Minikube
docker build -t flask-app:latest .

# Create Kubernetes secret with all API keys
kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY="your_groq_key" \
  --from-literal=ASTRA_DB_APPLICATION_TOKEN="your_astra_token" \
  --from-literal=ASTRA_DB_KEYSPACE="default_keyspace" \
  --from-literal=ASTRA_DB_API_ENDPOINT="your_astra_endpoint" \
  --from-literal=HF_TOKEN="your_hf_token" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN="your_hf_token"

# Apply deployment manifest
kubectl apply -f flask-deployment.yaml

# Verify pods are running
kubectl get pods
```

### 6. Expose the Application

```bash
kubectl port-forward svc/flask-service 5000:80 --address 0.0.0.0
```

Navigate to `http://<VM_EXTERNAL_IP>:5000`.

---

## 📊 Monitoring with Prometheus & Grafana

The Flask app exposes a `/metrics` endpoint powered by `prometheus_client`, tracking:

| Metric | Type | Description |
|---|---|---|
| `http_requests_total` | Counter | Total HTTP requests received |
| `model_predictions_total` | Counter | Total LLM predictions generated |

### 1. Deploy Prometheus and Grafana

```bash
# Create monitoring namespace
kubectl create namespace monitoring
kubectl get ns

# Deploy Prometheus (ConfigMap + Deployment + Service)
kubectl apply -f prometheus/prometheus-configmap.yaml
kubectl apply -f prometheus/prometheus-deployment.yaml

# Deploy Grafana
kubectl apply -f grafana/grafana-deployment.yaml

# Verify all pods are running
kubectl get pods -n monitoring
```

### 2. Access Prometheus

```bash
kubectl port-forward --address 0.0.0.0 svc/prometheus-service -n monitoring 9090:9090
```

Navigate to `http://<VM_EXTERNAL_IP>:9090`.  
Go to **Status → Targets** to verify the `flask-app` scrape target shows **UP**.

### 3. Access Grafana

```bash
kubectl port-forward --address 0.0.0.0 svc/grafana-service -n monitoring 3000:3000
```

Navigate to `http://<VM_EXTERNAL_IP>:3000`.  
Default credentials: **admin / admin**

### 4. Connect Grafana to Prometheus

1. Go to **Settings → Data Sources → Add Data Source**
2. Select **Prometheus**
3. Set URL to:
   ```
   http://prometheus-service.monitoring.svc.cluster.local:9090
   ```
4. Click **Save & Test** — a green success message confirms the connection

### 5. Build Dashboards

Create panels using the exposed metrics:

```promql
# Total request rate (per minute)
rate(http_requests_total[1m])

# Total prediction rate (per minute)
rate(model_predictions_total[1m])

# Cumulative request count
http_requests_total

# Cumulative prediction count
model_predictions_total
```

### Monitoring Architecture

```
Flask App (:5000/metrics)
       │
       │  scrape every 15s
       ▼
  Prometheus (:9090)
       │
       │  data source
       ▼
   Grafana (:3000)
  [Dashboards & Alerts]
```

---

## 🔬 Core Components

### `DataConverter` — `flipkart/data_converter.py`
Reads `flipkart_product_review.csv`, selects `product_title` and `review` columns, and wraps each row in a LangChain `Document` with `review` as `page_content` and `product_title` as metadata.

### `DataIngestor` — `flipkart/data_ingestion.py`
Connects to AstraDB using `langchain_astradb.AstraDBVectorStore` with `BAAI/bge-base-en-v1.5` embeddings via `HuggingFaceEndpointEmbeddings`. Supports two modes: `load_existing=False` for initial ingestion and `load_existing=True` for instant load.

### `RAGAgentBuilder` — `flipkart/rag_agent.py`
Builds a LangChain tool-calling agent backed by the Groq LLM. The `flipkart_retriever_tool` retrieves top-k reviews; the agent decides when to call it and synthesises a final answer.

### `app.py` — Flask Application
Creates the Flask app with Prometheus counters on every route. Exposes `/` (chat UI), `/get` (POST for agent responses), `/health` (liveness probe), and `/metrics` (Prometheus scrape endpoint).

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq (configurable model) |
| Embeddings | HuggingFace — `BAAI/bge-base-en-v1.5` |
| Vector Store | DataStax AstraDB (serverless) |
| LLM Framework | LangChain 1.2.1 |
| Frontend | Flask 3.1.2 + HTML/CSS |
| Monitoring | Prometheus + Grafana |
| Containerisation | Docker (python:3.11-slim) |
| Orchestration | Kubernetes (Minikube on GCP) |
| Cloud | Google Cloud Platform (E2 VM) |
| Language | Python 3.11+ |

---

## 🗂️ Dataset

The system uses `data/flipkart_product_review.csv` with the following columns:

| Column | Description |
|---|---|
| `product_title` | Name of the Flipkart product |
| `review` | Customer review text |

A compatible dataset is available on Kaggle: [Flipkart Product Reviews](https://www.kaggle.com/datasets/niraliivaghani/flipkart-product-customer-reviews-dataset)

---

## ⚙️ Configuration

All configuration lives in `flipkart/config.py` and is populated from the `.env` file:

```python
class Config:
    ASTRA_DB_API_ENDPOINT       = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN  = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_KEYSPACE           = os.getenv("ASTRA_DB_KEYSPACE")
    GROQ_API_KEY                = os.getenv("GROQ_API_KEY")
    EMBEDDING_MODEL             = "BAAI/bge-base-en-v1.5"
    RAG_MODEL                   = "groq:qwen/qwen3-32b"
```

---

## 📝 Logging

Logs are written daily to `logs/log_YYYY-MM-DD.log`:

```
2026-01-10 14:32:01 - INFO  - Flask app started on 0.0.0.0:5000
2026-01-10 14:32:15 - INFO  - Received query: best phone under 15000
2026-01-10 14:32:17 - INFO  - RAG chain completed in 1.8s
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

**dmt**  
Built with ❤️ for e-commerce AI and MLOps practitioners.

---

<p align="center">
  <i>If this project helped you, please consider giving it a ⭐</i>
</p>
