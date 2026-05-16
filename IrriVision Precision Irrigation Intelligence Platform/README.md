
<div align="center">

<!-- ═══════════════════════════════ HERO BANNER ═══════════════════════════════ -->

```
██╗██████╗ ██████╗ ██╗██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗
██║██╔══██╗██╔══██╗██║██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║
██║██████╔╝██████╔╝██║██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║
██║██╔══██╗██╔══██╗██║╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║
██║██║  ██║██║  ██║██║ ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║
╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
```

# IrriVision — Precision Irrigation Intelligence Platform

**Production-grade machine learning pipeline for three-class irrigation need classification**  
*Kaggle Playground Series · Season 6 · Episode 4*

---

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-FF6600?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![MLflow](https://img.shields.io/badge/MLflow-2.12%2B-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org/)
[![Optuna](https://img.shields.io/badge/Optuna-3.5%2B-5B5EA6?style=for-the-badge)](https://optuna.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-27AE60?style=for-the-badge)](LICENSE)
[![Balanced Accuracy](https://img.shields.io/badge/OOF%20Balanced%20Accuracy-0.98004-brightgreen?style=for-the-badge)](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.balanced_accuracy_score.html)

---

</div>

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Dataset](#-dataset)
- [Pipeline Architecture](#-pipeline-architecture)
- [Feature Engineering](#️-feature-engineering)
- [Modelling Strategy](#-modelling-strategy)
- [Results](#-results)
- [Project Structure](#-project-structure)
- [MLOps Integration](#-mlops-integration)
- [Quickstart](#-quickstart)
- [Configuration Reference](#️-configuration-reference)
- [Visualisations](#-visualisations)
- [Deliverables](#-deliverables)
- [Technical Stack](#-technical-stack)
- [Author](#-author)

---

## 🌾 Overview

**IrriVision** is an end-to-end, production-engineered machine learning pipeline that classifies agricultural field irrigation requirements into three tiers — **Low**, **Medium**, and **High** — using a rich set of soil, climate, crop, and regional features.

The pipeline is architected around enterprise-grade principles: modular phase-wise execution, reproducible configuration management, schema-validated data ingestion, MLflow experiment tracking, MongoDB metadata persistence, and fully packaged deliverables. Every design decision prioritises interpretability, robustness, and minority-class recall — the defining challenge of this problem.

> **Core insight:** A domain-driven composite feature (`physical_score`) — encoding soil moisture, rainfall, temperature, wind, mulching, and growth stage — accounts for **~45% of total model importance** and was the single highest-leverage engineering decision in the pipeline.

---

## 🎯 Problem Statement

| Attribute | Detail |
|-----------|--------|
| **Task** | Multi-class tabular classification (3 classes) |
| **Evaluation Metric** | Balanced Accuracy |
| **Primary Challenge** | Severe class imbalance — `High` class ≈ 3.7% of training data |
| **Competition** | Kaggle Playground Series S6E4 |
| **Dataset Type** | Synthetically generated from a real agricultural domain |

The evaluation metric — **Balanced Accuracy** — weights all three classes equally, regardless of frequency. This makes the rare `High` class the most consequential class to predict correctly, demanding targeted imbalance correction strategies beyond standard loss functions.

---

## 📊 Dataset

### Files

| File | Rows | Columns | Description |
|------|------|---------|-------------|
| `train.csv` | 630,000 | 21 | Features + target label |
| `test.csv` | 270,000 | 20 | Features only (no label) |
| `submission.csv` | 270,000 | 2 | Final predictions |

### Feature Schema

**Numerical Features (11)**

| Feature | Range | Domain Significance |
|---------|-------|---------------------|
| `Soil_pH` | 5.0 – 8.0 | Soil acidity — affects nutrient availability |
| `Soil_Moisture` | 0 – 70% | Water content — primary irrigation signal |
| `Organic_Carbon` | 0.5 – 1.5 | Fertility indicator — influences water retention |
| `Electrical_Conductivity` | 0 – 3.5 | Salinity / nutrient proxy |
| `Temperature_C` | 10 – 45°C | Evapotranspiration driver |
| `Humidity` | 20 – 100% | Ambient moisture — offsets irrigation need |
| `Rainfall_mm` | 0 – 3000mm | Natural water supply — strongest single predictor |
| `Sunlight_Hours` | 4 – 12 hrs | Solar energy → crop water demand |
| `Wind_Speed_kmh` | 0 – 20 km/h | Evaporative stress factor |
| `Field_Area_hectare` | 0 – 15 ha | Field scale |
| `Previous_Irrigation_mm` | 0 – 150mm | Historical irrigation context |

**Categorical Features (8)**

| Feature | Cardinality | Values |
|---------|------------|--------|
| `Crop_Type` | 6 | Cotton, Maize, Potato, Rice, Sugarcane, Wheat |
| `Region` | 5 | Central, East, North, South, West |
| `Soil_Type` | 4 | Clay, Loamy, Sandy, Silt |
| `Crop_Growth_Stage` | 4 | Flowering, Harvest, Sowing, Vegetative |
| `Irrigation_Type` | 4 | Canal, Drip, Rainfed, Sprinkler |
| `Water_Source` | 4 | Groundwater, Rainwater, Reservoir, River |
| `Season` | 3 | Kharif, Rabi, Zaid |
| `Mulching_Used` | 2 | Yes, No |

**Target Variable**

| Class | Train Frequency | Share |
|-------|----------------|-------|
| Low | ~359,100 | ~57.0% |
| Medium | ~247,800 | ~39.3% |
| **High** | **~23,100** | **~3.7%** ⚠️ |

---

## 🏗️ Pipeline Architecture

The pipeline is structured as **11 discrete, sequentially executed phases**, each with explicit input/output contracts and audit logging.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        IrriVision Pipeline                                  │
├──────┬──────────────────────────────────┬────────────────────────────────────┤
│Phase │ Name                             │ Key Outputs                        │
├──────┼──────────────────────────────────┼────────────────────────────────────┤
│  0   │ Environment & Secrets            │ CFG dict, folder scaffold, logger  │
│  1   │ Data Ingestion & Schema          │ Validated DataFrames (5 contracts) │
│  2   │ Exploratory Data Analysis        │ 5 executive PNGs → reports/        │
│  3   │ Feature Engineering              │ +28 engineered features            │
│  4   │ Preprocessing                    │ Label-encoded matrices             │
│  5   │ XGBoost Round 1 (5-Fold CV)      │ OOF proba, test proba, BA=0.97219  │
│  6   │ Pseudo-Label Generation + R2     │ Augmented dataset, BA=0.97xxx      │
│  7   │ Weighted Blend + Bias Tuning     │ best_bias.json, BA=0.98004         │
│  8   │ MLflow Logging                   │ Tracked run, artefacts             │
│  9   │ MongoDB Integration              │ Upserted metadata document         │
│  10  │ Submission & ZIP Packaging       │ submission.csv, deliverables.zip   │
└──────┴──────────────────────────────────┴────────────────────────────────────┘
```

### Data Flow Diagram

```
train.csv ──────────────┐
                        ├─► Schema Validation ─► Feature Engineering ─► Label Encoding
test.csv ───────────────┘                                                      │
                                                                               ▼
                                                              ┌─────────────────────────┐
                                                              │  5-Fold StratifiedKFold │
                                                              │  TargetEncoder (in-fold)│
                                                              │  XGBoost + SampleWeight │
                                                              └────────────┬────────────┘
                                                                           │
                                               ┌───────────────────────────┘
                                               ▼
                              OOF Proba (Round 1) + Test Proba (Round 1)
                                               │
                                               ▼
                              Pseudo-Label Generation (conf ≥ 0.98)
                                               │
                                               ▼
                          XGBoost Round 2 (train + pseudo-labelled test)
                                               │
                              ┌────────────────┘
                              ▼
                   Optuna Blend Weight Optimisation (50 trials)
                              │
                              ▼
                   Optuna Bias Tuning (300 trials, log-space)
                              │
                   ┌──────────┴──────────┐
                   ▼                     ▼
           submission.csv          MLflow + MongoDB
```

---

## ⚙️ Feature Engineering

All transformations are encapsulated in the stateless `build_features()` function and applied **identically** to both train and test sets — eliminating any risk of target leakage.

### Feature Groups

| Group | Features Created | Design Rationale |
|-------|-----------------|-----------------|
| **Physical Score** | `physical_score` (1) | Composite domain signal: high temperature, low moisture, low rainfall → urgency; harvest/sowing stage, mulching → low need. Accounts for ~45% of model importance. |
| **Adaptive Rounding** | `{col}_rounded` (11) | Synthetic datasets embed distributional signals in decimal values. Range-adaptive rounding (1–3 dp) exposes them without domain assumptions. |
| **Forensic Flags** | `canyon_low_rain`, `canyon_high_rain`, `q3_rain_breach_flag` (3) | Boundary thresholds at which class distributions exhibit sharp discontinuities, identified during EDA. |
| **Interaction Terms** | `mulch_shield_interaction`, `temp_humidity_ratio`, `rain_moisture_ratio` (3) | Physics-grounded cross-features: evapotranspiration proxy, mulch × moisture shielding, rainfall normalised by moisture. |
| **Decimal Digits** | `temp_decimal`, `humidity_decimal` (2) | Synthetic generation artefacts — class information encoded in the first decimal digit of measurements. |
| **Rainfall Bin** | `rainfall_bin` (1) | Ordinal discretisation into 5 bands aligned with forensic thresholds. |
| **Group Aggregates** | `{Crop_Type/Region}_mean_{rain/moisture}` (4) | Within-group environmental context that individual records do not capture. |

**Total: 19 original → 47 engineered features (+28)**

---

## 🧪 Modelling Strategy

### XGBoost with In-Fold Target Encoding

The core model is **XGBoost** trained with `StratifiedKFold` (5 folds). `TargetEncoder` is fitted **inside each fold** on the training split only — the correct protocol that prevents validation leakage. `compute_sample_weight("balanced")` is applied at training time to correct for the 3.7% minority class.

### Pseudo-Labelling

Test samples where the Round 1 model predicts with **≥ 0.98 confidence** are assigned pseudo-labels and merged with the original training data. A second 5-fold training run (Round 2) on this augmented dataset provides complementary probability estimates with additional signal for the `High` class.

### Weighted Ensemble

Optuna (TPE sampler, 50 trials) finds the optimal scalar weight `w` to blend Round 1 and Round 2 OOF probabilities:

```
combined_proba = w · P_round1 + (1 − w) · P_round2
```

### Optuna Bias Tuning

The blended probabilities undergo post-hoc log-space bias correction via a 3-dimensional Optuna study (300 trials):

```
final_class = argmax( log(P_combined + ε) + [b_Low, b_Medium, b_High] )
```

Positive `b_High` biases predictions toward the minority class without retraining — the most compute-efficient mechanism for correcting residual class imbalance at inference time.

---

## 📈 Results

| Pipeline Stage | OOF Balanced Accuracy | Δ vs Baseline |
|---------------|----------------------|---------------|
| XGBoost Round 1 | 0.97219 | — |
| XGBoost Round 2 (Pseudo-Labels) | ~0.973xx | +0.001xx |
| Weighted Blend (R1 + R2) | ~0.975xx | +0.003xx |
| **Blend + Bias Tuning (Final)** | **0.98004** | **+0.00785** |

### Submission Distribution

| Class | Predicted Count | Share |
|-------|----------------|-------|
| Low | 159,944 | 59.2% |
| Medium | 100,807 | 37.3% |
| High | 9,249 | 3.4% |

> The final bias-tuned model correctly allocates the `High` class at a rate consistent with its true prevalence — a direct result of the Optuna bias correction stage.

---

## 📁 Project Structure

```
irrivision/
│
├── 📓 ps6e4_production_pipeline.ipynb   ← Main pipeline notebook (43 cells, 11 phases)
│
├── 📂 outputs/
│   └── submission.csv                   ← Final Kaggle submission (270,000 rows)
│
├── 📂 reports/
│   ├── eda_class_imbalance.png          ← Target distribution bar chart
│   ├── eda_numerical_distributions.png  ← KDE per feature, class-stratified
│   ├── eda_categorical_class_split.png  ← Stacked bars per categorical
│   ├── eda_correlation_heatmap.png      ← Pearson correlation matrix
│   ├── feature_eng_spearman_correlation.png  ← New feature vs target ρ
│   └── model_r1_feature_importance.png  ← Top-25 XGBoost gain importances
│
├── 📂 artifacts/
│   └── best_bias.json                   ← Optimal bias vector + blend weights
│
├── 📂 logs/
│   └── pipeline_audit.log               ← Full execution audit trail
│
├── 📂 models/                           ← Serialised model artefacts (per run)
│
└── 📄 README.md                         ← This document
```

---

## 🔭 MLOps Integration

### MLflow Experiment Tracking

Every pipeline execution logs a fully reproducible MLflow run containing:

| Category | Logged Items |
|----------|-------------|
| **Parameters** | All XGBoost hyperparameters, seed, fold count, pseudo threshold, blend weights |
| **Metrics** | OOF BA per stage, bias vector components, pseudo-label rate, lift |
| **Artefacts** | All report PNGs, bias JSON, audit log |
| **Run Name** | Timestamped (`xgb-ps6e4-YYYYMMDD-HHMMSS`) for unambiguous identification |

MLflow backend is **switchable** via secret configuration:

```
DAGSHUB_TOKEN + DAGSHUB_REPO  →  DagsHub remote tracking
MLFLOW_TRACKING_URI           →  Custom remote server
(neither set)                 →  Local ./mlruns  [default]
```

Inspect runs locally:
```bash
mlflow ui --port 5000
```

### MongoDB Metadata Persistence

Each run upserts a structured document into `mlops_tracking.ps6e4_runs` keyed by `mlflow_run_id`, enabling downstream dashboarding, model registry queries, and cross-run comparison outside the MLflow UI.

```json
{
  "mlflow_run_id"     : "abc123...",
  "experiment"        : "ps6e4-irrigation-xgb",
  "timestamp_utc"     : "2026-05-15T16:33:19",
  "oof_ba_round1"     : 0.97219,
  "oof_ba_bias_tuned" : 0.98004,
  "bias_vector"       : [-0.12, 0.08, 1.43],
  "blend_weight_r1"   : 0.42,
  "pseudo_count"      : 248500,
  "mlflow_backend"    : "dagshub"
}
```

---

## 🚀 Quickstart

### Prerequisites

```bash
python >= 3.10
```

### Install Dependencies

```bash
pip install xgboost>=2.0 optuna>=3.5 mlflow>=2.12 pymongo>=4.6 \
            dagshub scikit-learn pandas numpy matplotlib seaborn
```

### Configure Secrets

Set the following environment variables (or inject via your preferred secrets manager):

```bash
# Required for data access — update to your local path
export DATA_DIR="/path/to/playground-series-s6e4"

# Optional — MLflow remote tracking
export DAGSHUB_TOKEN="your_dagshub_pat"
export DAGSHUB_REPO="username/irrivision"

# Optional — MongoDB persistence
export MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net"
```

### Run the Pipeline

Open `ps6e4_production_pipeline.ipynb` and execute all cells sequentially (top to bottom). The pipeline is self-contained and handles all directory creation, encoding, training, optimisation, and packaging automatically.

The notebook runs on:
- **Kaggle** (with GPU, recommended — `tree_method=hist, device=cuda`)
- **Any local Python environment** with CUDA or CPU-only (`device` falls back automatically)

---

## ⚙️ Configuration Reference

All pipeline parameters are centralised in the `CFG` dictionary (Phase 0, Cell 0.6). No magic numbers are scattered through the codebase.

| Key | Default | Description |
|-----|---------|-------------|
| `SEED` | `42` | Global random seed for all stochastic components |
| `N_FOLDS` | `5` | Number of stratified cross-validation folds |
| `THRESHOLD_PSEUDO` | `0.98` | Minimum confidence for pseudo-label acceptance |
| `OPTUNA_BIAS_TRIALS` | `300` | Bias tuning Optuna trials |
| `OPTUNA_BLEND_TRIALS` | `50` | Blend weight Optuna trials |
| `XGB_PARAMS.n_estimators` | `800` | XGBoost tree count |
| `XGB_PARAMS.max_depth` | `6` | Maximum tree depth |
| `XGB_PARAMS.learning_rate` | `0.05` | Shrinkage factor |
| `XGB_PARAMS.early_stopping_rounds` | `50` | Early stopping patience |
| `MLFLOW_EXPERIMENT` | `ps6e4-irrigation-xgb` | MLflow experiment namespace |
| `MONGO_COLLECTION` | `ps6e4_runs` | MongoDB target collection |

---

## 📉 Visualisations

All visualisations are generated automatically during pipeline execution and saved to `reports/`.

| Report | Description |
|--------|-------------|
| `eda_class_imbalance.png` | Target distribution bar chart with count + percentage annotations |
| `eda_numerical_distributions.png` | Per-feature KDE curves stratified by irrigation class |
| `eda_correlation_heatmap.png` | Lower-triangular Pearson correlation matrix for all numerical features |
| `eda_categorical_class_split.png` | Stacked bar charts showing class composition per categorical level |
| `feature_eng_spearman_correlation.png` | Spearman ρ of engineered features vs numeric target proxy |
| `model_r1_feature_importance.png` | Top-25 XGBoost feature importances (gain) — `physical_score` highlighted |

---

## 📦 Deliverables

| File | Contents |
|------|----------|
| `ps6e4_production_pipeline.ipynb` | Full pipeline notebook — 43 cells, 11 phases, ~1,400 lines |
| `outputs/submission.csv` | 270,000-row Kaggle submission |
| `artifacts/best_bias.json` | Serialised optimal bias vector and blend weights for inference reuse |
| `reports/*.png` | 6 executive visualisation artefacts |
| `logs/pipeline_audit.log` | Complete execution audit trail with timestamps |
| `ps6e4_deliverables_*.zip` | Self-contained archive of all the above |

---

## 🛠️ Technical Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.10+ |
| **Core ML** | XGBoost 2.0, scikit-learn |
| **Optimisation** | Optuna 3.5 (TPE sampler) |
| **Experiment Tracking** | MLflow 2.12, DagsHub |
| **Database** | MongoDB Atlas (pymongo 4.6) |
| **Data** | pandas, NumPy |
| **Visualisation** | Matplotlib, Seaborn |
| **Encoding** | scikit-learn `LabelEncoder`, `TargetEncoder` |
| **Imbalance Handling** | `compute_sample_weight("balanced")`, Optuna bias tuning |
| **Packaging** | Python `zipfile`, `pathlib` |

---

## 👤 Author

<div align="center">

**Built as a portfolio-quality, production-grade ML project**  
*Demonstrating end-to-end MLOps discipline, domain-driven feature engineering,*  
*and rigorous minority-class optimisation on large-scale tabular data.*

---

> *"Thoughtful feature engineering beats adding more models."*

---

[![Kaggle](https://img.shields.io/badge/Kaggle-Playground%20Series%20S6E4-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/playground-series-s6e4)

</div>

---

<div align="center">
<sub>IrriVision · Precision Irrigation Intelligence Platform · MIT License</sub>
</div>
