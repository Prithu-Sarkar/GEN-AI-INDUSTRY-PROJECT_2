# 🫁 End-to-End Chest Disease Classification

> A production-grade, end-to-end MLOps project for classifying chest diseases (Adenocarcinoma Cancer vs. Normal) from CT scan images using VGG16 transfer learning — with full experiment tracking, pipeline orchestration, and automated CI/CD deployment to AWS.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [ML Pipeline](#ml-pipeline)
- [Getting Started](#getting-started)
- [Experiment Tracking with MLflow & DagsHub](#experiment-tracking-with-mlflow--dagshub)
- [Pipeline Orchestration with DVC](#pipeline-orchestration-with-dvc)
- [AWS CI/CD Deployment](#aws-cicd-deployment-with-github-actions)
- [Development Workflow](#development-workflow)

---

## Overview

This project demonstrates a complete MLOps lifecycle for medical image classification. A VGG16 convolutional neural network is fine-tuned on chest CT scan data to distinguish between **Adenocarcinoma Cancer** and **Normal** cases. The system is built with a modular, production-ready codebase and includes:

- Automated multi-stage training pipeline managed by **DVC**
- Experiment tracking and model registry via **MLflow** and **DagsHub**
- Containerised **Flask** web application for real-time inference
- Fully automated **CI/CD** pipeline that builds, pushes, and deploys to **AWS EC2** on every `main` branch push

---

## Technology Stack

| Category | Technology |
|---|---|
| Language | Python 3.8+ |
| Deep Learning | TensorFlow / Keras, VGG16 (ImageNet weights) |
| Experiment Tracking | MLflow 2.x, DagsHub |
| Pipeline Orchestration | DVC (Data Version Control) |
| Web Framework | Flask, Flask-Cors |
| Containerisation | Docker |
| CI/CD | GitHub Actions |
| Cloud Platform | AWS EC2, AWS ECR, IAM |
| Configuration | PyYAML, python-box, ensure |
| Utilities | Pandas, NumPy, Matplotlib, Seaborn, Joblib, gdown |

---

## Project Structure

```
├── .github/
│   └── workflows/
│       └── main.yaml              # CI/CD pipeline (lint → build → deploy)
├── config/
│   └── config.yaml                # Artifact paths and stage configuration
├── src/
│   └── cnnClassifier/
│       ├── __init__.py            # Logger setup
│       ├── components/            # Core business logic per stage
│       │   ├── data_ingestion.py
│       │   ├── prepare_base_model.py
│       │   ├── model_trainer.py
│       │   └── model_evaluation_mlflow.py
│       ├── config/
│       │   └── configuration.py   # ConfigurationManager — reads YAML, returns entities
│       ├── constants/
│       │   └── __init__.py        # CONFIG_FILE_PATH, PARAMS_FILE_PATH
│       ├── entity/
│       │   └── config_entity.py   # Frozen dataclasses for type-safe config
│       ├── pipeline/
│       │   ├── stage_01_data_ingestion.py
│       │   ├── stage_02_prepare_base_model.py
│       │   ├── stage_03_model_trainer.py
│       │   ├── stage_04_model_evaluation.py
│       │   └── prediction.py      # Inference pipeline
│       └── utils/
│           └── common.py          # read_yaml, save_json, get_size, image encode/decode
├── templates/
│   └── index.html                 # Flask frontend
├── dvc.yaml                       # DVC pipeline definition
├── dvc.lock                       # Reproducibility lock file
├── params.yaml                    # Hyperparameters
├── main.py                        # Full pipeline entry point
├── app.py                         # Flask application
├── setup.py                       # Package installation
├── requirements.txt               # Python dependencies
└── scores.json                    # Latest evaluation output
```

---

## ML Pipeline

The training pipeline is defined in `dvc.yaml` and consists of four sequential stages:

```
data_ingestion  →  prepare_base_model  →  training  →  evaluation
```

### Stage 1 — Data Ingestion
Downloads the Chest CT Scan dataset from Google Drive and extracts it into `artifacts/data_ingestion/`.

### Stage 2 — Prepare Base Model
Loads **VGG16** with pretrained ImageNet weights (`include_top=False`), freezes all convolutional layers, and attaches a custom 2-class softmax classification head. The uncompiled model architecture is saved to `artifacts/prepare_base_model/`.

### Stage 3 — Model Training
Loads the saved model architecture, compiles it with a fresh SGD optimizer, and fine-tunes it on the CT scan data with optional augmentation (rotation, flip, zoom, shear, shift). The trained model is saved to `artifacts/training/model.h5`.

### Stage 4 — Model Evaluation
Evaluates the trained model on a 30% validation split and logs loss, accuracy, all hyperparameters, and the model artefact to **MLflow / DagsHub**. Results are persisted locally in `scores.json`.

**Key hyperparameters** (configurable in `params.yaml`):

```yaml
IMAGE_SIZE:    [224, 224, 3]
BATCH_SIZE:    16
EPOCHS:        3
LEARNING_RATE: 0.01
AUGMENTATION:  True
CLASSES:       2
WEIGHTS:       imagenet
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Docker (for deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/entbappy/Chest-Cancer-Classification-Project.git
cd Chest-Cancer-Classification-Project

# Install the package and dependencies
pip install -r requirements.txt
pip install -e .
```

### Running the Full Pipeline

```bash
python main.py
```

Or using DVC for reproducible, cached execution:

```bash
dvc init
dvc repro
```

### Running the Flask Application

```bash
python app.py
```

The application will be available at `http://localhost:8080`. Upload a chest CT scan image to get a real-time prediction.

---

## Experiment Tracking with MLflow & DagsHub

All training runs are tracked on [DagsHub](https://dagshub.com/).

### Set environment variables before running:

```bash
export MLFLOW_TRACKING_URI=https://dagshub.com/<username>/<repo>.mlflow
export MLFLOW_TRACKING_USERNAME=<your_dagshub_username>
export MLFLOW_TRACKING_PASSWORD=<your_dagshub_token>
```

### Launch local MLflow UI:

```bash
mlflow ui
```

MLflow records:
- All hyperparameters from `params.yaml`
- Evaluation metrics: `loss`, `accuracy`
- The trained Keras model (registered as `VGG16Model`)

---

## Pipeline Orchestration with DVC

DVC manages pipeline stage dependencies, caching, and reproducibility.

```bash
# Initialise DVC
dvc init

# Run the full pipeline (skips unchanged stages)
dvc repro

# Visualise the pipeline DAG
dvc dag
```

**DVC vs MLflow — when to use which:**

| Tool | Purpose |
|---|---|
| **DVC** | Lightweight pipeline orchestration, data versioning, stage caching |
| **MLflow** | Production-grade experiment tracking, model logging, model registry |

---

## AWS CI/CD Deployment with GitHub Actions

Every push to the `main` branch triggers a three-stage automated workflow defined in `.github/workflows/main.yaml`:

```
CI (lint + test)  →  CD Build (Docker → ECR)  →  CD Deploy (ECR → EC2)
```

### Setup Steps

**1. Create an IAM user** with the following policies:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonEC2FullAccess`

**2. Create an ECR repository** to store the Docker image. Note the URI:
```
<account_id>.dkr.ecr.<region>.amazonaws.com/<repo-name>
```

**3. Launch an EC2 instance** (Ubuntu) and install Docker:
```bash
sudo apt-get update -y && sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

**4. Configure EC2 as a self-hosted GitHub Actions runner:**

Go to your GitHub repo → *Settings → Actions → Runners → New self-hosted runner* and follow the provided commands on the EC2 instance.

**5. Add the following GitHub Secrets** to your repository:

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `AWS_REGION` | e.g. `us-east-1` |
| `AWS_ECR_LOGIN_URI` | ECR registry URI (without repo name) |
| `ECR_REPOSITORY_NAME` | Name of your ECR repository |

Once configured, every push to `main` will automatically build the Docker image, push it to ECR, pull it on EC2, and restart the container on port `8080`.

---

## Development Workflow

When extending or modifying the project, follow this update sequence to ensure all layers stay in sync:

1. **`config/config.yaml`** — define new artifact paths or stage config
2. **`params.yaml`** — adjust hyperparameters
3. **`src/cnnClassifier/entity/config_entity.py`** — add/update frozen dataclasses
4. **`src/cnnClassifier/config/configuration.py`** — update `ConfigurationManager` to return new entities
5. **`src/cnnClassifier/components/`** — implement the business logic
6. **`src/cnnClassifier/pipeline/`** — wire the component into a pipeline stage
7. **`main.py`** — add the stage call to the end-to-end runner
8. **`dvc.yaml`** — register the new stage with its deps and outputs
