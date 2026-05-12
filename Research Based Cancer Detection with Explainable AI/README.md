<div align="center">

<img src="https://img.shields.io/badge/ThyroCheck_AI-Precision_Diagnostics-00C0A3?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0tMiAxNWwtNS01IDEuNDEtMS40MUwxMCAxNC4xN2w3LjU5LTcuNTlMMTkgOGwtOSA5eiIvPjwvc3ZnPg==" />

# ThyroCheck AI
### Research-Grade Thyroid Cancer Detection System with Explainable AI

<p align="center">
  <img src="https://img.shields.io/badge/TensorFlow-2.15-FF6F00?style=flat-square&logo=tensorflow&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-Production-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-≥1.0-1C3C3C?style=flat-square&logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-LLaMA_3.1-F55036?style=flat-square&logo=meta&logoColor=white" />
  <img src="https://img.shields.io/badge/MLflow-2.13-0194E2?style=flat-square&logo=mlflow&logoColor=white" />
  <img src="https://img.shields.io/badge/MongoDB_Atlas-Free_Tier-47A248?style=flat-square&logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/HuggingFace-Model_Hub-FFD21E?style=flat-square&logo=huggingface&logoColor=black" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" />
</p>

<p align="center">
  <a href="https://github.com/d-hackmt/thyroid_detection_xai"><img src="https://img.shields.io/badge/GitHub-Repository-181717?style=flat-square&logo=github" /></a>
  <a href="https://huggingface.co/Diveshj/thyroid_models"><img src="https://img.shields.io/badge/HuggingFace-Diveshj%2Fthyroid__models-FFD21E?style=flat-square&logo=huggingface&logoColor=black" /></a>
  <a href="https://www.linkedin.com/in/dhackmt"><img src="https://img.shields.io/badge/LinkedIn-d--hackmt-0A66C2?style=flat-square&logo=linkedin" /></a>
</p>

---

*Empowering clinicians with Fibonacci-scaled neural architecture, gradient-weighted explainability, and LLM-generated diagnostic narratives — bridging research innovation with clinical interpretability.*

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture at a Glance](#-architecture-at-a-glance)
- [FibonacciNet — Novel CNN Architecture](#-fibonaccinet--novel-cnn-architecture)
- [Explainability — Grad-CAM](#-explainability--grad-cam)
- [LLM Diagnostic Narrative — LangChain + Groq](#-llm-diagnostic-narrative--langchain--groq)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [API Reference](#-api-reference)
- [Experiment Pipeline — Notebook](#-experiment-pipeline--notebook)
- [MLflow & DagsHub Tracking](#-mlflow--dagshub-tracking)
- [MongoDB Persistence](#-mongodb-persistence)
- [Report Generation](#-report-generation)
- [Configuration](#-configuration)
- [Dataset](#-dataset)
- [Results & Metrics](#-results--metrics)
- [Research Foundation](#-research-foundation)
- [Authors & Acknowledgements](#-authors--acknowledgements)

---

## 🔬 Overview

**ThyroCheck AI** is a research-grade, end-to-end thyroid cancer detection system built on a custom deep learning architecture inspired by the Fibonacci number sequence. The system accepts thyroid ultrasound images and delivers:

- **Binary classification** — Benign vs. Malignant
- **Gradient-weighted visual explanations** via Grad-CAM over the final depthwise separable convolutional layer
- **LLM-generated clinical narratives** via LangChain ≥ 1.0 + Groq (LLaMA 3.1)
- **Downloadable DOCX diagnostic reports** with scan images, heatmaps, probability coefficients, and AI commentary
- **Full experiment tracking** via MLflow and DagsHub
- **Persistent result storage** via MongoDB Atlas
- **Dual deployment interfaces** — a production FastAPI web application and a Streamlit analytics dashboard

The system is not a black-box: every prediction is accompanied by a spatial attention map that highlights the exact nodule regions driving the model's output, making findings interpretable to radiologists and researchers alike.

---

## 🏛️ Architecture at a Glance

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ThyroCheck AI System                        │
├────────────────────────┬────────────────────────────────────────────┤
│     Web Interface      │          Analytics Dashboard               │
│  FastAPI + HTML/CSS    │         Streamlit Application              │
│     (Port 8000)        │           (Port 8501)                      │
└────────────┬───────────┴───────────────────┬────────────────────────┘
             │                               │
             ▼                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Backend — FastAPI Router                     │
│   POST /analyze          POST /report         GET /                 │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
             ┌─────────────────────┼──────────────────────┐
             ▼                     ▼                      ▼
┌────────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│  Image Preprocessor│  │   FibonacciNet   │  │    Grad-CAM Engine   │
│  utils/processing  │  │ (HuggingFace Hub)│  │    utils/gradcam     │
│  224×224 · RGB     │  │ Sigmoid → Binary │  │  Avg2MaxPool Layer   │
└────────────────────┘  └──────────────────┘  └──────────────────────┘
                                   │
             ┌─────────────────────┼──────────────────────┐
             ▼                     ▼                      ▼
┌────────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│   MongoDB Atlas    │  │  MLflow / DagsHub│  │  LangChain + Groq    │
│  Result Persistence│  │  Experiment Track│  │  LLaMA 3.1 Narrative │
└────────────────────┘  └──────────────────┘  └──────────────────────┘
                                   │
                                   ▼
                      ┌────────────────────────┐
                      │  DOCX Report Generator │
                      │  utils/report_generator│
                      └────────────────────────┘
```

---

## 🧠 FibonacciNet — Novel CNN Architecture

FibonacciNet is the core contribution of this research. It is a custom convolutional neural network whose filter counts in successive blocks follow the **Fibonacci number sequence** — a mathematically motivated progression designed to create a natural, gradually expanding representational capacity:

```
Block 1 → Block 2 → Block 3 → Block 4 → Block 5 → Block 6 → Block 7
  21         34         55         89        144        233        377
```

### Architectural Innovations

#### 1. Partial Connection Blocks (PCB) — Skip Bridges
Two non-contiguous skip connections bridge feature maps across the network using the novel **Avg2MaxPooling** layer rather than standard identity shortcuts:

```
Block 2 (56×56×34) ──PCB-1──→ Block 4 (14×14×89)
Block 3 (28×28×55) ──PCB-2──→ Block 5 (7×7×144)
```

Each PCB performs: `Conv2D → Avg2MaxPool → Conv2D → Avg2MaxPool → Resize → Concatenate`

#### 2. Avg2MaxPooling — Novel Pooling Layer
A custom trainable layer that **explicitly emphasises edge features** in ultrasound imagery:

```python
output = AvgPool(x) − (MaxPool(x) + MaxPool(x))
```

This operation subtracts twice the local maximum from the local average, amplifying boundary and contour responses — particularly effective for delineating hypoechoic nodule margins in B-mode ultrasound.

#### 3. Depthwise Separable Convolutions (Blocks 6 & 7)
The final two blocks employ depthwise separable convolutions (DW → PW → BN → ReLU) to capture high-level semantic features at reduced parameter cost, keeping the model deployable in resource-constrained environments.

#### Complete Block Layout

| Block | Filters | Layer Type | Output Spatial |
|------:|--------:|:-----------|:---------------|
| 1 | 21 | Conv2D + BN + ReLU + MaxPool | 112 × 112 |
| 2 | 34 | Conv2D + BN + ReLU + MaxPool | 56 × 56 |
| 3 | 55 | Conv2D + BN + ReLU + MaxPool | 28 × 28 |
| PCB-1 | 24 | Conv2D + Avg2MaxPool × 2 | 14 × 14 |
| 4 | 89 | Conv2D + BN + ReLU + MaxPool + concat(PCB-1) | 14 × 14 |
| PCB-2 | 24 | Conv2D + Avg2MaxPool × 2 | 7 × 7 |
| 5 | 144 | Conv2D + BN + ReLU + MaxPool + concat(PCB-2) | 7 × 7 |
| 6 | 233 | DepthwiseSeparableConv | 7 × 7 |
| 7 | 377 | DepthwiseSeparableConv | 7 × 7 |
| Head | 1 | GlobalAveragePooling2D + Dense(sigmoid) | — |

**Input:** `224 × 224 × 3` · **Output:** Scalar probability ∈ [0, 1]  
**Threshold:** 0.5 → `{0: Benign, 1: Malignant}`

---

## 🔥 Explainability — Grad-CAM

**Gradient-weighted Class Activation Mapping (Grad-CAM)** is applied over the final `DepthwiseSeparableConv` layer to produce spatial attention heatmaps. These maps:

- Highlight the exact ultrasound regions (nodule boundaries, calcification zones, vascularity patterns) that drove the classification
- Are overlaid on the original scan using a Jet colourmap at α = 0.4 opacity
- Are embedded directly in the DOCX diagnostic report alongside the raw heatmap

The target layer is resolved dynamically at inference time by scanning the model's layer list in reverse, ensuring forward compatibility with model updates:

```python
last_conv = next(
    (layer.name for layer in model.layers[::-1]
     if isinstance(layer, DepthwiseSeparableConv)),
    None
)
```

---

## 🤖 LLM Diagnostic Narrative — LangChain + Groq

The experiment pipeline integrates **LangChain ≥ 1.0** with Groq's hosted inference to generate human-readable clinical commentary:

| Model | Role | Max Tokens |
|:------|:-----|:----------:|
| `llama-3.1-8b-instant` | Per-sample clinical interpretation note | 400 |
| `llama-3.1-70b-versatile` | Full experiment executive summary | 700 |

LangChain components used (new ≥ 1.0 API):

```python
from langchain_groq        import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
```

The pipeline chains a structured prompt template to the LLM and pipes the output into the DOCX report, delivering an AI-authored narrative that contextualises the model's numerical outputs in clinical language. Token budgets are calibrated to remain within Groq's free-tier rate limits across full pipeline runs.

---

## 📁 Project Structure

```
thyroid_detection_xai/
│
├── app.py                              # FastAPI application entry point
├── streamlit_app.py                    # Streamlit analytics dashboard
├── requirements.txt                    # Python dependencies
│
├── backend/
│   └── routes.py                       # FastAPI router: GET /, POST /analyze, POST /report
│
├── frontend/
│   ├── static/
│   │   ├── style.css                   # Medical-themed UI (teal / dark palette)
│   │   └── app.js                      # Drag-and-drop upload, result rendering
│   └── templates/
│       └── index.html                  # Jinja2 template — ThyroCheck AI dashboard
│
├── utils/
│   ├── __init__.py
│   ├── config.py                       # HuggingFace repo & model filename constants
│   ├── model_architecture.py           # FibonacciNet, Avg2MaxPooling, DepthwiseSeparableConv
│   ├── processing.py                   # Image preprocessing pipeline (resize, normalise)
│   ├── gradcam.py                      # make_gradcam_heatmap, save_and_display_gradcam
│   ├── report_generator.py             # DOCX report builder (python-docx)
│   └── logger.py                       # Rotating file + stream logger
│
├── experiments/
│   └── THYROID_NODULE_DETECTION.ipynb  # End-to-end training & evaluation notebook
│
├── test files/
│   ├── 0 non cancer.jpg                # Benign sample for manual testing
│   └── 1 cancer.jpg                    # Malignant sample for manual testing
│
├── logs/
│   └── app.log                         # Runtime application logs
│
├── RESEARCH/
│   ├── Fibonacci Paper.docx            # Architecture research reference
│   ├── Introduction To Medical Imaging.docx
│   └── fibonnaci.pdf                   # Supporting mathematical background
│
└── NOTES/
    ├── NOTES.png                       # Architecture diagrams
    └── Thyroid.excalidraw              # Editable design canvas
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|:------|:-----------|:--------|
| **Deep Learning** | TensorFlow 2.15 / Keras | Model training, custom layers, inference |
| **Model Hosting** | Hugging Face Hub (`Diveshj/thyroid_models`) | Versioned model artefact registry |
| **Web Backend** | FastAPI + Uvicorn | REST API — `/analyze`, `/report` endpoints |
| **Web Frontend** | HTML5, CSS3, Vanilla JS, Jinja2 | Drag-and-drop clinical UI |
| **Dashboard** | Streamlit | Interactive analysis & metrics dashboard |
| **Explainability** | Grad-CAM (custom implementation) | Gradient-weighted attention heatmaps |
| **LLM Orchestration** | LangChain ≥ 1.0 (`langchain-groq`, `langchain-core`) | Prompt chains, LLM abstraction |
| **LLM Inference** | Groq API — LLaMA 3.1 8B / 70B | Low-latency clinical narrative generation |
| **Experiment Tracking** | MLflow 2.13 + DagsHub | Parameter logging, metric streaming, model registry |
| **Result Persistence** | MongoDB Atlas (M0 free tier) | Training run metadata, prediction records |
| **Report Generation** | python-docx | Professional DOCX clinical reports |
| **Image Processing** | OpenCV, Pillow | Preprocessing, heatmap overlay |
| **Dataset** | KaggleHub | Programmatic dataset download |
| **Logging** | Python `logging` | Rotating file + stdout handler |

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.9 or higher
- `pip` ≥ 23.0
- Git

### 1 — Clone the Repository

```bash
git clone https://github.com/d-hackmt/thyroid_detection_xai.git
cd thyroid_detection_xai
```

### 2 — Create and Activate a Virtual Environment

```bash
# Create environment
python -m venv .venv

# Activate — Linux / macOS
source .venv/bin/activate

# Activate — Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

### 3 — Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4 — Configure Environment Variables

Create a `.env` file in the project root (or export the variables in your shell):

```env
# Groq API — https://console.groq.com
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx

# MongoDB Atlas — https://cloud.mongodb.com
MONGO_DB_URL=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/

# DagsHub / MLflow — https://dagshub.com
MLFLOW_TRACKING_URI=https://dagshub.com/<username>/thyroid_detection_xai.mlflow
MLFLOW_TRACKING_USERNAME=<dagshub_username>
MLFLOW_TRACKING_PASSWORD=<dagshub_token>
```

> **Security notice:** Never commit `.env` to version control. Add it to `.gitignore`.

### 5 — Authenticate with Hugging Face (First Run)

The model is hosted publicly at [`Diveshj/thyroid_models`](https://huggingface.co/Diveshj/thyroid_models) and is downloaded automatically on first inference via `hf_hub_download`. For private repositories:

```bash
huggingface-cli login
```

---

## 🚀 Running the Application

### Option A — FastAPI Web Application

```bash
python app.py
```

The server starts on `http://localhost:8000`.

| URL | Description |
|:----|:------------|
| `http://localhost:8000` | ThyroCheck AI clinical dashboard |
| `http://localhost:8000/docs` | Interactive Swagger API documentation |
| `http://localhost:8000/redoc` | ReDoc API reference |

**Workflow:**
1. Open the dashboard in your browser
2. Drag-and-drop or click to upload a thyroid ultrasound image (`.png`, `.jpg`, `.jpeg`)
3. Click **Analyze** — results render within seconds including prediction label, confidence score, and Grad-CAM heatmap
4. Click **Download Report** to receive a formatted DOCX diagnostic report

### Option B — Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Opens automatically at `http://localhost:8501`.

The Streamlit interface provides:
- Side-by-side original vs. Grad-CAM overlay columns
- Live metric cards (prediction label, class ID, confidence score, confidence %)
- One-click DOCX report download

---

## 📡 API Reference

### `GET /`

Returns the ThyroCheck AI HTML dashboard.

---

### `POST /analyze`

Runs full inference (prediction + Grad-CAM) on an uploaded image.

**Request**

```
Content-Type: multipart/form-data
Body: file=<image_file>
```

**Response — `200 OK`**

```json
{
  "label":          "Malignant (Cancerous)",
  "score":          0.9231,
  "percent":        92.31,
  "class_id":       1,
  "is_malignant":   true,
  "original_image": "<base64-encoded PNG>",
  "gradcam_image":  "<base64-encoded PNG>"
}
```

| Field | Type | Description |
|:------|:-----|:------------|
| `label` | `string` | Human-readable classification result |
| `score` | `float` | Raw sigmoid output ∈ [0, 1] |
| `percent` | `float` | Confidence percentage toward predicted class |
| `class_id` | `int` | `0` = Benign, `1` = Malignant |
| `is_malignant` | `bool` | `true` when `score > 0.5` |
| `original_image` | `string` | Base64 PNG of the original uploaded scan |
| `gradcam_image` | `string` | Base64 PNG of the Grad-CAM overlay; `null` if unavailable |

**Error Responses**

| Status | Condition |
|:------:|:----------|
| `503` | Model failed to load from Hugging Face Hub |
| `422` | Invalid or missing `file` field in multipart form |

---

### `POST /report`

Generates and streams a formatted DOCX diagnostic report.

**Request**

```
Content-Type: multipart/form-data
Body: file=<image_file>
```

**Response — `200 OK`**

```
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename="thyroid_analysis_report.docx"
Body: <binary DOCX stream>
```

---

## 🧪 Experiment Pipeline — Notebook

The file `experiments/THYROID_NODULE_DETECTION.ipynb` is the canonical end-to-end training and evaluation notebook. It is structured as a sequential 19-phase pipeline:

| Phase | Description |
|------:|:------------|
| 1 | Dependency installation |
| 2 | Secret loading (GROQ, MongoDB, MLflow/DagsHub, Kaggle) |
| 3 | Global imports, reproducibility seeds, output directory initialisation |
| 4 | GPU detection and memory growth configuration |
| 5 | Dataset download via KaggleHub |
| 6 | Image DataFrame construction (class 0 / class 1 scan) |
| 7 | Exploratory Data Analysis — class distribution, sample grids |
| 8 | Class balancing (minority upsampling), train/val/test split (80/10/10), `ImageDataGenerator` |
| 9 | FibonacciNet instantiation and `model.summary()` |
| 10 | Model compilation + training with MLflow autologging and DagsHub streaming |
| 11 | Training history plots (accuracy + loss curves) |
| 12 | Test-set evaluation — classification report, confusion matrix, ROC curve + AUC |
| 13 | Model serialisation (`thyroid_cancer_model.keras`) |
| 14 | Grad-CAM generation for 4 test samples — original / overlay / raw heatmap grid |
| 15 | MongoDB Atlas persistence — training run metadata + per-sample prediction records |
| 16 | LangChain + Groq LLM — per-sample clinical notes + executive summary |
| 17 | DOCX report assembly with images, prediction table, LLM narrative, and disclaimer |
| 18 | Source `.py` file mirroring into `outputs/src/` |
| 19 | Output archive (`thyroid_xai_outputs.zip`) and download |

**Required Secrets** (add to your environment before running):

| Secret Key | Source |
|:-----------|:-------|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) |
| `MONGO_DB_URL` | [cloud.mongodb.com](https://cloud.mongodb.com) (free M0 cluster) |
| `MLFLOW_TRACKING_URI` | DagsHub project settings |
| `MLFLOW_TRACKING_USERNAME` | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | DagsHub access token |
| `KAGGLE_USERNAME` | [kaggle.com/settings](https://www.kaggle.com/settings) |
| `KAGGLE_KEY` | Kaggle API key |

---

## 📊 MLflow & DagsHub Tracking

All training runs are tracked via **MLflow 2.13** with optional remote logging to **DagsHub**:

```python
USE_DAGSHUB = True   # set False for local mlruns/ directory
```

Automatically captured artefacts per run:

- **Parameters:** `model`, `img_size`, `batch_size`, `learning_rate`, `max_epochs`, `seed`
- **Metrics:** `loss`, `accuracy`, `auc`, `val_loss`, `val_accuracy`, `val_auc` (per epoch)
- **Model artefact:** Full Keras model in MLflow model format
- **Custom metrics:** `roc_auc` (logged post-training)

Access your experiment dashboard at:
```
https://dagshub.com/<your_username>/thyroid_detection_xai.mlflow
```

---

## 🗄️ MongoDB Persistence

Prediction results and training metadata are persisted to a **MongoDB Atlas M0** (free tier) cluster under the database `thyroid_xai`:

### Collection: `training_runs`

```json
{
  "run_id":         "abc123...",
  "model":          "FibonacciNet",
  "epochs_trained": 18,
  "final_val_acc":  0.9412,
  "roc_auc":        0.9781,
  "timestamp":      "2025-09-12T14:23:11.000Z"
}
```

### Collection: `predictions`

```json
{
  "run_id":      "abc123...",
  "sample_idx":  0,
  "true_label":  1,
  "pred_label":  1,
  "confidence":  0.9231
}
```

---

## 📄 Report Generation

The `utils/report_generator.py` module produces professional `.docx` clinical reports containing:

| Section | Content |
|:--------|:--------|
| **Header** | ThyroCheck AI branding with timestamp |
| **1. Executive Summary** | 4-row table: Diagnostic Determination, Probability Coefficient, Confidence Level, Neural Network ID |
| **2. Diagnostic Imaging** | Original ultrasound scan + Grad-CAM attention heatmap |
| **3. AI Clinical Narrative** | LangChain + Groq LLaMA 3.1 generated text |
| **4. Technical Methodology** | FibonacciNet architecture description |
| **Disclaimer** | Clinical non-diagnostic advisory notice |

Reports are streamed as binary DOCX via `StreamingResponse` in the FastAPI route and as `st.download_button` in the Streamlit interface.

---

## 🔧 Configuration

Edit `utils/config.py` to update model registry pointers:

```python
# utils/config.py

REPO_ID        = "Diveshj/thyroid_models"       # HuggingFace repository ID
MODEL_FILENAME = "thyroid_cancer_model.keras"   # Model filename in the repo
```

The model is loaded lazily on the first inference request and cached globally in the FastAPI process (`MODEL` singleton) and via `@st.cache_resource` in Streamlit.

---

## 📦 Dataset

**Thyroid Cancer Classification — Ultrasound Dataset**  
Source: [Kaggle — diveshzz/thyroid-cancer-classification-ultrasound-dataset](https://www.kaggle.com/datasets/diveshzz/thyroid-cancer-classification-ultrasound-dataset)

| Property | Value |
|:---------|:------|
| Modality | B-mode thyroid ultrasound |
| Classes | `0` — Benign (non-cancerous) · `1` — Malignant (cancerous) |
| Input resolution | Resized to 224 × 224 px |
| Normalisation | Pixel values scaled to [0, 1] |
| Class balancing | Minority class upsampled to match majority |
| Split | 80% train · 10% validation · 10% test (stratified) |
| Augmentation | Horizontal flip · rotation ±10° · zoom ±10% (training only) |

---

## 📈 Results & Metrics

> Metrics reflect performance of the trained FibonacciNet on the held-out test split. Individual run results are tracked in MLflow / DagsHub.

| Metric | Value |
|:-------|------:|
| Test Accuracy | — *(see MLflow run)* |
| ROC-AUC | — *(see MLflow run)* |
| Optimiser | Adam (lr = 1e-4) |
| Loss function | Binary Cross-Entropy |
| Callbacks | EarlyStopping (patience=3) · ReduceLROnPlateau (factor=0.5, patience=2) |

Evaluation artefacts saved per run: `confusion_matrix.png` · `roc_curve.png` · `training_history.png`

---

## 📚 Research Foundation

This project is grounded in original research exploring the application of Fibonacci-sequence-based filter progressions in medical image classification. Key references:

- **FibonacciNet — Novel CNN Architecture:** Proprietary research document (see `RESEARCH/Fibonacci Paper.docx`)
- **Introduction to Medical Imaging:** Domain background and ultrasound modality overview (see `RESEARCH/Introduction To Medical Imaging.docx`)
- **Mathematical basis:** Fibonacci sequence in biological and natural growth systems (see `RESEARCH/fibonnaci.pdf`)
- **Grad-CAM:** Selvaraju et al., *"Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization"*, ICCV 2017

---

## 👥 Authors & Acknowledgements

<table>
  <tr>
    <td align="center">
      <strong>Divesh J.</strong><br/>
      <em>Architecture Design · Engineering · Research</em><br/>
      <a href="https://github.com/d-hackmt">GitHub: d-hackmt</a><br/>
      <a href="https://www.linkedin.com/in/dhackmt">LinkedIn: dhackmt</a>
    </td>
    <td align="center">
      <strong>Prof. Nirmal Gaud</strong><br/>
      <em>Research Supervisor · Academic Guidance</em><br/>
      <a href="https://www.linkedin.com/in/nirmal-gaud-210408174/">LinkedIn Profile</a>
    </td>
  </tr>
</table>

**Acknowledgements:**
- [Hugging Face](https://huggingface.co) for model hosting infrastructure
- [Groq](https://groq.com) for low-latency LLaMA inference
- [DagsHub](https://dagshub.com) for MLflow remote tracking
- [MongoDB Atlas](https://www.mongodb.com/atlas) for free-tier cloud persistence
- The medical imaging research community for open ultrasound datasets and Grad-CAM methodology

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full terms.

---

<div align="center">

**ThyroCheck AI** — *Precision. Transparency. Research.*

*Built with ❤️ at the intersection of deep learning and clinical interpretability.*

[![GitHub](https://img.shields.io/badge/Star_on_GitHub-⭐-yellow?style=flat-square&logo=github)](https://github.com/d-hackmt/thyroid_detection_xai)

</div>
