# 🐔 Poultry Disease Identification

[![Python](https://img.shields.io/badge/Python-3.8-blue?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Flask](https://img.shields.io/badge/Flask-API-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange?logo=mlflow)](https://mlflow.org/)
[![DagsHub](https://img.shields.io/badge/DagsHub-Experiment%20Tracking-purple)](https://dagshub.com/)
[![DVC](https://img.shields.io/badge/DVC-Pipeline-945DD6?logo=dvc)](https://dvc.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![AWS](https://img.shields.io/badge/Deploy-AWS%20ECR%20%2B%20EC2-FF9900?logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Azure](https://img.shields.io/badge/Deploy-Azure%20Web%20App-0078D4?logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)

---

## 📌 Project Overview

**Poultry Disease Identification** is a production-grade, end-to-end deep learning application that classifies poultry health from fecal images using **VGG16 Transfer Learning**. The model distinguishes between two classes — **Healthy** and **Coccidiosis** — providing a fast, accessible diagnostic tool for poultry farmers.

The project is built following rigorous **MLOps principles**, covering the complete lifecycle: data ingestion → model training → evaluation → experiment tracking → containerization → CI/CD → cloud deployment.

### What is Coccidiosis?
Coccidiosis is one of the most economically devastating poultry diseases worldwide, caused by *Eimeria* parasites. Early detection through fecal image analysis can significantly reduce mortality rates and production losses.

---

## 🎯 Learning Outcomes

- Master the **end-to-end ML lifecycle** from data ingestion to cloud deployment
- Write **modular, production-grade Python** code for Deep Learning using CNNs
- Apply **MLOps principles** including automated pipelines with DVC
- Gain hands-on experience with **containerization** using Docker
- Implement **CI/CD pipelines** using GitHub Actions for automated deployment
- Build and deploy scalable **REST APIs** using Flask
- Deploy applications to **AWS** (ECR + EC2) and **Azure** (Web App Service)

---

## 🗂️ Repository Structure

```
Poultry-Disease-Identification/
│
├── .github/
│   └── workflows/
│       ├── main.yaml                  # CI/CD → AWS ECR + EC2
│       └── main_chickenapp.yml        # CI/CD → Azure Web App
│
├── artifacts/                         # Auto-generated pipeline outputs
│   ├── data_ingestion/
│   │   └── Chicken-fecal-images/      # Downloaded & unzipped dataset
│   ├── prepare_base_model/
│   │   ├── base_model.h5              # Raw VGG16 backbone
│   │   └── base_model_updated.h5      # VGG16 + custom classification head
│   ├── prepare_callbacks/
│   │   ├── tensorboard_log_dir/       # TensorBoard logs
│   │   └── checkpoint_dir/model.h5    # Best model checkpoint
│   └── training/
│       └── model.h5                   # Final trained model
│
├── config/
│   └── config.yaml                    # Paths, URLs, artifact locations
│
├── research/
│   ├── 01_data_ingestion.ipynb        # Stage 01 — exploratory notebook
│   ├── 02_prepare_base_model.ipynb    # Stage 02 — exploratory notebook
│   ├── 03_prepare_callbacks.ipynb     # Stage 03 — exploratory notebook
│   ├── 04_training.ipynb              # Stage 04 — exploratory notebook
│   ├── 05_model_evaluation.ipynb      # Stage 05 — exploratory notebook
│   └── trials.ipynb                   # Utility trials (ConfigBox, ensure)
│
├── src/cnnClassifier/
│   ├── __init__.py                    # Logger setup
│   ├── components/
│   │   ├── data_ingestion.py          # Download + unzip dataset
│   │   ├── prepare_base_model.py      # Load VGG16 + add classification head
│   │   ├── prepare_callbacks.py       # TensorBoard + ModelCheckpoint callbacks
│   │   ├── training.py                # Train with augmentation & generators
│   │   └── model_evaluation_mlflow.py # Evaluate + log to MLflow / DagsHub
│   ├── config/
│   │   └── __init__.py                # ConfigurationManager
│   ├── constants/
│   │   └── __init__.py                # CONFIG_FILE_PATH, PARAMS_FILE_PATH
│   ├── entity/
│   │   └── __init__.py                # Frozen dataclasses for all configs
│   ├── pipeline/
│   │   ├── stage_01_data_ingestion.py
│   │   ├── stage_02_prepare_base_model.py
│   │   ├── stage_03_training.py
│   │   ├── stage_04_evaluation.py
│   │   └── predict.py                 # Inference pipeline
│   └── utils/
│       └── common.py                  # read_yaml, save_json, decode/encode image
│
├── templates/
│   └── index.html                     # Flask web UI
│
├── app.py                             # Flask REST API server
├── main.py                            # Orchestrates all 4 pipeline stages
├── params.yaml                        # Hyperparameters
├── dvc.yaml                           # DVC pipeline definition
├── dvc.lock                           # DVC pipeline lock file
├── scores.json                        # Latest evaluation metrics
├── setup.py                           # Package installer
├── requirements.txt                   # Python dependencies
├── Dockerfile                         # Container image definition
└── Poultry_Disease_Identification_Colab.ipynb  # Full Colab notebook
```

---

## 🧠 Model Architecture

The model uses **VGG16** as a frozen feature extractor with a custom classification head added on top.

```
Input Image (224 × 224 × 3)
        │
        ▼
┌───────────────────────┐
│   VGG16 Backbone      │  ← Pre-trained on ImageNet, all layers FROZEN
│   (Feature Extractor) │
└───────────────────────┘
        │
        ▼
    Flatten Layer
        │
        ▼
  Dense(2, softmax)          ← Custom head for binary classification
        │
        ▼
  Output: [Coccidiosis, Healthy]
```

**Training Strategy:** Transfer Learning with full backbone freezing. Only the dense classification head is trained, allowing fast convergence even with limited data.

---

## 🔁 MLOps Pipeline

```
config.yaml + params.yaml
         │
         ▼
Stage 01 ── Data Ingestion
         │   Download ZIP from GitHub URL
         │   Extract → artifacts/data_ingestion/Chicken-fecal-images/
         │
         ▼
Stage 02 ── Prepare Base Model
         │   Load VGG16 (ImageNet weights, include_top=False)
         │   Add Flatten + Dense(2, softmax) head
         │   Compile with SGD + CategoricalCrossentropy
         │   Save base_model.h5 and base_model_updated.h5
         │
         ▼
Stage 03 ── Prepare Callbacks
         │   TensorBoard callback (timestamped log dir)
         │   ModelCheckpoint (save_best_only=True)
         │
         ▼
Stage 04 ── Model Training
         │   ImageDataGenerator with augmentation
         │   (rotation, flip, shift, shear, zoom)
         │   80/20 train/validation split
         │   Fit model → save artifacts/training/model.h5
         │
         ▼
Stage 05 ── Model Evaluation + MLflow
             Evaluate on 30% validation split
             Log loss, accuracy, params → DagsHub / MLflow
             Register model → MLflow Model Registry
             Save scores → scores.json
```

### DVC Pipeline (Reproducible)

All stages are wired into DVC for full pipeline reproducibility:

```bash
dvc init
dvc repro      # Runs only changed stages
dvc dag        # Visualise the pipeline DAG
```

---

## ⚙️ Hyperparameters (`params.yaml`)

| Parameter | Value | Description |
|---|---|---|
| `IMAGE_SIZE` | `[224, 224, 3]` | VGG16 expected input shape |
| `BATCH_SIZE` | `16` | Training batch size |
| `EPOCHS` | `3` | Training epochs |
| `AUGMENTATION` | `True` | Enable data augmentation |
| `INCLUDE_TOP` | `False` | Exclude VGG16 classifier head |
| `WEIGHTS` | `imagenet` | Pre-trained weights |
| `CLASSES` | `2` | Coccidiosis / Healthy |
| `LEARNING_RATE` | `0.01` | SGD learning rate |

---

## 📊 Model Performance

| Metric | Value |
|---|---|
| **Validation Loss** | 1.8001 |
| **Validation Accuracy** | **73.28%** |

> Results are logged automatically to MLflow / DagsHub after each evaluation run and persisted in `scores.json`.

---

## 🚀 Getting Started (Local)

### Prerequisites

- Python 3.8
- Git
- Conda (recommended) or venv

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Prithu-Sarkar/GEN-AI-INDUSTRY-PROJECT_2.git
cd GEN-AI-INDUSTRY-PROJECT_2
```

### Step 2 — Create & Activate Virtual Environment

```bash
conda create -n poultry python=3.8 -y
conda activate poultry
```

Or with `venv`:

```bash
python -m venv venv
source venv/bin/activate       # Linux / Mac
venv\Scripts\activate          # Windows
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set Environment Variables

```bash
export MLFLOW_TRACKING_URI=<your-dagshub-mlflow-uri>
export MLFLOW_TRACKING_USERNAME=<your-dagshub-username>
export MLFLOW_TRACKING_PASSWORD=<your-dagshub-token>
```

### Step 5 — Run the Full Pipeline

```bash
python main.py
```

This executes all 4 stages sequentially — data ingestion, base model preparation, training, and evaluation.

### Step 6 — Launch the Flask App

```bash
python app.py
```

Open `http://localhost:5000` and upload a poultry fecal image to get a prediction.

---

## 🌐 Flask REST API

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Renders the web UI |
| `/train` | `GET/POST` | Triggers the full training pipeline |
| `/predict` | `POST` | Accepts base64 image, returns prediction |

### Prediction Request

```json
POST /predict
Content-Type: application/json

{
  "image": "<base64-encoded-image-string>"
}
```

### Prediction Response

```json
[{ "image": "Healthy" }]
```
or
```json
[{ "image": "Coccidiosis" }]
```

---

## 📓 Google Colab Notebook

The project includes `Poultry_Disease_Identification_Colab.ipynb` — a fully self-contained notebook that builds and runs the entire pipeline from scratch inside Colab with **no local setup needed**.

### Required Colab Secrets

| Secret Key | Description |
|---|---|
| `MONGO_DB_URL` | MongoDB Atlas connection string |
| `MLFLOW_TRACKING_URI` | DagsHub MLflow tracking URI |
| `MLFLOW_TRACKING_USERNAME` | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | DagsHub access token |

### Notebook Flow

| Cell | Stage |
|---|---|
| 0 | Environment variables from Colab Secrets |
| 1 | Install all dependencies |
| 2–3 | Create project root & full directory structure |
| 4 | Write `config.yaml` and `params.yaml` |
| 5a–5f | Write all `src/` modules, pipeline stages, Flask app |
| 6 | Install `cnnClassifier` package via `pip install -e .` |
| 7 | Stage 01 — Data ingestion (auto-downloads dataset) |
| 8 | Stage 02 — Prepare VGG16 base model |
| 9 | Stage 03 — Prepare TensorBoard + Checkpoint callbacks |
| 10 | Stage 04 — Model training with augmentation |
| 11 | Stage 05 — Evaluation + MLflow logging to DagsHub |
| 12 | Validation metrics bar chart |
| 13 | Prediction demo on a sample image |
| 14 | ZIP entire project and auto-download |

> ✅ **Dataset downloads automatically** from a public GitHub URL — no Kaggle API key or manual upload required.

---

## 🐳 Docker

### Build the Image

```bash
docker build -t poultry-disease-app:latest .
```

### Run the Container

```bash
docker run -p 5000:5000 poultry-disease-app:latest
```

### Dockerfile

```dockerfile
FROM python:3.8-slim-buster

RUN apt update -y && apt install awscli -y
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD ["python3", "app.py"]
```

---

## 🔄 CI/CD — GitHub Actions

### Workflow 1 — AWS ECR + EC2 (`main.yaml`)

Triggers automatically on every push to `main`.

```
Push to main
     │
     ▼
① Continuous Integration
   └── Lint code  |  Run unit tests
     │
     ▼
② Continuous Delivery
   └── Configure AWS credentials
   └── Login to Amazon ECR
   └── Build & push Docker image to ECR
     │
     ▼
③ Continuous Deployment  (self-hosted EC2 runner)
   └── Pull latest image from ECR
   └── Run container on EC2 (port 8080)
   └── Prune old images
```

**Required GitHub Secrets:**

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `AWS_REGION` | e.g. `us-east-1` |
| `AWS_ECR_LOGIN_URI` | ECR registry URI |
| `ECR_REPOSITORY_NAME` | ECR repository name |

### Workflow 2 — Azure Web App (`main_chickenapp.yml`)

Triggers on push to `main` or manual workflow dispatch.

```
Push to main
     │
     ▼
① Build
   └── Docker Buildx setup
   └── Login to Azure Container Registry
   └── Build & push image (tagged with commit SHA)
     │
     ▼
② Deploy
   └── Azure Web Apps Deploy → production slot
```

---

## ☁️ Manual Cloud Deployment

### AWS

```bash
# Build, tag, and push to ECR
docker build -t <ecr-uri>/poultry-app:latest .
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <ecr-uri>
docker push <ecr-uri>/poultry-app:latest

# On EC2 — pull and run
docker pull <ecr-uri>/poultry-app:latest
docker run -d -p 8080:8080 <ecr-uri>/poultry-app:latest
```

**IAM Policies required:** `AmazonEC2ContainerRegistryFullAccess`, `AmazonEC2FullAccess`

### Azure

```bash
docker build -t chickenapp.azurecr.io/chicken:latest .
docker login chickenapp.azurecr.io
docker push chickenapp.azurecr.io/chicken:latest
```

Then configure your Azure Web App to pull from ACR.

---

## 🧪 Experiment Tracking — MLflow + DagsHub

Every evaluation run automatically logs:

| Logged Item | Details |
|---|---|
| **Parameters** | `image_size`, `batch_size` |
| **Metrics** | `loss`, `accuracy` |
| **Model Artifact** | Registered as `VGG16PoultryDisease` |

All runs are visible in the **DagsHub** experiments dashboard with full parameter-to-metric traceability.

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.8 |
| Deep Learning | TensorFlow 2.x / Keras |
| Model | VGG16 Transfer Learning (ImageNet) |
| Data Processing | NumPy, Pandas |
| Visualization | Matplotlib, Seaborn |
| Configuration | python-box, PyYAML, ensure |
| Pipeline Automation | DVC |
| Experiment Tracking | MLflow + DagsHub |
| Web Framework | Flask + Flask-CORS |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Cloud Option A | AWS ECR + EC2 |
| Cloud Option B | Azure Container Registry + Web App |
| Notebook | Google Colab |

---

## 📋 Development Workflow

When extending the project, always follow this order:

```
1. config/config.yaml          ← Add new paths or source URLs
2. params.yaml                 ← Add new hyperparameters
3. src/cnnClassifier/entity    ← Add new frozen dataclass
4. src/cnnClassifier/config    ← Add getter in ConfigurationManager
5. src/cnnClassifier/components ← Implement component logic
6. src/cnnClassifier/pipeline  ← Add or update stage script
7. main.py                     ← Wire stage into orchestrator
8. dvc.yaml                    ← Register stage in DVC DAG
```

---

## 🔗 References

- [VGG16 Paper — Simonyan & Zisserman, 2014](https://arxiv.org/abs/1409.1556)
- [TensorFlow Transfer Learning Guide](https://www.tensorflow.org/tutorials/images/transfer_learning)
- [DVC Documentation](https://dvc.org/doc)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [DagsHub](https://dagshub.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [Azure Web Apps Deploy Action](https://github.com/Azure/webapps-deploy)

---

## 👤 Author

**Prithu Sarkar**
[GitHub](https://github.com/Prithu-Sarkar) · [Repository](https://github.com/Prithu-Sarkar/GEN-AI-INDUSTRY-PROJECT_2)

---

> *This project demonstrates how a real-world Computer Vision application can be built, tracked, containerized, and deployed using modern MLOps practices — from a research notebook all the way to a live cloud endpoint.*
