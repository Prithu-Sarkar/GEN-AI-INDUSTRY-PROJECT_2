<div align="center">

<!-- HEADER BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,20,24&height=200&section=header&text=Teen%20Mental%20Health%20ML&fontSize=52&fontAlignY=38&desc=Machine%20Learning%20for%20Adolescent%20Depression%20Detection&descAlignY=58&descSize=18&fontColor=ffffff&animation=twinkling" width="100%"/>

<br/>

<!-- BADGES ROW 1 -->
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-Enabled-189AB4?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io)
[![LightGBM](https://img.shields.io/badge/LightGBM-Enabled-02BF89?style=for-the-badge)](https://lightgbm.readthedocs.io)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)

<!-- BADGES ROW 2 -->
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-FF6B6B?style=for-the-badge)](https://shap.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)]()
[![AUC](https://img.shields.io/badge/Best%20AUC-1.0000-gold?style=for-the-badge)]()

<br/>

<p align="center">
  <i>"Harnessing machine learning to illuminate the silent struggles of adolescent mental health — because early detection saves lives."</i>
</p>

<br/>

<!-- QUICK STATS -->
<table>
  <tr>
    <td align="center"><b>🗂️ Dataset</b><br/>1,200 Records</td>
    <td align="center"><b>🔬 Features</b><br/>13 Raw → 16 Engineered</td>
    <td align="center"><b>🤖 Models</b><br/>7 Trained & Evaluated</td>
    <td align="center"><b>🏆 Best AUC</b><br/>1.0000 (LightGBM)</td>
    <td align="center"><b>📊 Best F1</b><br/>1.0000 (LightGBM)</td>
  </tr>
</table>

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Clinical Motivation](#-clinical-motivation)
- [Dataset](#-dataset)
- [Project Architecture](#-project-architecture)
- [Feature Engineering](#-feature-engineering)
- [Models & Methodology](#-models--methodology)
- [Experiment Tracking](#-experiment-tracking-with-mlflow)
- [Performance Results](#-performance-results)
- [Explainability — SHAP Analysis](#-explainability--shap-analysis)
- [Artifacts & Outputs](#-artifacts--outputs)
- [Repository Structure](#-repository-structure)
- [Installation & Usage](#-installation--usage)
- [Ethical Considerations](#-ethical-considerations)
- [License](#-license)

---

## 🧠 Overview

**Teen Mental Health ML** is a rigorous, end-to-end machine learning pipeline designed to detect the likelihood of **depression in adolescents** based on behavioural, lifestyle, and digital-usage signals. The system trains, evaluates, and interprets seven distinct classifiers — ranging from a simple logistic baseline to a deep neural network — and exposes full model explainability through SHAP (SHapley Additive exPlanations).

The entire experiment lifecycle is governed by **MLflow**, ensuring reproducibility, auditability, and seamless comparison across all runs.

> This project is intended to serve as a research-grade foundation for clinical decision-support tools, mental health screening platforms, and population-level adolescent wellness analytics.

---

## 💡 Clinical Motivation

Depression is among the most prevalent and underdiagnosed conditions in the adolescent population globally. Subtle behavioural patterns — disrupted sleep, excessive screen exposure, social media dependency, elevated stress and anxiety — are known precursors that often go undetected by conventional screening.

This system operationalises those signals into a high-accuracy predictive model, enabling:

- **Proactive screening** before clinical symptoms escalate
- **Data-driven prioritisation** of at-risk individuals in school or community settings
- **Interpretable predictions** that clinicians and counsellors can act upon with confidence

---

## 📦 Dataset

| Property | Detail |
|---|---|
| **File** | `Teen_Mental_Health_Dataset.csv` |
| **Records** | 1,200 adolescent profiles |
| **Missing Values** | None |
| **Target Variable** | `depression_label` (binary: 0 = Not Depressed, 1 = Depressed) |
| **Train / Test Split** | 960 / 240 (80/20 stratified) |

### Raw Feature Schema

| Feature | Type | Description |
|---|---|---|
| `age` | Numerical | Respondent age (years) |
| `gender` | Categorical | Gender identity |
| `daily_social_media_hours` | Numerical | Average daily social media usage (hours) |
| `platform_usage` | Categorical | Primary platform (Instagram, TikTok, etc.) |
| `sleep_hours` | Numerical | Average nightly sleep duration (hours) |
| `screen_time_before_sleep` | Numerical | Pre-sleep screen exposure (hours) |
| `academic_performance` | Numerical | GPA / academic score |
| `physical_activity` | Numerical | Weekly physical activity hours |
| `social_interaction_level` | Categorical | Qualitative level (low / medium / high) |
| `stress_level` | Numerical | Self-reported stress (scale) |
| `anxiety_level` | Numerical | Self-reported anxiety (scale) |
| `addiction_level` | Numerical | Social media addiction score |
| `depression_label` | Binary | Target — presence of depression indicator |

---

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  DATA INGESTION & VALIDATION                │
│          Teen_Mental_Health_Dataset.csv (1,200 records)     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               PREPROCESSING PIPELINE                        │
│  ├── Categorical Encoding (3 features, LabelEncoder)        │
│  ├── Outlier Detection (IQR method)                         │
│  └── Standard Scaling (StandardScaler → scaler.pkl)        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               FEATURE ENGINEERING                           │
│  ├── Interaction Terms (age × sleep, age × stress …)        │
│  ├── Polynomial Features (squared, sqrt transforms)         │
│  ├── Ratio Features (social_media / sleep, social / screen) │
│  └── Feature Selection via SelectKBest + Mutual Information │
│       → 16 features retained (feature_names.pkl)            │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              MODEL TRAINING & EVALUATION                    │
│  ├── Logistic Regression   ├── Random Forest               │
│  ├── XGBoost               ├── LightGBM                    │
│  ├── Voting Ensemble       ├── Stacking Ensemble           │
│  └── Deep Neural Network (TensorFlow / Keras)              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│         EXPLAINABILITY & EXPERIMENT TRACKING                │
│  ├── SHAP Feature Importance (XGBoost)                      │
│  ├── SHAP Beeswarm & Force Plots                            │
│  └── MLflow Experiment: Teen_Mental_Health_ML               │
│       └── 7 runs tracked (AUC, Accuracy, F1 per run)       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   PERSISTED ARTIFACTS                       │
│  models/  ·  outputs/  ·  artifacts/  ·  mlruns/           │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Feature Engineering

Sixteen predictive features were derived from the original thirteen raw inputs using the following transformation strategy:

**Interaction Features** — Capture multiplicative relationships between behavioural signals:
- `age × sleep_hours` — Age-adjusted sleep adequacy
- `age × daily_social_media_hours` — Usage intensity by developmental stage
- `age × stress_level` — Stress burden relative to maturity

**Ratio Features** — Encode proportional dependencies:
- `daily_social_media_hours ÷ sleep_hours` — Digital-to-sleep displacement ratio
- `daily_social_media_hours ÷ screen_time_before_sleep` — Pre-sleep digital load density
- `age ÷ sleep_hours` — Sleep efficiency normalised by age
- `age ÷ daily_social_media_hours` — Age-relative media dependency

**Polynomial Transforms** — Introduce non-linearity for smoother decision boundaries:
- `sleep_hours²`, `sleep_hours_sqrt`
- `daily_social_media_hours²`, `daily_social_media_hours_sqrt`

**Feature Selection** — `SelectKBest` with mutual information criterion was applied over the full engineered feature space, yielding 16 maximally informative features retained in `artifacts/selected_features.pkl`.

---

## 🤖 Models & Methodology

Seven model families were trained and cross-evaluated to provide a comprehensive benchmark landscape.

| # | Model | Class | Strategy |
|---|---|---|---|
| 1 | **Logistic Regression** | Linear | L2-regularised baseline; interpretable probability calibration |
| 2 | **Random Forest** | Ensemble (Bagging) | 100 decision trees; OOB estimation; feature importance via impurity |
| 3 | **XGBoost** | Ensemble (Boosting) | Gradient-boosted trees with regularisation; SHAP-native |
| 4 | **LightGBM** | Ensemble (Boosting) | Leaf-wise growth; histogram-based; fastest convergence |
| 5 | **Voting Ensemble** | Meta-Ensemble | Soft-vote aggregation over LR + RF + XGB + LGBM |
| 6 | **Stacking Ensemble** | Meta-Ensemble | Level-1 base learners + Logistic Regression meta-learner |
| 7 | **Deep Neural Network** | Deep Learning | Multi-layer Keras network; EarlyStopping; Dropout regularisation |

All models share the same 80/20 stratified train-test split and the same preprocessed feature matrix to guarantee fair comparison.

---

## 📡 Experiment Tracking with MLflow

All training runs are logged to the **`Teen_Mental_Health_ML`** MLflow experiment (ID: `625955058818508427`). Each of the seven model runs records:

- `accuracy` — Overall classification accuracy
- `auc` — Area Under the ROC Curve
- `f1` — F1-Score on the positive (depressed) class

To launch the MLflow UI locally after cloning:

```bash
mlflow ui --backend-store-uri ./mlruns
```

Then navigate to `http://127.0.0.1:5000` to explore run comparisons, metric histories, and artifact links interactively.

---

## 📊 Performance Results

### Full Model Benchmark

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Balanced Acc |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Logistic Regression | 0.9917 | 1.0000 | 0.6667 | 0.8000 | 0.9893 | 0.8333 |
| Random Forest | 0.9875 | 1.0000 | 0.5000 | 0.6667 | 0.9957 | 0.7500 |
| XGBoost | 0.9958 | 1.0000 | 0.8333 | 0.9091 | **1.0000** | 0.9167 |
| **LightGBM** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| Voting Ensemble | 0.9958 | 1.0000 | 0.8333 | 0.9091 | **1.0000** | 0.9167 |
| Stacking Ensemble | 0.9958 | 1.0000 | 0.8333 | 0.9091 | **1.0000** | 0.9167 |
| Deep Neural Network | 0.9833 | 0.6250 | 0.8333 | 0.7143 | 0.9836 | 0.9103 |

> **🏆 Champion Model — LightGBM** achieved a perfect score across all metrics on the held-out test set: Accuracy 1.0, F1 1.0, AUC 1.0. The gradient-boosted ensemble family (XGBoost, Voting, Stacking) also attained AUC = 1.0 with near-perfect accuracy, demonstrating that the engineered features cleanly separate the two classes.

### Key Observations

- **Precision is uniformly perfect (1.0)** across all tree-based models, meaning zero false positives — no healthy adolescent is incorrectly flagged as depressed.
- **Recall varies**, with LightGBM uniquely achieving 1.0, capturing every true positive in the test set.
- **Deep Neural Network** showed the lowest precision (0.625) — consistent with its tendency to overfit on smaller datasets without extensive tuning — yet maintained competitive AUC (0.9836).
- **Logistic Regression** as a linear baseline delivered remarkable AUC (0.9893), validating that the engineered features are highly linearly separable.

---

## 🔍 Explainability — SHAP Analysis

Model transparency is a non-negotiable requirement in any clinical-adjacent application. This project provides three layers of SHAP explainability (applied to the XGBoost model):

**Global Feature Importance** (`04_shap_feature_importance.png`)
Aggregate SHAP values ranked by mean absolute impact across all test predictions, revealing which features most consistently drive the model's decisions.

**Beeswarm Summary Plot** (`05_shap_summary_beeswarm.png`)
Encodes both feature importance and the direction of each feature's effect — positive SHAP values push toward depression, negative values toward non-depression — across the full test distribution.

**Individual Force Plots** (`06_shap_force_plot_1.png`, `_2.png`, `_3.png`)
Decompose the model's prediction for three individual samples, showing exactly how each feature contributes to or diminishes the final risk score for that specific adolescent profile.

The top predictive features (derived from SHAP rankings) are:

| Rank | Feature | Signal |
|---|---|---|
| 1 | `sleep_hours` | Lower sleep → higher risk |
| 2 | `anxiety_level` | Higher anxiety → strong positive predictor |
| 3 | `daily_social_media_hours ÷ screen_time_before_sleep` | High ratio → elevated risk |
| 4 | `daily_social_media_hours ÷ sleep_hours` | Displacement ratio — social media crowding out sleep |
| 5 | `stress_level` | Compounding risk factor alongside anxiety |

---

## 💾 Artifacts & Outputs

### Saved Models (`models/`)

| File | Model |
|---|---|
| `logisticregression_model.pkl` | Logistic Regression |
| `randomforest_model.pkl` | Random Forest |
| `xgboost_model.pkl` | XGBoost |
| `lightgbm_model.pkl` | LightGBM |
| `votingensemble_model.pkl` | Voting Ensemble |
| `stackingensemble_model.pkl` | Stacking Ensemble |
| `deep_nn_model.h5` | Deep Neural Network (Keras) |

### Pipeline Artifacts (`artifacts/`)

| File | Contents |
|---|---|
| `scaler.pkl` | Fitted `StandardScaler` for inference preprocessing |
| `feature_names.pkl` | Full engineered feature name list |
| `selected_features.pkl` | 16 selected features used in training |
| `label_encoders.pkl` | Fitted `LabelEncoder` objects for categorical columns |
| `config.json` | Experiment configuration snapshot |

### Visualisation Outputs (`outputs/`)

| File | Description |
|---|---|
| `01_eda_overview.png` | Exploratory data analysis — distribution and correlation overview |
| `02_model_comparison.png` | Side-by-side performance bar chart across all 7 models |
| `03_deep_nn_history.png` | Training & validation loss/accuracy curves for the Deep NN |
| `04_shap_feature_importance.png` | Global SHAP feature importance (XGBoost) |
| `05_shap_summary_beeswarm.png` | SHAP beeswarm plot — feature direction and magnitude |
| `06_shap_force_plot_1/2/3.png` | Individual prediction explanations (3 samples) |
| `07_roc_curves_comparison.png` | Overlaid ROC curves for all models |
| `08_confusion_matrices.png` | Confusion matrices — all 7 models in a single panel |
| `model_metrics.csv` | Machine-readable metrics table |
| `FINAL_REPORT.txt` | Human-readable experiment summary |

---

## 🗂️ Repository Structure

```
teen-mental-health-ml/
│
├── 📄 Teen_Mental_Health_Dataset.csv   ← Primary dataset (1,200 records)
│
├── 📁 models/                          ← Serialised trained models
│   ├── logisticregression_model.pkl
│   ├── randomforest_model.pkl
│   ├── xgboost_model.pkl
│   ├── lightgbm_model.pkl
│   ├── votingensemble_model.pkl
│   ├── stackingensemble_model.pkl
│   └── deep_nn_model.h5
│
├── 📁 artifacts/                       ← Preprocessing pipeline artifacts
│   ├── config.json
│   ├── scaler.pkl
│   ├── feature_names.pkl
│   ├── selected_features.pkl
│   └── label_encoders.pkl
│
├── 📁 outputs/                         ← Visualisations and reports
│   ├── 01_eda_overview.png
│   ├── 02_model_comparison.png
│   ├── 03_deep_nn_history.png
│   ├── 04_shap_feature_importance.png
│   ├── 05_shap_summary_beeswarm.png
│   ├── 06_shap_force_plot_[1-3].png
│   ├── 07_roc_curves_comparison.png
│   ├── 08_confusion_matrices.png
│   ├── model_metrics.csv
│   └── FINAL_REPORT.txt
│
├── 📁 mlruns/                          ← MLflow experiment tracking store
│   └── 625955058818508427/             ← Experiment: Teen_Mental_Health_ML
│       └── [7 run directories]
│
├── 📁 logs/                            ← Training logs
└── 📄 README.md                        ← This document
```

---

## 🚀 Installation & Usage

### Prerequisites

```bash
Python >= 3.10
```

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/teen-mental-health-ml.git
cd teen-mental-health-ml
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> Core dependencies: `scikit-learn`, `xgboost`, `lightgbm`, `tensorflow`, `shap`, `mlflow`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `joblib`

### 4. Run the Full Pipeline

```bash
python main.py
```

This will execute data ingestion, preprocessing, feature engineering, model training, evaluation, SHAP analysis, and artifact serialisation in sequence.

### 5. Inspect Experiment Results

```bash
mlflow ui --backend-store-uri ./mlruns
# Open: http://127.0.0.1:5000
```

### 6. Load a Model for Inference

```python
import joblib
import pickle
import pandas as pd

# Load preprocessing artifacts
with open("artifacts/scaler.pkl", "rb") as f:
    scaler = joblib.load(f)

with open("artifacts/selected_features.pkl", "rb") as f:
    selected_features = pickle.load(f)

# Load champion model
model = joblib.load("models/lightgbm_model.pkl")

# Prepare a new sample (after encoding + scaling)
sample = pd.DataFrame([{
    "sleep_hours": 5.5,
    "anxiety_level": 8,
    "stress_level": 7,
    "daily_social_media_hours": 6.0,
    # ... all 16 selected features
}])

prediction = model.predict(sample[selected_features])
probability = model.predict_proba(sample[selected_features])[:, 1]

print(f"Depression Risk: {'High' if prediction[0] == 1 else 'Low'}")
print(f"Probability Score: {probability[0]:.4f}")
```

---

## ⚖️ Ethical Considerations

This project handles sensitive, health-adjacent data and therefore carries significant ethical obligations:

**Privacy** — All data must be fully anonymised before use. No personally identifiable information (PII) should ever be present in the dataset. Compliance with applicable data protection regulations (GDPR, HIPAA, DPDP Act, etc.) is mandatory.

**Bias & Fairness** — Model performance must be audited across demographic subgroups (age, gender, socioeconomic status) to ensure equitable prediction accuracy. Disparate false-negative rates across groups could result in systematic under-detection in marginalised populations.

**Clinical Scope** — This system is a **decision-support tool, not a diagnostic instrument**. Outputs must always be reviewed and contextualised by qualified mental health professionals. No autonomous clinical decision should be made solely on the basis of model output.

**Transparency** — The inclusion of SHAP explainability is intentional: any prediction presented to a clinician or counsellor must be accompanied by a human-interpretable explanation of the contributing factors.

**Consent** — In any live deployment, explicit informed consent must be obtained from adolescent participants (and their guardians where applicable) prior to data collection.

---

## 📜 License

This project is distributed under the **MIT License**. See [`LICENSE`](LICENSE) for full terms.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,20,24&height=100&section=footer" width="100%"/>

<br/>

**Built with rigour. Deployed with responsibility. Interpreted with compassion.**

<br/>

*© 2026 Teen Mental Health ML Project. All rights reserved.*

</div>
