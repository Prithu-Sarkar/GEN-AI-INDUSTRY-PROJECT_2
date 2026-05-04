<div align="center">

<img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/TensorFlow-2.12%2B-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"/>
<img src="https://img.shields.io/badge/MLflow-Tracked-0194E2?style=for-the-badge&logo=mlflow&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-App%20Ready-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge"/>

# ☀️ Solar Panel Defect Classification

**A production-grade deep learning pipeline for automated detection and classification of solar panel surface defects using computer vision.**

*End-to-end training · Transfer learning · Hyperparameter tuning · MLflow tracking · MongoDB logging · Streamlit inference app*

</div>

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Dataset](#dataset)
- [Pipeline Architecture](#pipeline-architecture)
- [Models](#models)
- [Project Structure](#project-structure)
- [Quickstart](#quickstart)
- [Configuration](#configuration)
- [Experiment Tracking](#experiment-tracking)
- [Inference App](#inference-app)
- [Results](#results)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Solar energy infrastructure requires continuous inspection to maintain optimal output efficiency. Manual inspection is costly, inconsistent, and difficult to scale across large photovoltaic farms. This project presents a fully automated defect classification system trained on real-world solar panel imagery, capable of distinguishing between six surface conditions with high accuracy.

The pipeline progresses from a simple CNN baseline through regularised architectures and into state-of-the-art transfer learning models, with full hyperparameter optimisation and experiment logging — suitable for direct integration into industrial monitoring workflows.

---

## Problem Statement

Surface defects and contamination on photovoltaic panels directly reduce energy output. Identifying defect type is critical for dispatching the correct maintenance response:

| Class | Description |
|---|---|
| `Bird-drop` | Localised organic soiling from bird droppings |
| `Clean` | No defect — panel operating at full efficiency |
| `Dusty` | Diffuse dust accumulation reducing light transmission |
| `Electrical-damage` | Cell-level electrical fault (hot spots, micro-cracks) |
| `Physical-damage` | Mechanical damage to glass or frame |
| `Snow-Covered` | Snow occlusion requiring thermal or manual clearing |

---

## Dataset

The dataset consists of labelled RGB images of solar panels organised in a class-per-folder structure.

```
dataset/
├── Bird-drop/
├── Clean/
├── Dusty/
├── Electrical-damage/
├── Physical-damage/
└── Snow-Covered/
```

**Preparation:**
1. Download or assemble your dataset in the above structure.
2. Compress it as a single `.zip` file.
3. Upload the zip to your Google Drive.
4. Set `ZIP_PATH` in **Phase 2** of the notebook to the Drive path.

> The pipeline automatically handles class imbalance via inverse-frequency class weights computed at load time.

---

## Pipeline Architecture

The notebook is structured as a 13-phase, end-to-end ML pipeline:

```
Phase 0  →  Install dependencies
Phase 1  →  Environment & secrets setup (MLflow / DagsHub / MongoDB)
Phase 2  →  Dataset mount & extraction (Google Drive)
Phase 3  →  Data loading, preprocessing, pipeline validation
Phase 3b →  Exploratory data analysis (class distribution, sample grid)
Phase 4  →  Baseline CNN (reference model)
Phase 5  →  Improved CNN (BatchNorm + Dropout + Augmentation)
Phase 6  →  Transfer learning — MobileNetV2
Phase 7  →  Transfer learning — EfficientNetB0
Phase 8  →  Hyperparameter tuning (Keras Tuner — Random Search)
Phase 9  →  Final model training with full MLflow logging
Phase 10 →  Evaluation (confusion matrix, classification report, MongoDB log)
Phase 11 →  Streamlit inference app generation
Phase 12 →  Final model packaging & zip download
Phase 13 →  Cross-model comparison summary
```

---

## Models

Four architectures are trained and compared:

### Baseline CNN
A lightweight 3-block convolutional network used as a performance reference. Establishes the lower bound for accuracy on this dataset.

### Improved CNN
Addresses overfitting in the baseline with dual Conv layers per block, BatchNormalisation, spatial Dropout, data augmentation (flip, rotation, zoom), and L2 weight regularisation on Dense layers. Trained with `EarlyStopping` and `ReduceLROnPlateau`.

### MobileNetV2 (Transfer Learning)
ImageNet-pretrained MobileNetV2 backbone (frozen) with a custom classification head. Lightweight and suitable for edge deployment. Input preprocessing aligned to MobileNetV2's expected `[-1, 1]` range via `mobilenet_preprocess_input`.

### EfficientNetB0 (Transfer Learning + Tuning)
ImageNet-pretrained EfficientNetB0 backbone (frozen) with a configurable head. Preprocessing handled via `effnet_preprocess_input`. Subjected to Keras Tuner Random Search (20 trials) over:

| Hyperparameter | Search Range |
|---|---|
| `rotation_factor` | 0.05 – 0.30 |
| `zoom_factor` | 0.05 – 0.30 |
| `dropout_rate` | 0.0 – 0.50 |
| `dense_units` | 64 – 512 |
| `learning_rate` | 1e-4 – 1e-2 (log scale) |

The best configuration is then retrained for up to 30 epochs with early stopping and logged as the **final model**.

---

## Project Structure

```
solar_panel_project/
├── dataset/                     # Extracted class-per-folder image data
├── outputs/
│   ├── models/
│   │   ├── mobilenetv2.h5
│   │   ├── efficientnetb0_base.h5
│   │   └── trained_effnet_finetune.h5   ← final production model
│   ├── plots/
│   │   ├── class_distribution.png
│   │   ├── sample_images.png
│   │   ├── baseline_cnn_history.png
│   │   ├── improved_cnn_history.png
│   │   ├── mobilenetv2_history.png
│   │   ├── efficientnet_history.png
│   │   ├── final_model_history.png
│   │   └── confusion_matrix.png
│   ├── class_names.json
│   ├── best_hyperparameters.json
│   ├── eval_metrics.json
│   ├── baseline_history.pkl
│   └── improved_cnn_history.pkl
└── app/
    ├── app.py                   ← Streamlit inference application
    ├── trained_effnet_finetune.h5
    ├── class_names.json
    └── requirements.txt
```

---

## Quickstart

### Prerequisites

- Google Colab (GPU runtime — T4 or A100 recommended)
- Google Drive with dataset zip uploaded
- DagsHub account (optional, for remote MLflow tracking)
- MongoDB Atlas URI (optional, for experiment logging)

### Running the Notebook

**1. Open in Colab**

Upload `Solar_Panel_Defect_Classification_Fixed.ipynb` to Google Colab and switch the runtime to GPU:

```
Runtime → Change runtime type → T4 GPU
```

**2. Configure Colab Secrets**

Navigate to the 🔑 Secrets panel and add the following keys:

| Secret Key | Description |
|---|---|
| `MONGO_DB_URL` | MongoDB Atlas connection string |
| `MLFLOW_TRACKING_URI` | DagsHub MLflow endpoint |
| `MLFLOW_TRACKING_USERNAME` | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | DagsHub access token |

> If you prefer local MLflow logging (no DagsHub), set `USE_DAGSHUB = False` in Phase 1. MongoDB logging gracefully degrades if the URI is not set.

**3. Upload Dataset to Google Drive**

Place your dataset zip at a known Drive path, then update Phase 2:

```python
ZIP_PATH = "/content/drive/MyDrive/solar_dataset.zip"   # update this
```

**4. Run All Cells**

Execute all cells top-to-bottom (`Runtime → Run all`). The pipeline will:
- Mount Drive and extract the dataset
- Run a pipeline sanity check before any training begins
- Train all four model architectures
- Run hyperparameter search
- Log the final model to MLflow
- Generate evaluation plots and a confusion matrix
- Package and download all outputs as a single zip

---

## Configuration

All global hyperparameters and paths are centralised in Phase 1 — no hard-coded values exist elsewhere in the notebook.

```python
# Image / training params
IMG_HEIGHT  = 224
IMG_WIDTH   = 224
BATCH_SIZE  = 32
SEED        = 42
VAL_SPLIT   = 0.2

# MLflow experiment name
EXPERIMENT_NAME = "solar_panel_defect_classification"
```

---

## Experiment Tracking

All training runs are tracked with **MLflow**, logging:

- All hyperparameters (model config, image size, batch size, val split)
- Per-epoch train/validation accuracy and loss
- Best validation accuracy as a summary scalar
- The final `.h5` model file as a registered artifact

When `USE_DAGSHUB = True`, all runs are pushed to your DagsHub repository's MLflow server, enabling cross-run comparison, metric visualisation, and model registry from any browser.

When `USE_DAGSHUB = False`, runs are stored locally at `/content/mlruns` and viewable via:

```bash
mlflow ui --backend-store-uri /content/mlruns
```

### MongoDB Logging

After evaluation, a summary record is inserted into:

```
solar_panel_classification.experiments
```

Each document captures timestamp, model name, class names, best hyperparameters, overall accuracy, and number of validation samples — providing a persistent audit trail independent of MLflow.

---

## Inference App

A ready-to-deploy **Streamlit** inference application is generated at `app/app.py` during Phase 11.

**Features:**
- Upload any solar panel image (JPG / PNG)
- Displays the top prediction with confidence percentage
- Shows top-3 ranked predictions
- Expandable full probability table for all 6 classes
- Clean/Defect decision with contextual status message

**Local deployment:**

```bash
cd solar_panel_project/app
pip install -r requirements.txt
streamlit run app.py
```

**Requirements:**

```
tensorflow>=2.12
streamlit>=1.28
numpy
Pillow
```

---

## Results

Model comparison across all phases (representative results — actual values depend on dataset):

| Model | Val Accuracy | Notes |
|---|---|---|
| Baseline CNN | ~72% | Reference only |
| Improved CNN | ~85% | BatchNorm + Dropout + Augmentation |
| MobileNetV2 | ~89% | Frozen ImageNet backbone |
| EfficientNetB0 (base) | ~91% | Frozen ImageNet backbone |
| **EfficientNetB0 (tuned)** | **~94%** | **Best HP config — production model** |

> Actual results will vary depending on dataset size, class balance, and Colab GPU allocation.

---

## Tech Stack

| Component | Technology |
|---|---|
| Deep learning framework | TensorFlow / Keras 2.12+ |
| Transfer learning backbones | MobileNetV2, EfficientNetB0 (ImageNet) |
| Hyperparameter tuning | Keras Tuner (Random Search) |
| Experiment tracking | MLflow + DagsHub |
| Database logging | MongoDB Atlas (pymongo) |
| Inference app | Streamlit |
| Training environment | Google Colab (GPU) |
| Dataset I/O | Google Drive |

---

## Contributing

Contributions are welcome. To propose changes:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/fine-tuning`)
3. Commit your changes with clear messages
4. Open a pull request with a description of the improvement

Areas open for contribution include fine-tuning the frozen backbones, adding ONNX export support, expanding to additional defect classes, or building a FastAPI serving layer around the final model.

---

## License

This project is licensed under the **MIT License**. See `LICENSE` for details.

---

<div align="center">

Built for production-grade solar infrastructure monitoring · Powered by TensorFlow & MLflow

</div>
