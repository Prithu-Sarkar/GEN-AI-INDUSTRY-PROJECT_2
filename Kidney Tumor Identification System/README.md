# Kidney Tumor Identification System

An end-to-end deep learning pipeline for automated classification of kidney tumors from CT scan images, built with VGG16 transfer learning and a full MLOps stack including MLflow, DagsHub, DVC, MongoDB, and CI/CD via GitHub Actions.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Pipeline Stages](#pipeline-stages)
- [Local Setup](#local-setup)
- [Running on Google Colab](#running-on-google-colab)
- [MLflow & DagsHub Tracking](#mlflow--dagshub-tracking)
- [DVC Pipeline](#dvc-pipeline)
- [CI/CD — AWS Deployment](#cicd--aws-deployment)
- [API Reference](#api-reference)
- [Results](#results)
- [Future Enhancements](#future-enhancements)

---

## Overview

This system classifies kidney CT scan images into two categories — **Tumor** and **Normal** — using a fine-tuned VGG16 convolutional neural network. The project is structured as a production-grade MLOps pipeline: every training run is version-controlled, every experiment is tracked, and every deployment is automated.

**Key capabilities:**
- Automated data ingestion from Google Drive
- Transfer learning with frozen VGG16 convolutional layers and a custom classification head
- Experiment tracking with MLflow logged to DagsHub
- Experiment metadata persisted to MongoDB Atlas
- Model checkpointing and TensorBoard callback support
- Flask REST API for real-time inference
- Containerised deployment on AWS EC2 via GitHub Actions + Amazon ECR

---

## Architecture

```
CT Scan Input
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Training Pipeline                        │
│                                                             │
│  Data Ingestion → Base Model Prep → Callbacks → Training    │
│        │                │                │          │       │
│   Google Drive        VGG16           TensorBoard  model.h5│
│   (gdown)          + Custom Head    + Checkpoint           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │   Evaluation     │
                    │  MLflow/DagsHub  │
                    │  MongoDB Atlas   │
                    │  scores.json     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Flask REST API  │
                    │  /predict route  │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Docker → ECR    │
                    │  → EC2 (port     │
                    │    8080)         │
                    └──────────────────┘
```

---

## Project Structure

```
Kidney Tumor Identification System/
├── .github/
│   └── workflows/
│       └── main.yaml               # GitHub Actions CI/CD pipeline
├── config/
│   └── config.yaml                 # Artifact paths and source URLs
├── research/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_prepare_base_model.ipynb
│   ├── 03_prepare_callbacks.ipynb
│   ├── 04_training.ipynb
│   └── 05_model_evaluation_with_mlflow.ipynb
├── src/
│   └── cnnClassifier/
│       ├── __init__.py             # Logger setup
│       ├── components/
│       │   ├── data_ingestion.py
│       │   ├── prepare_base_model.py
│       │   ├── prepare_callbacks.py
│       │   ├── training.py
│       │   └── evaluation.py
│       ├── config/
│       │   └── configuration.py    # ConfigurationManager
│       ├── constants/
│       │   └── __init__.py         # YAML file path constants
│       ├── entity/
│       │   └── config_entity.py    # Frozen dataclasses per stage
│       ├── pipeline/
│       │   └── predict.py          # Inference pipeline
│       └── utils/
│           └── common.py           # YAML, JSON, binary I/O helpers
├── templates/
│   └── index.html                  # Web UI for image upload
├── app.py                          # Flask application
├── main.py                         # Full pipeline runner
├── params.yaml                     # Hyperparameters
├── setup.py                        # Package installation
├── requirements.txt
├── scores.json                     # Latest evaluation output
└── metadata.txt                    # Human-readable experiment snapshot
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Deep Learning | TensorFlow 2.12, Keras, VGG16 |
| Experiment Tracking | MLflow 2.2.2, DagsHub |
| Data Versioning | DVC |
| Metadata Storage | MongoDB Atlas (pymongo) |
| Web Framework | Flask, Flask-CORS |
| Data Pipeline | gdown, NumPy, Pandas |
| Containerisation | Docker |
| Cloud | AWS EC2, AWS ECR |
| CI/CD | GitHub Actions |
| Colab Runtime | Google Colab (T4 GPU) |

---

## Pipeline Stages

### Stage 1 — Data Ingestion
Downloads the kidney CT scan dataset (~57 MB) from Google Drive using `gdown` and extracts it into `artifacts/data_ingestion/kidney-ct-scan-image/`. The directory contains two class folders: `Tumor` and `Normal`.

### Stage 2 — Prepare Base Model
Loads VGG16 with ImageNet weights (`include_top=False`) and attaches a custom classification head:
- `Flatten` layer
- `Dense(2, activation='softmax')`

All convolutional layers are frozen. The model is compiled with SGD (`lr=0.01`) and categorical cross-entropy loss.

**Saved artifacts:**
- `artifacts/prepare_base_model/base_model.h5` — frozen VGG16 backbone
- `artifacts/prepare_base_model/base_model_updated.h5` — full model with head

### Stage 3 — Prepare Callbacks
Instantiates two Keras callbacks:
- **TensorBoard** — writes timestamped event logs to `artifacts/prepare_callbacks/tensorboard_log_dir/`
- **ModelCheckpoint** — saves the best weights (by validation loss) to `artifacts/prepare_callbacks/checkpoint_dir/model.h5`

### Stage 4 — Training
Trains the model using `ImageDataGenerator` with an 80/20 train-validation split. When `AUGMENTATION: True`, the training generator applies rotation, flipping, shifting, shear, and zoom. GPU is used automatically when available.

**Saved artifact:** `artifacts/training/model.h5`

### Stage 5 — Evaluation
Evaluates the trained model on a 30% validation split, logs loss and accuracy to `scores.json`, and pushes the full experiment (params + metrics + model artifact) to MLflow / DagsHub. The model is registered under `VGG16KidneyTumorModel` in the MLflow Model Registry.

---

## Local Setup

### Prerequisites
- Python 3.8+
- Conda (recommended)
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/Kidney-Tumor-Identification-System.git
cd "Kidney Tumor Identification System"

# 2. Create and activate a conda environment
conda create -n kidney-cls python=3.8 -y
conda activate kidney-cls

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set MLflow / DagsHub environment variables
export MLFLOW_TRACKING_URI=https://dagshub.com/<username>/<repo>.mlflow
export MLFLOW_TRACKING_USERNAME=<dagshub-username>
export MLFLOW_TRACKING_PASSWORD=<dagshub-token>
export MONGO_DB_URL=<mongodb-atlas-connection-string>

# 5. Run the full training pipeline
python main.py

# 6. Launch the Flask inference server
python app.py
# Open http://localhost:8080
```

---

## Running on Google Colab

A fully self-contained Colab notebook (`Kidney_Tumor_Identification_System_Colab.ipynb`) is included. It writes all source files inline, requires no git clone, and runs the complete pipeline end-to-end.

**Required Colab Secrets** (add via the 🔑 icon in the sidebar):

| Secret Key | Value |
|---|---|
| `MONGO_DB_URL` | MongoDB Atlas connection string |
| `MLFLOW_TRACKING_URI` | DagsHub MLflow tracking URI |
| `MLFLOW_TRACKING_USERNAME` | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | DagsHub access token |

**Runtime:** Set to **GPU → T4** (Runtime → Change runtime type).

The final cell zips all artifacts, configs, scores, metadata, and logs and triggers an automatic browser download.

---

## MLflow & DagsHub Tracking

Every training run logs the following to DagsHub:

- **Parameters:** `EPOCHS`, `BATCH_SIZE`, `IMAGE_SIZE`, `LEARNING_RATE`, `AUGMENTATION`, `CLASSES`, `WEIGHTS`
- **Metrics:** `loss`, `accuracy`
- **Artifact:** Full Keras model registered as `VGG16KidneyTumorModel`

To launch the local MLflow UI:

```bash
mlflow ui
# Open http://localhost:5000
```

---

## DVC Pipeline

DVC is used for lightweight pipeline orchestration and data/model versioning.

```bash
# Initialise DVC
dvc init

# Reproduce the full pipeline
dvc repro

# Visualise the DAG
dvc dag
```

The `dvc.yaml` defines stages that map directly to the five pipeline components. Running `dvc repro` will re-execute only the stages whose inputs have changed.

---

## CI/CD — AWS Deployment

The GitHub Actions workflow (`.github/workflows/main.yaml`) triggers on every push to `main` and runs three jobs:

| Job | Description |
|---|---|
| `integration` | Lint + unit test checks |
| `build-and-push-ecr-image` | Builds Docker image, pushes to Amazon ECR |
| `Continuous-Deployment` | Pulls latest image on EC2 self-hosted runner, restarts container on port 8080 |

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `AWS_REGION` | e.g. `us-east-1` |
| `AWS_ECR_LOGIN_URI` | e.g. `566373416292.dkr.ecr.us-east-1.amazonaws.com` |
| `ECR_REPOSITORY_NAME` | Name of your ECR repository |

### IAM Permissions Required
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonEC2FullAccess`

### EC2 Docker Setup

```bash
sudo apt-get update -y && sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

After setup, register the EC2 instance as a GitHub self-hosted runner under **Settings → Actions → Runners**.

---

## API Reference

The Flask app exposes two endpoints:

### `GET /`
Returns the web UI for manual image upload and prediction.

### `POST /predict`
Accepts a base64-encoded CT scan image and returns the predicted class.

**Request body:**
```json
{
  "image": "<base64-encoded-image-string>"
}
```

**Response:**
```json
{
  "image": "<base64-encoded-image-string>",
  "prediction": "Tumor"
}
```

---

## Results

Evaluation metrics are saved to `scores.json` after each run and logged to MLflow.

```json
{
  "loss": <float>,
  "accuracy": <float>
}
```

A human-readable snapshot of every run (scores, hyperparameters, artifact paths, timestamp) is written to `metadata.txt` for safe Git storage — avoiding large binary rendering issues on GitHub.

---

## Future Enhancements

- **Advanced architectures** — benchmark against ResNet50, EfficientNetB0, and Vision Transformers
- **Grad-CAM visualisation** — overlay heatmaps on CT scans to highlight the regions driving the prediction
- **Multi-class classification** — expand labels to cover specific tumour subtypes (Angiomyolipoma, Renal Cell Carcinoma, etc.)
- **DICOM support** — ingest raw medical imaging files directly without preprocessing
- **Mobile API** — lightweight TFLite model export for mobile deployment
- **Automated retraining** — trigger DVC pipeline on new data arrival via MongoDB change streams

---

## License

This project is licensed under the terms of the [MIT License](LICENSE).
