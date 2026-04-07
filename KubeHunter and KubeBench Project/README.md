# 🌧️ MLOps — Rain in Australia Prediction with Kubernetes Security Scanning

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-black?logo=flask)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?logo=mongodb)](https://www.mongodb.com/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange?logo=mlflow)](https://mlflow.org/)
[![DagsHub](https://img.shields.io/badge/DagsHub-Experiment%20Tracking-purple)](https://dagshub.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-326CE5?logo=kubernetes)](https://kubernetes.io/)
[![KubeHunter](https://img.shields.io/badge/Kube--Hunter-Security%20Scan-red)](https://github.com/aquasecurity/kube-hunter)
[![KubeBench](https://img.shields.io/badge/Kube--Bench-CIS%20Benchmark-orange)](https://github.com/aquasecurity/kube-bench)

---

## 📌 Project Overview

This is a **full end-to-end MLOps project** that builds, tracks, deploys, and security-scans a machine learning application on Kubernetes. The ML model predicts whether it will rain tomorrow based on Australian weather station data.

The project covers the complete lifecycle:

- **Data Engineering** — raw data ingestion from MongoDB Atlas
- **ML Pipeline** — data validation → transformation → model training → evaluation
- **Experiment Tracking** — MLflow + DagsHub for logging parameters, metrics, and model artifacts
- **Web App** — Flask prediction API served via a web UI
- **Containerization** — Dockerized Flask app
- **Kubernetes Deployment** — deployed on Minikube inside a GCP VM
- **Security Scanning** — Kube-Hunter (penetration testing) and Kube-Bench (CIS benchmark audit)
- **Google Colab** — full pipeline notebook for reproducibility

---

## 🗂️ Repository Structure

```
├── artifacts/
│   ├── raw/                    # Raw ingested data (CSV)
│   ├── processed/              # Scaled features, train/test splits, encoders
│   └── models/                 # Trained model (model.pkl), evaluation plots
├── notebook/
│   └── MLOps_RainAustralia_Colab.ipynb   # End-to-end Colab notebook
├── pipeline/                   # Modular pipeline stage scripts
├── src/                        # Core source modules (ingestion, transformation, training)
├── static/                     # Static assets for Flask UI
├── templates/
│   └── index.html              # Flask web UI template
├── application.py              # Flask prediction server
├── setup.py                    # Package setup
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition
├── k8s-deployment.yaml         # Kubernetes Deployment + Service manifest
├── insecure-rbac.yaml          # RBAC manifest (intentional vulnerabilities for scanning demo)
├── kube-hunter.yaml            # Kube-Hunter Job manifest
├── kube-bench.yaml             # Kube-Bench Pod manifest
└── kubebench-report-generator.py  # Script to parse kube-bench JSON → Markdown report
```

---

## 🧠 ML Pipeline

### Dataset
The [Rain in Australia](https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package) dataset contains daily weather observations from numerous Australian weather stations. The task is binary classification: **will it rain tomorrow? (Yes / No)**

### Features Used
```
Location, MinTemp, MaxTemp, Rainfall, Evaporation, Sunshine,
WindGustDir, WindGustSpeed, WindDir9am, WindDir3pm,
WindSpeed9am, WindSpeed3pm, Humidity9am, Humidity3pm,
Pressure9am, Pressure3pm, Cloud9am, Cloud3pm, Temp9am,
Temp3pm, RainToday, Year, Month, Day
```

### Pipeline Stages

```
MongoDB Atlas
     │
     ▼
① Data Ingestion ──────── Pull raw docs → artifacts/raw/rain_data.csv
     │
     ▼
② Data Validation ─────── Column checks, null %, target distribution
     │
     ▼
③ Data Transformation ─── Date parsing, LabelEncoding, StandardScaler,
     │                     median imputation, train/test split (80/20)
     ▼
④ Model Training ──────── RandomForest + GradientBoosting
     │                     logged to MLflow / DagsHub
     ▼
⑤ Model Evaluation ────── Accuracy, F1, Precision, Recall, ROC-AUC,
     │                     Confusion Matrix, ROC Curve plots
     ▼
⑥ Artifact Export ─────── artifacts/models/model.pkl
```

### Models Trained

| Model | Key Hyperparameters |
|---|---|
| RandomForestClassifier | `n_estimators=100`, `max_depth=10`, `min_samples_split=5` |
| GradientBoostingClassifier | `n_estimators=100`, `learning_rate=0.1`, `max_depth=5` |

The best model (by F1 score) is automatically saved as `artifacts/models/model.pkl` and registered in MLflow.

---

## 🧪 Experiment Tracking — MLflow + DagsHub

All training runs are logged to [DagsHub](https://dagshub.com/) via MLflow Remote Tracking.

Each run logs:
- **Parameters**: model type, hyperparameters
- **Metrics**: accuracy, f1_score, precision, recall, roc_auc
- **Artifacts**: model pickle, confusion matrix plot, ROC curve, feature importance chart

### Configure Secrets (Colab)

Add the following to your **Colab Secrets** before running the notebook:

| Secret Key | Description |
|---|---|
| `MONGO_DB_URL` | MongoDB Atlas connection string |
| `MLFLOW_TRACKING_URI` | DagsHub MLflow URI |
| `MLFLOW_TRACKING_USERNAME` | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | DagsHub access token |

---

## 🚀 Running the Colab Notebook

Open `notebook/MLOps_RainAustralia_Colab.ipynb` in Google Colab.

The notebook runs all pipeline stages end-to-end in sequence:

| Cell | Stage |
|---|---|
| 0 | Set environment variables from Colab Secrets |
| 1 | Install all dependencies |
| 2 | Clone this repository |
| 3 | Create artifact directories |
| 4 | Data ingestion from MongoDB (with public dataset fallback) |
| 5 | Data validation |
| 6 | Data transformation + scaling |
| 7 | Model training + MLflow logging |
| 8 | Model evaluation — plots |
| 9 | Feature importance |
| 10 | Save best model as `model.pkl` |
| 11 | Log plots and model artifact to MLflow |
| 12 | (Optional) Seed MongoDB with the public dataset |
| 13 | Final summary |

---

## 🌐 Flask Web Application

The trained model is served via a Flask web app (`application.py`). Users fill in weather feature values through a form and receive a **"Rain Tomorrow: YES / NO"** prediction.

### Run Locally

```bash
# 1. Install dependencies
pip install -e .

# 2. Make sure model.pkl is present at artifacts/models/model.pkl

# 3. Run the server
python application.py
```

Visit `http://localhost:5000` in your browser.

---

## 🐳 Docker

### Build the Image

```bash
docker build -t flask-app:latest .
```

### Run the Container

```bash
docker run -p 5000:5000 flask-app:latest
```

### Dockerfile Summary

```dockerfile
FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -e .
EXPOSE 5000
ENV FLASK_APP=application.py
CMD ["python", "application.py"]
```

---

## ☸️ Kubernetes Deployment on GCP (Minikube)

### 1. GCP VM Setup

Create a VM on Google Compute Engine with the following spec:

| Setting | Value |
|---|---|
| Machine Type | E2 Standard |
| RAM | 16 GB |
| Boot Disk | 150 GB, Ubuntu 24.04 LTS |
| Networking | Enable HTTP, HTTPS, Port Forwarding |

SSH into the VM from the GCP Console.

### 2. Install Docker

Follow the [official Docker docs](https://docs.docker.com) to install Docker on Ubuntu, then:

```bash
# Verify
docker run hello-world

# Run without sudo
sudo usermod -aG docker $USER && newgrp docker

# Enable on boot
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

### 3. Install Minikube

Follow [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/) — select Linux / x86 / Binary download.

```bash
minikube start
minikube status
```

### 4. Install kubectl

```bash
sudo snap install kubectl --classic
kubectl version --client
```

### 5. Enable Minikube Addons

```bash
minikube addons enable dashboard
minikube addons enable metrics-server
minikube addons enable ingress
```

### 6. Create Namespace

```bash
kubectl create namespace vulnerable-test
```

### 7. Apply RBAC

```bash
kubectl apply -f insecure-rbac.yaml
```

### 8. Build & Deploy the App

```bash
# Point Docker to Minikube's Docker daemon
eval $(minikube docker-env)

# Build image inside Minikube
docker build -t flask-app:latest .

# Deploy to Kubernetes
kubectl apply -f k8s-deployment.yaml

# Check pods
kubectl get pods -n vulnerable-test
```

### 9. Access the Application

```bash
kubectl port-forward svc/vulnerable-flask-service 5000:80 -n vulnerable-test --address 0.0.0.0
```

Open `http://<GCP-EXTERNAL-IP>:5000` in your browser.

---

## 🔐 Security Scanning

### Intentional Vulnerabilities (for Demo)

The deployment manifest and RBAC file are intentionally configured with security misconfigurations to demonstrate real-world risks:

| Vulnerability | Location | Description |
|---|---|---|
| Running as root | `k8s-deployment.yaml` | `runAsUser: 0` |
| Privileged container | `k8s-deployment.yaml` | `privileged: true` |
| Privilege escalation allowed | `k8s-deployment.yaml` | `allowPrivilegeEscalation: true` |
| Host filesystem mounted | `k8s-deployment.yaml` | `hostPath: /` mounted at `/host` |
| Hardcoded secret | `k8s-deployment.yaml` | `SECRET_PASSWORD: "admin123"` |
| Cluster-admin RBAC | `insecure-rbac.yaml` | Service account bound to `cluster-admin` |
| Excessive capabilities | `insecure-rbac.yaml` | `SYS_ADMIN`, `NET_ADMIN` added |

> ⚠️ These are **intentional** for security scanning demonstration only. Never use these configurations in production.

---

### 🦅 Kube-Hunter — Penetration Testing

Kube-Hunter actively probes the cluster from inside a pod to find exploitable vulnerabilities.

**Deploy the Job:**
```bash
kubectl create -f kube-hunter.yaml
```

**Find the pod name:**
```bash
kubectl get pods
```

**View scan results:**
```bash
kubectl logs <kube-hunter-pod-name>
```

The output lists discovered vulnerabilities such as open API server access, exposed secrets, privileged container escape paths, and insecure service account tokens.

---

### 📋 Kube-Bench — CIS Benchmark Audit

Kube-Bench checks cluster configuration against the [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes) and reports PASS / FAIL / WARN for each control.

**Deploy kube-bench:**
```bash
kubectl apply -f kube-bench.yaml
```

**Extract JSON report:**
```bash
kubectl logs kube-bench | sed -n '/^{/,/^}$/p' > kube-bench-results.json
```

**Pretty-print with jq:**
```bash
sudo apt install jq
jq . kube-bench-results.json
```

**Generate a Markdown report:**
```bash
python3 kubebench-report-generator.py
```

This produces `kube_bench_report.md` with a full structured breakdown of every CIS control — pass/fail counts, reasons, and remediation steps.

---

### Verify Vulnerabilities Manually

```bash
# Check if container can access host filesystem
kubectl exec -it <pod-name> -n vulnerable-test -- ls /host

# Open shell with elevated privileges
kubectl exec -it <pod-name> -n vulnerable-test -- /bin/bash

# List secrets across all namespaces
kubectl get secrets --all-namespaces

# Check what actions the insecure service account can perform
kubectl auth can-i --list \
  --as=system:serviceaccount:vulnerable-test:insecure-service-account
```

---

## 🛠️ Tech Stack

| Category | Tool / Library |
|---|---|
| Language | Python 3.11 |
| ML | scikit-learn (RandomForest, GradientBoosting) |
| Data | pandas, numpy |
| Database | MongoDB Atlas (pymongo) |
| Experiment Tracking | MLflow + DagsHub |
| Web Framework | Flask |
| Containerization | Docker |
| Orchestration | Kubernetes (Minikube) |
| Cloud | Google Cloud Platform (GCP VM) |
| Security — Pen Test | Kube-Hunter (Aqua Security) |
| Security — Audit | Kube-Bench (Aqua Security) |
| Notebook | Google Colab |

---

## ⚙️ Local Setup (Non-Colab)

```bash
# 1. Clone the repository
git clone https://github.com/Prithu-Sarkar/GEN-AI-INDUSTRY-PROJECT_2.git
cd GEN-AI-INDUSTRY-PROJECT_2

# 2. Create a virtual environment (Python 3.11 required)
python3.11 -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -e .

# 4. Set environment variables
export MONGO_DB_URL="your-mongodb-atlas-uri"
export MLFLOW_TRACKING_URI="your-dagshub-mlflow-uri"
export MLFLOW_TRACKING_USERNAME="your-dagshub-username"
export MLFLOW_TRACKING_PASSWORD="your-dagshub-token"

# 5. Run the pipeline stages
python pipeline/data_ingestion.py
python pipeline/data_transformation.py
python pipeline/model_training.py

# 6. Run the Flask app
python application.py
```

> **Python 3.11 is required.** Versions above 3.11 have limited ML library compatibility; lower versions may cause dependency issues.

---

## 📊 Sample Results

| Metric | RandomForest | GradientBoosting |
|---|---|---|
| Accuracy | ~0.857 | ~0.863 |
| F1 Score | ~0.72 | ~0.74 |
| ROC-AUC | ~0.88 | ~0.90 |

*(Actual values vary by run and data split)*

---

## 📁 Key Files Reference

| File | Purpose |
|---|---|
| `application.py` | Flask web server — loads model, serves predictions |
| `Dockerfile` | Container image for the Flask app |
| `k8s-deployment.yaml` | K8s Deployment + NodePort Service (with intentional vulns) |
| `insecure-rbac.yaml` | ServiceAccount + ClusterRoleBinding + Deployment (insecure) |
| `kube-hunter.yaml` | Kube-Hunter batch job for active vulnerability scanning |
| `kube-bench.yaml` | Kube-Bench pod for CIS benchmark audit |
| `kubebench-report-generator.py` | Converts kube-bench JSON output → Markdown report |
| `setup.py` | Package installer (reads from requirements.txt) |
| `requirements.txt` | All Python dependencies |

---

## 🔗 References

- [Aqua Kube-Hunter](https://github.com/aquasecurity/kube-hunter)
- [Aqua Kube-Bench](https://github.com/aquasecurity/kube-bench)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [DagsHub](https://dagshub.com/)
- [Minikube Docs](https://minikube.sigs.k8s.io/docs/)
- [Rain in Australia Dataset — Kaggle](https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package)

---

## 👤 Author

**Prithu Sarkar**
[GitHub](https://github.com/Prithu-Sarkar) · [Repository](https://github.com/Prithu-Sarkar/GEN-AI-INDUSTRY-PROJECT_2)

---

> *This project is built for educational purposes — demonstrating how MLOps practices, containerization, Kubernetes deployment, and cloud-native security scanning come together in a single real-world pipeline.*
