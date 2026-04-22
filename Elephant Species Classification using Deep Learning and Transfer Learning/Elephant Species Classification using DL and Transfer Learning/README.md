# 🐘 Elephant Species Classification
### Deep Learning & Transfer Learning · TensorFlow · MLflow · MongoDB

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=flat-square&logo=tensorflow)
![MLflow](https://img.shields.io/badge/MLflow-DagsHub-blue?style=flat-square&logo=mlflow)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?style=flat-square&logo=mongodb)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

Binary image classification of **African** vs **Asian** elephants using a full end-to-end deep learning pipeline — from raw data ingestion through baseline CNN, transfer learning, hyperparameter optimisation, model comparison, and experiment tracking.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Project Structure](#-project-structure)
- [Pipeline Phases](#-pipeline-phases)
- [Models](#-models)
- [Tech Stack](#-tech-stack)
- [Setup & Usage](#-setup--usage)
- [Experiment Tracking](#-experiment-tracking)
- [Outputs](#-outputs)
- [Results](#-results)
- [Deployment](#-deployment)

---

## 🔍 Overview

| | |
|---|---|
| **Task** | Binary image classification |
| **Classes** | African Elephant · Asian Elephant |
| **Framework** | TensorFlow / Keras |
| **Environment** | Google Colab (GPU — T4) |
| **Tracking** | MLflow + DagsHub · MongoDB Atlas |
| **Deployment** | Streamlit (MobileNetV2 backend) |

The project demonstrates a production-style ML workflow: reproducible data pipelines, multiple model architectures, automated hyperparameter search, dual experiment logging (MLflow + MongoDB), and a packaged Streamlit inference app.

---

## 📁 Project Structure

```
elephant-classification/
│
├── Elephant_Classification_Final.ipynb   # Main pipeline notebook (Colab)
├── app.py                                # Streamlit inference app
├── class_indices.json                    # Class label mapping
├── Deployment.txt                        # Deployment instructions
└── README.md
```

**Generated at runtime** (inside `/content/outputs/` → zipped):

```
outputs/
├── models/
│   ├── baseline_cnn_best.h5
│   ├── mobilenetv2_best.h5
│   ├── best_mobilenetv2.weights.h5        # used by Streamlit app
│   ├── best_mobilenetv2_hpo.weights.h5
│   ├── best_xception.weights.h5
│   └── class_indices.json
├── plots/
│   ├── 01_augmented_samples.png
│   ├── 02_cnn_history.png
│   ├── 03_mob_frozen_history.png
│   ├── 04_mob_ft_history.png
│   ├── 05_xception_history.png
│   ├── 06_model_comparison.png
│   └── 07_sample_predictions.png
└── reports/
    ├── cnn_report.txt
    ├── mobilenetv2_report.txt
    ├── hpo_report.txt
    ├── xception_report.txt
    └── experiment_summary.json
```

---

## 🔄 Pipeline Phases

| # | Phase | Description |
|---|-------|-------------|
| 0 | **Setup & Secrets** | Install dependencies; load all credentials from Colab Secrets |
| 1 | **Imports & GPU** | Library imports, GPU memory growth config |
| 2 | **Data Ingestion** | Extract dataset ZIPs, auto-detect `train/` and `test/` paths, create output dirs |
| 3 | **Augmentation** | `ImageDataGenerator` with rotation, zoom, flip, shift, shear; visualise sample batch |
| 4 | **Baseline CNN** | Custom 4-block Conv→BN→Pool architecture with EarlyStopping + ReduceLROnPlateau |
| 5 | **MobileNetV2** | Frozen-base training → fine-tune top 30 layers at lower LR |
| 6 | **HPO** | KerasTuner `RandomSearch` over dense units, dropout rate, learning rate (10 trials) |
| 7 | **Xception** | 299×299 pipeline with native `preprocess_input` and GlobalMaxPooling |
| 8 | **Comparison** | Side-by-side accuracy/loss bar chart; best model identified; summary JSON saved |
| 9 | **Inference Demo** | Visual grid of test predictions with true vs. predicted labels |
| 10 | **Artifact ZIP** | All models, plots, and reports packaged into `elephant_clf_outputs.zip` |

---

## 🧠 Models

### Baseline CNN
A custom sequential network built from scratch as a performance baseline.

- 4 convolutional blocks: `Conv2D → BatchNorm → MaxPool`
- Filter progression: 32 → 64 → 128 → 256
- Dense head: 256 → 128 → 2 (softmax)
- Dropout: 0.5 and 0.3

### MobileNetV2 (Transfer Learning)
Pre-trained on ImageNet; fine-tuned for binary elephant classification.

- Base frozen for initial 20 epochs (`lr = 1e-4`)
- Top 30 layers unfrozen for fine-tuning (`lr = 1e-5`)
- Custom head: `GlobalAveragePooling2D → Dense(256) → Dropout(0.4) → Dense(2)`

### MobileNetV2 + KerasTuner HPO
Same architecture with automated hyperparameter search.

| Hyperparameter | Search Range |
|---|---|
| `dense_units` | 128 – 512 (step 64) |
| `dropout_rate` | 0.2 – 0.6 (step 0.1) |
| `learning_rate` | 1e-5 – 1e-3 (log scale) |

Strategy: `RandomSearch`, 10 trials, `EarlyStopping(patience=4)`

### Xception (Transfer Learning)
Deeper architecture for comparison; requires 299×299 input.

- Native `xception_preprocess` function applied
- Head: `GlobalMaxPooling2D → Dense(256) → Dropout(0.4) → Dense(2)`
- Frozen base, 20 epochs (`lr = 1e-4`)

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Deep Learning | TensorFlow 2.x / Keras |
| HPO | KerasTuner |
| Experiment Tracking | MLflow + DagsHub |
| Metadata Store | MongoDB Atlas |
| Visualisation | Matplotlib, Seaborn |
| Evaluation | Scikit-learn (classification report, ROC-AUC) |
| Deployment | Streamlit |
| Environment | Google Colab (T4 GPU) |

---

## 🚀 Setup & Usage

### 1. Prerequisites

Add the following keys to **Colab Secrets** (`🔑` icon in the left panel):

| Secret Key | Description |
|---|---|
| `MONGO_DB_URL` | MongoDB Atlas connection string |
| `MLFLOW_TRACKING_URI` | DagsHub MLflow tracking URI |
| `MLFLOW_TRACKING_USERNAME` | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | DagsHub access token |

### 2. Upload Dataset

Upload both ZIPs directly to `/content/` in Colab:

```
train-20260105T160050Z-1-001.zip
test-20260105T160050Z-1-001.zip
```

Expected structure inside each ZIP:

```
train/
├── African/
│   ├── img001.jpg
│   └── ...
└── Asian/
    ├── img001.jpg
    └── ...
```

### 3. Run the Notebook

Open `Elephant_Classification_Final.ipynb` in Google Colab and select **Runtime → Run all**.

The notebook will:
1. Extract ZIPs and detect paths automatically
2. Train all four models sequentially
3. Log every experiment to MLflow and MongoDB
4. Save all outputs and download `elephant_clf_outputs.zip`

---

## 📊 Experiment Tracking

### MLflow / DagsHub

Each model run logs:
- **Per-epoch metrics**: `train_accuracy`, `val_accuracy`, `train_loss`, `val_loss`
- **Final metrics**: `accuracy`, `loss`
- **Artifacts**: all plots and classification reports
- **Parameters**: architecture name, epochs, optimizer, learning rate, batch size

```python
mlflow.set_experiment("Elephant-Species-Classification")
# Runs: Baseline_CNN | MobileNetV2_FineTuned | MobileNetV2_HPO | Xception_Transfer
```

### MongoDB

Each run inserts one document into `elephant_clf.experiments`:

```json
{
  "run_name": "MobileNetV2_FineTuned",
  "timestamp": "2026-01-05T16:00:00",
  "params": { "model": "MobileNetV2", "epochs": 20, "lr_ft": 0.00001 },
  "metrics": { "accuracy": 0.9412, "loss": 0.1873 },
  "notes": ""
}
```

---

## 📦 Outputs

All artifacts are saved to `/content/outputs/` during the run and packaged into a single ZIP for download:

```bash
/content/elephant_clf_outputs.zip
```

Contents include model weights (`.h5`), training curve plots, confusion matrices, ROC curves, per-class classification reports, and a consolidated `experiment_summary.json`.

---

## 📈 Results

> Metrics are populated after running the notebook on your dataset.

| Model | Test Accuracy | Test Loss |
|-------|:---:|:---:|
| Baseline CNN | — | — |
| MobileNetV2 (fine-tuned) | — | — |
| MobileNetV2 + HPO | — | — |
| Xception | — | — |

The best-performing model's weights are saved as `best_mobilenetv2.weights.h5` and used directly by the Streamlit deployment app.

---

## 🌐 Deployment

The project ships with a **Streamlit** app (`app.py`) that loads the best MobileNetV2 weights and serves real-time predictions.

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py

# Run persistently on a server
nohup python3 -m streamlit run app.py &
```

**Required files alongside `app.py`:**
- `best_mobilenetv2.weights.h5` — trained weights (from outputs ZIP)
- `class_indices.json` — label mapping (`{"African": 0, "Asian": 1}`)

Upload an elephant image via the browser interface to receive a predicted species and confidence score.

---

## 📄 License

This project is released under the [MIT License](LICENSE).
