<div align="center">

<br/>

```
███╗   ███╗██╗      ██████╗ ██████╗ ███████╗
████╗ ████║██║     ██╔═══██╗██╔══██╗██╔════╝
██╔████╔██║██║     ██║   ██║██████╔╝███████╗
██║╚██╔╝██║██║     ██║   ██║██╔═══╝ ╚════██║
██║ ╚═╝ ██║███████╗╚██████╔╝██║     ███████║
╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝     ╚══════╝
```

# Industrial Machine Efficiency — End-to-End MLOps Pipeline

### Predictive Intelligence · Jenkins Shared Library · Kubernetes · MLflow · MongoDB · Groq AI

<br/>

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![MLflow](https://img.shields.io/badge/MLflow-DagsHub-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Docker](https://img.shields.io/badge/Docker-Containerised-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io)
[![Jenkins](https://img.shields.io/badge/Jenkins-Shared_Library-D24939?style=for-the-badge&logo=jenkins&logoColor=white)](https://jenkins.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-FF6B35?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![LangChain](https://img.shields.io/badge/LangChain-≥1.2-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

> **A production-grade MLOps system** that ingests 100,000+ industrial sensor records from MongoDB Atlas, processes and models machine efficiency using Scikit-learn, tracks experiments on DagsHub via MLflow, containerises the inference server with Docker, orchestrates deployment to Kubernetes, and automates the entire lifecycle through a Jenkins Shared Library CI/CD pipeline — augmented with Groq-powered LLM feature analysis via LangChain.

<br/>

</div>

---

## Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Pipeline Phases](#-pipeline-phases)
  - [Phase 0 — Environment & Configuration](#phase-0--environment--configuration)
  - [Phase 1 — Source Module Authoring](#phase-1--source-module-authoring)
  - [Phase 2 — Data Ingestion (MongoDB)](#phase-2--data-ingestion-mongodb)
  - [Phase 3 — Exploratory Data Analysis](#phase-3--exploratory-data-analysis)
  - [Phase 4 — Groq LLM Feature Intelligence](#phase-4--groq-llm-feature-intelligence)
  - [Phase 5 — Data Processing Pipeline](#phase-5--data-processing-pipeline)
  - [Phase 6 — Model Training & MLflow Tracking](#phase-6--model-training--mlflow-tracking)
  - [Phase 7 — Flask Inference Server](#phase-7--flask-inference-server)
  - [Phase 8 — Containerisation with Docker](#phase-8--containerisation-with-docker)
  - [Phase 9 — Kubernetes Deployment](#phase-9--kubernetes-deployment)
  - [Phase 10 — Jenkins Shared Library CI/CD](#phase-10--jenkins-shared-library-cicd)
  - [Phase 11 — GitHub Webhooks & Full Automation](#phase-11--github-webhooks--full-automation)
- [Dataset Schema](#-dataset-schema)
- [Jenkins Shared Library](#-jenkins-shared-library)
- [Infrastructure Setup](#-infrastructure-setup)
- [Credentials & Secrets Reference](#-credentials--secrets-reference)
- [Local Development](#-local-development)
- [MLflow Experiment Tracking](#-mlflow-experiment-tracking)
- [Inference API](#-inference-api)
- [Contributing](#-contributing)

---

## 🏗 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MLOPS PIPELINE ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────────────────────┘

   ┌──────────────┐     ┌───────────────┐     ┌──────────────────────────────┐
   │   MongoDB    │────▶│  Data         │────▶│  Feature Engineering         │
   │   Atlas      │     │  Ingestion    │     │  + LabelEncoding             │
   │  (Raw Data)  │     │  (Phase 2)    │     │  + StandardScaler            │
   └──────────────┘     └───────────────┘     └──────────────┬───────────────┘
                                                              │
                         ┌────────────────────────────────────▼───────────────┐
                         │              GROQ LLM  (LangChain ≥ 1.2)          │
                         │        llama-3.1-8b-instant  │  Feature Insights   │
                         └────────────────────────────────────┬───────────────┘
                                                              │
   ┌──────────────────────────────────────────────────────────▼───────────────┐
   │                        MODEL TRAINING                                    │
   │   LogisticRegression  │  accuracy / precision / recall / F1              │
   │   MLflow → DagsHub    │  Params + Metrics + Model Artifact               │
   └──────────────────────────────────────────────────────────┬───────────────┘
                                                              │
              ┌───────────────────────────────────────────────▼───────────────┐
              │                  FLASK INFERENCE SERVER                        │
              │             application.py   (port 5000)                      │
              └───────────────────────────────────────────────┬───────────────┘
                                                              │
       ┌──────────────────────────────────────────────────────▼───────────────┐
       │                      DOCKER CONTAINER                                │
       │        python:3.11  │  pip install -e .  │  EXPOSE 5000             │
       └──────────────────────────────────────────────────────┬───────────────┘
                                                              │
  ┌───────────────────────────────────────────────────────────▼──────────────┐
  │                     KUBERNETES (Minikube / GCP)                          │
  │   Deployment (1 replica)  │  NodePort Service (30007)                   │
  └───────────────────────────────────────────────────────────┬──────────────┘
                                                              │
┌─────────────────────────────────────────────────────────────▼──────────────┐
│                   JENKINS SHARED LIBRARY CI/CD                              │
│                                                                             │
│  ┌─────────────┐  ┌──────────────────┐  ┌────────────┐  ┌───────────────┐ │
│  │ gitCheckout │→ │ dockerBuildAndPush│→ │installKubectl│→│  k8sDeploy   │ │
│  │  (Groovy)   │  │    (Groovy)      │  │  (Groovy)  │  │   (Groovy)    │ │
│  └─────────────┘  └──────────────────┘  └────────────┘  └───────────────┘ │
│                                                                             │
│              Triggered automatically via GitHub Webhook                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Language** | Python | 3.11 | Core runtime |
| **ML Framework** | scikit-learn | ≥ 1.4 | Modelling & preprocessing |
| **Experiment Tracking** | MLflow + DagsHub | Latest | Params, metrics, model registry |
| **Data Store** | MongoDB Atlas | Latest | Raw data source |
| **LLM** | Groq — LLaMA 3.1 8B Instant | Latest | AI feature analysis |
| **LLM Orchestration** | LangChain | ≥ 1.2 | Prompt chains, ChatGroq |
| **Web Framework** | Flask | Latest | REST inference server |
| **Containerisation** | Docker | Latest | Portable deployment image |
| **Orchestration** | Kubernetes (Minikube) | Latest | Scalable pod management |
| **CI/CD** | Jenkins Shared Library | LTS | Automated build & deploy |
| **Source Control** | GitHub + Webhooks | - | Trigger-based automation |
| **Cloud** | Google Cloud Platform (GCP) | - | VM & networking |
| **Logging** | Python `logging` | stdlib | Structured, dated log files |

---

## 📁 Project Structure

```
PROJECT/
│
├── src/                            ← Core source modules
│   ├── __init__.py
│   ├── logger.py                   ← Custom logging utility
│   ├── custom_exception.py         ← Structured error handling with traceback
│   ├── data_processing.py          ← DataProcessing class (load → preprocess → split)
│   └── model_training.py           ← ModelTraining class (train → evaluate → MLflow)
│
├── pipeline/
│   ├── __init__.py
│   └── training_pipeline.py        ← Orchestration entry point
│
├── artifacts/
│   ├── raw/
│   │   └── data.csv                ← Raw ingested dataset (100k rows)
│   ├── processed/
│   │   ├── X_train.pkl             ← Scaled training features
│   │   ├── X_test.pkl              ← Scaled test features
│   │   ├── y_train.pkl             ← Training labels
│   │   ├── y_test.pkl              ← Test labels
│   │   └── scaler.pkl              ← Fitted StandardScaler
│   └── models/
│       └── model.pkl               ← Serialised LogisticRegression model
│
├── k8s/
│   ├── deployment.yaml             ← Kubernetes Deployment manifest (1 replica)
│   └── service.yaml                ← NodePort Service (port 30007)
│
├── templates/
│   └── index.html                  ← Flask prediction form (Jinja2)
│
├── static/
│   └── style.css                   ← Frontend stylesheet
│
├── logs/                           ← Auto-generated dated log files
│
├── application.py                  ← Flask inference server (GET + POST)
├── Dockerfile                      ← Container build definition
├── Jenkinsfile                     ← Pipeline definition using shared library
├── requirements.txt                ← Project dependencies
└── setup.py                        ← Installable package configuration
│
└── Jenkins-shared-Lib/             ← Separate shared library repository
    └── vars/
        ├── gitCheckout.groovy
        ├── dockerBuildAndPush.groovy
        ├── installKubectl.groovy
        └── k8sDeploy.groovy
```

---

## 🔄 Pipeline Phases

### Phase 0 — Environment & Configuration

All credentials are managed through environment secrets — no credentials are ever hard-coded. The following environment variables must be configured prior to execution:

```python
import os
from google.colab import userdata

os.environ['MONGO_DB_URL']              = userdata.get('MONGO_DB_URL')
os.environ['GROQ_API_KEY']             = userdata.get('GROQ_API_KEY')
os.environ['MLFLOW_TRACKING_URI']      = userdata.get('MLFLOW_TRACKING_URI')
os.environ['MLFLOW_TRACKING_USERNAME'] = userdata.get('MLFLOW_TRACKING_USERNAME')
os.environ['MLFLOW_TRACKING_PASSWORD'] = userdata.get('MLFLOW_TRACKING_PASSWORD')
```

**MLflow Tracking Mode:** Set `USE_DAGSHUB = True` to log to the remote DagsHub server. Set to `False` to log locally to `./mlruns`.

---

### Phase 1 — Source Module Authoring

All source modules are authored as production-grade Python classes with full logging and structured exception handling.

#### `src/logger.py`

Configures a dated rotating log file under `./logs/` and streams output simultaneously to the console. Each module receives a named logger via `get_logger(__name__)`.

```python
LOG_FILE = os.path.join("logs", f"log_{datetime.now().strftime('%Y-%m-%d')}.log")
```

#### `src/custom_exception.py`

Wraps all exceptions with file name, line number, and original error context — enabling precise root cause analysis across the pipeline.

```python
class CustomException(Exception):
    def __init__(self, message: str, error_detail: Exception = None):
        self.error_message = self.get_detailed_error_message(message, error_detail)
        super().__init__(self.error_message)
```

#### `src/data_processing.py`

The `DataProcessing` class encapsulates the full preprocessing lifecycle:

| Method | Responsibility |
|---|---|
| `load_data()` | Reads raw CSV into a Pandas DataFrame |
| `preprocess()` | Parses `Timestamp`, extracts `Year/Month/Day/Hour`, applies `LabelEncoder` |
| `split_and_scale_and_save()` | Applies `StandardScaler`, performs 80/20 stratified split, serialises all artefacts |

#### `src/model_training.py`

The `ModelTraining` class encapsulates training, evaluation, and experiment tracking:

| Method | Responsibility |
|---|---|
| `load_data()` | Loads serialised train/test splits from `artifacts/processed/` |
| `train_model()` | Trains `LogisticRegression(max_iter=1000)`, serialises `model.pkl` |
| `evaluate_model()` | Computes accuracy, weighted precision, recall, and F1 |
| `log_to_mlflow()` | Logs all parameters, metrics, and model artefact to DagsHub |

---

### Phase 2 — Data Ingestion (MongoDB)

Data is sourced from a **MongoDB Atlas** collection (`mlops_project.machine_efficiency`) and written to `artifacts/raw/data.csv`. A robust fallback mechanism is included for offline or development scenarios.

```python
client  = MongoClient(os.environ['MONGO_DB_URL'], serverSelectionTimeoutMS=5000)
records = list(client['mlops_project']['machine_efficiency'].find({}, {'_id': 0}))
df      = pd.DataFrame(records)
df.to_csv('artifacts/raw/data.csv', index=False)
```

**Fallback:** If the MongoDB collection is unreachable or empty, the pipeline automatically falls back to a locally provided CSV file, ensuring uninterrupted execution.

---

### Phase 3 — Exploratory Data Analysis

A comprehensive EDA suite generates four publication-quality visualisations, all saved to `artifacts/`:

| Output File | Contents |
|---|---|
| `eda_class_distribution.png` | Bar chart + pie chart of `Efficiency_Status` class balance |
| `eda_correlation_heatmap.png` | Lower-triangular Pearson correlation heatmap across all numerical features |
| `eda_feature_distributions.png` | Overlapping histograms of five key sensor features segmented by efficiency class |

Key findings from EDA inform feature selection and guide the LLM analysis in Phase 4.

---

### Phase 4 — Groq LLM Feature Intelligence

An AI-powered feature analysis layer interrogates the dataset's correlation structure using **Groq's LLaMA 3.1 8B Instant** model via **LangChain ≥ 1.2**. The analysis is token-budget-aware (`max_tokens=512`) to remain within Groq's rate limits.

```python
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    max_tokens=512,
    api_key=os.environ["GROQ_API_KEY"],
)
```

The LLM is prompted with the top-six feature correlations with `Efficiency_Status` and tasked with:

1. Identifying and explaining the three most predictive features
2. Proposing a feature engineering improvement
3. Flagging potential data quality concerns

The generated insight is saved to `artifacts/llm_feature_insight.txt` and included in the final output bundle.

---

### Phase 5 — Data Processing Pipeline

The `DataProcessing` class is executed end-to-end against the ingested raw data:

```python
processor = DataProcessing(
    input_path="artifacts/raw/data.csv",
    output_path="artifacts/processed"
)
processor.run()
```

**Preprocessing steps:**

- `Timestamp` parsed and decomposed into `Year`, `Month`, `Day`, `Hour`
- `Machine_ID` and `Timestamp` columns dropped (non-predictive)
- `Operation_Mode` and `Efficiency_Status` label-encoded (alphabetical ordering: `High=0`, `Low=1`, `Medium=2`)
- All 14 features scaled with `StandardScaler`
- 80/20 stratified split preserves class distribution

**Feature set (14 predictors):**

```
Operation_Mode, Temperature_C, Vibration_Hz, Power_Consumption_kW,
Network_Latency_ms, Packet_Loss_%, Quality_Control_Defect_Rate_%,
Production_Speed_units_per_hr, Predictive_Maintenance_Score, Error_Rate_%,
Year, Month, Day, Hour
```

---

### Phase 6 — Model Training & MLflow Tracking

```python
trainer = ModelTraining(
    processed_data_path="artifacts/processed/",
    model_output_path="artifacts/models/"
)
metrics = trainer.run()
```

**Algorithm:** `LogisticRegression(random_state=42, max_iter=1000)`

**MLflow Experiment:** `MLOps-Jenkins-SharedLib`

All runs are logged to **DagsHub** with the following tracked artefacts:

| Type | Logged Items |
|---|---|
| Parameters | `model_type`, `max_iter`, `random_state`, `test_size`, `stratify` |
| Metrics | `accuracy`, `precision`, `recall`, `f1_score` (all weighted) |
| Artefacts | Serialised `LogisticRegression` model via `mlflow.sklearn.log_model` |

Post-training evaluation generates a confusion matrix heatmap and per-class F1 bar chart, saved to `artifacts/model_evaluation.png`.

---

### Phase 7 — Flask Inference Server

`application.py` serves as the production inference endpoint:

| Route | Method | Behaviour |
|---|---|---|
| `/` | `GET` | Renders the prediction form with all 14 feature input fields |
| `/` | `POST` | Accepts form data, scales inputs, runs model inference, returns label |

**Label mapping** (LabelEncoder alphabetical ordering):

```python
LABELS = {0: "High", 1: "Low", 2: "Medium"}
```

The server loads `model.pkl` and `scaler.pkl` once at startup, ensuring low-latency inference on each request.

---

### Phase 8 — Containerisation with Docker

The application is packaged as a portable Docker image using a minimal **Python 3.11** base:

```dockerfile
FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -e .

EXPOSE 5000

ENV FLASK_APP=application.py

CMD ["python", "application.py"]
```

**Build & run locally:**

```bash
docker build -t mlops-efficiency:latest .
docker run -d -p 5000:5000 mlops-efficiency:latest
```

**Push to DockerHub:**

```bash
docker tag mlops-efficiency:latest <your-dockerhub-username>/mlops-efficiency:latest
docker push <your-dockerhub-username>/mlops-efficiency:latest
```

> **Important:** Update the `image:` field in `k8s/deployment.yaml` to match your DockerHub repository before deploying.

---

### Phase 9 — Kubernetes Deployment

The application is deployed to a Kubernetes cluster (Minikube on GCP) using two manifest files.

#### `k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-container
          image: <your-dockerhub-username>/jenkins-shared-mlops-project:latest
          ports:
            - containerPort: 5000
```

#### `k8s/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  type: NodePort
  selector:
    app: flask-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
      nodePort: 30007
```

**Apply manifests manually:**

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods
kubectl get services
```

**Expose the application externally:**

```bash
kubectl port-forward deployment/flask-deployment 5000:5000 --address 0.0.0.0
```

Access the live application at: `http://<VM_EXTERNAL_IP>:5000`

---

### Phase 10 — Jenkins Shared Library CI/CD

The Jenkins pipeline is defined in `Jenkinsfile` and powered by a **reusable Shared Library** (`@Library('jenkins-shared')`). The shared library abstracts each stage into a named Groovy function, enabling consistent reuse across multiple projects.

#### `Jenkinsfile`

```groovy
@Library('jenkins-shared') _

pipeline {
    agent any
    environment {
        DOCKER_REPO = "your-dockerhub-username/jenkins-shared-mlops-project"
    }
    stages {
        stage('Checkout') {
            steps {
                gitCheckout(
                    'https://github.com/Prithu-Sarkar/GEN-AI-INDUSTRY-PROJECT_2.git',
                    '*/main',
                    'github-token'
                )
            }
        }

        stage('Build & Push Image') {
            steps {
                dockerBuildAndPush(DOCKER_REPO, 'dockerhub-token')
            }
        }

        stage('Install Kubectl') {
            steps {
                installKubectl()
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                k8sDeploy('kubeconfig')
            }
        }
    }
}
```

#### Shared Library Functions (`vars/`)

**`gitCheckout.groovy`** — Parameterised SCM checkout
```groovy
def call(String repoUrl, String branch, String credId) {
    checkout([
        $class: 'GitSCM',
        branches: [[name: branch]],
        userRemoteConfigs: [[credentialsId: credId, url: repoUrl]]
    ])
}
```

**`dockerBuildAndPush.groovy`** — Build image and push to DockerHub
```groovy
def call(String imageName, String registryCredId) {
    def dockerImage = docker.build("${imageName}:latest")
    docker.withRegistry('https://registry.hub.docker.com', registryCredId) {
        dockerImage.push('latest')
    }
}
```

**`installKubectl.groovy`** — Download and install `kubectl` binary
```groovy
def call() {
    sh '''
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl && mv kubectl /usr/local/bin/kubectl
    kubectl version --client
    '''
}
```

**`k8sDeploy.groovy`** — Apply Kubernetes manifests using kubeconfig secret
```groovy
def call(String kubeconfigCredId, String manifestsPath = "k8s") {
    kubeconfig(credentialsId: kubeconfigCredId, serverUrl: "") {
        sh """
        kubectl apply -f ${manifestsPath}/deployment.yaml
        kubectl apply -f ${manifestsPath}/service.yaml
        """
    }
}
```

---

### Phase 11 — GitHub Webhooks & Full Automation

GitHub Webhooks eliminate the need for manual pipeline triggers. Every `git push` to the `main` branch automatically fires the Jenkins pipeline.

#### Step 1 — Add Webhook in GitHub

Navigate to: **Repository → Settings → Webhooks → Add webhook**

| Field | Value |
|---|---|
| Payload URL | `http://<JENKINS_PUBLIC_IP>:8080/github-webhook/` |
| Content type | `application/json` |
| Trigger | Just the `push` event |

#### Step 2 — Configure Jenkins Build Trigger

In the Jenkins job configuration:

**Build Triggers** → ✅ **GitHub hook trigger for GITScm polling**

#### Step 3 — Verify End-to-End Automation

```bash
# Make any change and push
git add .
git commit -m "chore: trigger pipeline"
git push origin main
```

The Jenkins dashboard will reflect an automatically triggered build within seconds.

---

## 📊 Dataset Schema

The dataset comprises **100,000 rows** of industrial IoT sensor readings, collected across multiple machines over a continuous period.

| Column | Type | Description |
|---|---|---|
| `Timestamp` | datetime | ISO 8601 observation timestamp |
| `Machine_ID` | int | Unique machine identifier (dropped during preprocessing) |
| `Operation_Mode` | categorical | Operational state: `Active`, `Idle`, `Maintenance` |
| `Temperature_C` | float | Operating temperature in Celsius |
| `Vibration_Hz` | float | Vibration frequency in Hertz |
| `Power_Consumption_kW` | float | Instantaneous power draw in kilowatts |
| `Network_Latency_ms` | float | Control network round-trip latency in milliseconds |
| `Packet_Loss_%` | float | Network packet loss percentage |
| `Quality_Control_Defect_Rate_%` | float | Output defect rate percentage |
| `Production_Speed_units_per_hr` | float | Throughput in units per hour |
| `Predictive_Maintenance_Score` | float | Composite maintenance urgency score |
| `Error_Rate_%` | float | System error event rate |
| `Efficiency_Status` | categorical | **Target variable**: `High`, `Medium`, `Low` |

---

## 🔧 Jenkins Shared Library

The shared library is maintained as an independent repository and registered in Jenkins under the name `jenkins-shared`.

**Jenkins Configuration Path:**
`Manage Jenkins → Configure System → Global Pipeline Libraries`

| Setting | Value |
|---|---|
| Name | `jenkins-shared` |
| Default Version | `main` |
| SCM | Git |
| Repository URL | Your shared library repository URL |

> **Critical:** The library name in Jenkins must exactly match the `@Library('jenkins-shared')` declaration at the top of every `Jenkinsfile`.

---

## 🌐 Infrastructure Setup

### GCP Virtual Machine

| Configuration | Value |
|---|---|
| Machine Series | E2 Standard |
| RAM | 16 GB |
| Boot Disk | 150 GB |
| OS | Ubuntu 24.04 LTS |
| Networking | HTTP, HTTPS, Port Forwarding enabled |

### Docker Installation (Ubuntu)

Follow the [official Docker documentation](https://docs.docker.com/engine/install/ubuntu/) to install Docker. After installation:

```bash
# Run Docker without sudo
sudo usermod -aG docker $USER

# Enable Docker on boot
sudo systemctl enable docker.service
sudo systemctl enable containerd.service

# Verify installation
docker run hello-world
```

### Minikube Installation

```bash
# Install Minikube binary
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start the cluster (uses Docker as driver)
minikube start

# Verify cluster health
minikube status
kubectl get nodes
kubectl cluster-info
```

### Jenkins (Docker-in-Docker)

Jenkins runs as a Docker container on the **same network as Minikube**, enabling it to communicate with the cluster directly.

```bash
docker run -d --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(which docker):/usr/bin/docker \
  -u root \
  -e DOCKER_GID=$(getent group docker | cut -d: -f3) \
  --network minikube \
  jenkins/jenkins:lts
```

Retrieve the initial admin password:

```bash
docker logs jenkins
```

Access the Jenkins UI at: `http://<GCP_EXTERNAL_IP>:8080`

**Required Jenkins Plugins:**
- Docker
- Docker Pipeline
- Kubernetes

### Kubeconfig Secret for Jenkins

Jenkins requires access to the Kubernetes cluster credentials. The kubeconfig file must be base64-encoded and stored as a **Secret file** credential in Jenkins.

```bash
# Extract and base64-encode each certificate
cat ~/.minikube/ca.crt                              | base64 -w 0; echo
cat ~/.minikube/profiles/minikube/client.crt        | base64 -w 0; echo
cat ~/.minikube/profiles/minikube/client.key        | base64 -w 0; echo
```

Replace the certificate references in `~/.kube/config` with the base64-encoded values, save the file locally, then upload it to Jenkins:

**Jenkins → Manage Jenkins → Credentials → Global → Add Credentials**

| Field | Value |
|---|---|
| Kind | Secret file |
| File | Edited kubeconfig file |
| ID | `kubeconfig` |

---

## 🔑 Credentials & Secrets Reference

| Credential ID | Type | Platform | Purpose |
|---|---|---|---|
| `github-token` | Username + Password | Jenkins | GitHub repository checkout |
| `dockerhub-token` | Username + Password | Jenkins | Docker image push to DockerHub |
| `kubeconfig` | Secret file | Jenkins | Kubernetes cluster access |
| `MONGO_DB_URL` | Secret text | Runtime env | MongoDB Atlas connection |
| `GROQ_API_KEY` | Secret text | Runtime env | Groq LLM API access |
| `MLFLOW_TRACKING_URI` | Secret text | Runtime env | DagsHub MLflow server URL |
| `MLFLOW_TRACKING_USERNAME` | Secret text | Runtime env | DagsHub authentication |
| `MLFLOW_TRACKING_PASSWORD` | Secret text | Runtime env | DagsHub authentication |

> **Security Note:** Credential IDs in Jenkins must exactly match the string literals used in the `Jenkinsfile` and Groovy library functions. Any mismatch will cause a silent authentication failure.

---

## 💻 Local Development

### Prerequisites

- Python **3.11** (strictly — higher versions may cause ML library incompatibilities)
- Docker Desktop
- `kubectl` CLI
- Access credentials for MongoDB Atlas, DagsHub, and Groq

### Setup

```bash
# Clone the project repository
git clone https://github.com/Prithu-Sarkar/GEN-AI-INDUSTRY-PROJECT_2.git
cd GEN-AI-INDUSTRY-PROJECT_2

# Create and activate a Python 3.11 virtual environment
python3.11 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install all dependencies
pip install -e .

# Set required environment variables
export MONGO_DB_URL="mongodb+srv://..."
export GROQ_API_KEY="gsk_..."
export MLFLOW_TRACKING_URI="https://dagshub.com/..."
export MLFLOW_TRACKING_USERNAME="your-username"
export MLFLOW_TRACKING_PASSWORD="your-token"
```

### Run the Training Pipeline

```bash
python pipeline/training_pipeline.py
```

### Run the Inference Server

```bash
python application.py
# → http://localhost:5000
```

---

## 📈 MLflow Experiment Tracking

All training runs are tracked under the experiment name `MLOps-Jenkins-SharedLib` on DagsHub.

**Tracked per run:**

```
Parameters  →  model_type, max_iter, random_state, test_size, stratify
Metrics     →  accuracy, precision, recall, f1_score
Artefacts   →  LogisticRegression model (mlflow.sklearn format)
```

**View experiment history:**

```bash
mlflow ui --backend-store-uri $MLFLOW_TRACKING_URI
# → http://localhost:5000 (local UI)
# → https://dagshub.com/<username>/<repo>/experiments (remote)
```

---

## 🌐 Inference API

Once deployed, the Flask server accepts predictions via HTTP form POST:

**Endpoint:** `POST /`

**Input features (14 fields):**

```
Operation_Mode, Temperature_C, Vibration_Hz, Power_Consumption_kW,
Network_Latency_ms, Packet_Loss_%, Quality_Control_Defect_Rate_%,
Production_Speed_units_per_hr, Predictive_Maintenance_Score,
Error_Rate_%, Year, Month, Day, Hour
```

**Response:** One of `High`, `Medium`, or `Low` efficiency classification.

**Example cURL:**

```bash
curl -X POST http://<VM_IP>:5000/ \
  -d "Operation_Mode=1&Temperature_C=75.5&Vibration_Hz=3.2&Power_Consumption_kW=8.5&\
Network_Latency_ms=15.0&Packet_Loss_=0.5&Quality_Control_Defect_Rate_=4.2&\
Production_Speed_units_per_hr=450&Predictive_Maintenance_Score=0.7&\
Error_Rate_=5.1&Year=2024&Month=6&Day=15&Hour=14"
```

---

## 🤝 Contributing

Contributions are welcome. Please adhere to the following workflow:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes with a descriptive message following [Conventional Commits](https://www.conventionalcommits.org/)
4. Push to your fork and open a Pull Request against `main`
5. Ensure all pipeline stages pass before requesting review

---

<div align="center">

<br/>

**Built with precision. Deployed with confidence. Monitored with intelligence.**

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-Prithu--Sarkar-181717?style=for-the-badge&logo=github)](https://github.com/Prithu-Sarkar/GEN-AI-INDUSTRY-PROJECT_2)

<br/>

*MLOps · Jenkins Shared Library · Kubernetes · MLflow · MongoDB · Groq AI · LangChain*

</div>
