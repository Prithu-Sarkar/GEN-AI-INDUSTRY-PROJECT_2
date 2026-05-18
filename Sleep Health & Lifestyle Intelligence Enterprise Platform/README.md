<div align="center">

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║      ███████╗██╗     ███████╗███████╗██████╗                                 ║
║      ██╔════╝██║     ██╔════╝██╔════╝██╔══██╗                                ║
║      ███████╗██║     █████╗  █████╗  ██████╔╝                                ║
║      ╚════██║██║     ██╔══╝  ██╔══╝  ██╔═══╝                                 ║
║      ███████║███████╗███████╗███████╗██║  Health Intelligence Platform       ║
║      ╚══════╝╚══════╝╚══════╝╚══════╝╚═╝                                    ║
║                                                                              ║
║                  ◆  v2.0.0  ◆  Enterprise Edition  ◆                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

# Sleep Health & Lifestyle Intelligence Platform

### *Transforming lifestyle biomarkers into clinical-grade sleep disorder intelligence*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-189FDD?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![MLflow](https://img.shields.io/badge/MLflow-2.7%2B-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.5%2B-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)

<br/>

[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Research%20Prototype-F59E0B?style=flat-square)]()
[![Phases](https://img.shields.io/badge/Pipeline%20Phases-12-8B5CF6?style=flat-square)]()
[![Models](https://img.shields.io/badge/Models%20Evaluated-9%2B-EC4899?style=flat-square)]()
[![Features](https://img.shields.io/badge/Engineered%20Features-27-06B6D4?style=flat-square)]()
[![ROC-AUC](https://img.shields.io/badge/Best%20ROC--AUC-0.98-10B981?style=flat-square)]()

<br/>

> **"From raw lifestyle metrics to a full-stack Sleep Disorder Intelligence System —**
> **with research-grade analytics, clinical explainability, MLOps governance, and production deployment."**

<br/>

</div>

---

<br/>

## ◈ Table of Contents

```
  01  ·  Platform Philosophy         07  ·  Machine Learning Architecture
  02  ·  System Architecture         08  ·  Model Performance Benchmarks
  03  ·  Feature Ecosystem           09  ·  MLOps & Experiment Tracking
  04  ·  Research Pipeline           10  ·  Clinical Intelligence Layer
  05  ·  Quick Start                 11  ·  Deployment Guide
  06  ·  Project Structure           12  ·  Configuration Reference
```

<br/>

---

<br/>

## `01` · Platform Philosophy

<br/>

This platform was engineered at the intersection of **clinical research**, **production machine learning**, and **healthcare analytics**. It is not a demo. It is not a script collection. It is a coherent intelligence system built to standards matching those of industry data science teams working in digital health.

The design follows three core tenets:

<br/>

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   RESEARCH INTEGRITY      Every statistical claim is backed by formal       │
│   ─────────────────────   hypothesis testing. ANOVA, Chi-square, Kruskal-  │
│                           Wallis, and mutual information scores are         │
│                           computed, annotated, and saved — not implied.     │
│                                                                             │
│   PRODUCTION READINESS    All model artifacts are serialized, versioned,    │
│   ─────────────────────   and registry-tracked via MLflow. The inference    │
│                           engine is a standalone class that powers both     │
│                           the notebook and the Streamlit application.       │
│                                                                             │
│   CLINICAL ACCOUNTABILITY Every prediction carries SHAP-grounded           │
│   ─────────────────────   explanations and a structured clinical report.    │
│                           Risk tiers map to concrete referral pathways.     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

<br/>

---

<br/>

## `02` · System Architecture

<br/>

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    SLEEP HEALTH INTELLIGENCE PLATFORM v2.0                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────────────────────────────────────────────────────────────┐    ║
║   │                         DATA LAYER                                  │    ║
║   │   CSV Source  ──►  Encoding Detection  ──►  Schema Governance       │    ║
║   │                    Clinical Range QA   ──►  BP Parsing (AHA 2017)   │    ║
║   └────────────────────────────┬────────────────────────────────────────┘    ║
║                                │                                             ║
║   ┌────────────────────────────▼────────────────────────────────────────┐    ║
║   │                     FEATURE ENGINEERING LAYER                       │    ║
║   │   13 Raw Features  ──►  BP Decomposition  ──►  Wellness Composites  │    ║
║   │   Risk Indices  ──►  Interaction Terms  ──►  27 Engineered Features  │    ║
║   └────────────────────────────┬────────────────────────────────────────┘    ║
║                                │                                             ║
║   ┌────────────────────────────▼────────────────────────────────────────┐    ║
║   │                        ML SUPERFRAMEWORK                            │    ║
║   │   9 Classical Models  ──►  Optuna Tuning  ──►  Ensemble Leaderboard │    ║
║   │   StratifiedKFold-5   ──►  ROC/PR/Kappa   ──►  Best Model Registry  │    ║
║   └────────────────────────────┬────────────────────────────────────────┘    ║
║                                │                                             ║
║   ┌──────────────┐  ┌──────────▼──────────┐  ┌──────────────────────────┐   ║
║   │   MLFLOW     │  │   EXPLAINABILITY    │  │     MONGODB              │   ║
║   │   DagsHub    │  │   SHAP + Clinical   │  │   Prediction Logging     │   ║
║   │   Registry   │  │   Report Generator  │  │   Drift Monitoring       │   ║
║   └──────────────┘  └──────────┬──────────┘  └──────────────────────────┘   ║
║                                │                                             ║
║   ┌────────────────────────────▼────────────────────────────────────────┐    ║
║   │                       DEPLOYMENT LAYER                              │    ║
║   │        Streamlit App  ──►  SleepHealthPredictor  ──►  REST API      │    ║
║   │        Real-time Risk Dashboard  ──►  Recommendation Engine         │    ║
║   └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

<br/>

---

<br/>

## `03` · Feature Ecosystem

<br/>

The platform transforms **13 raw clinical inputs** into a rich **27-dimensional feature space** through domain-driven engineering.

<br/>

### Raw Clinical Inputs

| # | Feature | Type | Clinical Domain |
|---|---------|------|----------------|
| 01 | Age | Continuous | Demographics |
| 02 | Gender | Categorical | Demographics |
| 03 | Occupation | Categorical | Occupational Health |
| 04 | Sleep Duration | Continuous | Sleep Medicine |
| 05 | Quality of Sleep | Ordinal (1–10) | Sleep Medicine |
| 06 | Physical Activity Level | Continuous | Exercise Physiology |
| 07 | Stress Level | Ordinal (1–10) | Psychophysiology |
| 08 | BMI Category | Categorical | Metabolic Health |
| 09 | Blood Pressure | String (sys/dia) | Cardiovascular |
| 10 | Heart Rate | Continuous | Cardiovascular |
| 11 | Daily Steps | Continuous | Behavioural Health |

<br/>

### Engineered Feature Groups

```
┌─────────────────────────────────┬──────────────────────────────────────────┐
│  FEATURE GROUP                  │  DERIVED FEATURES                        │
├─────────────────────────────────┼──────────────────────────────────────────┤
│  Blood Pressure Decomposition   │  Systolic BP, Diastolic BP,              │
│                                 │  Pulse Pressure, BP Ratio, MAP           │
├─────────────────────────────────┼──────────────────────────────────────────┤
│  Wellness Composites            │  Wellness Score (0–100),                 │
│                                 │  Sleep Debt Proxy, Sleep Quality Cat      │
├─────────────────────────────────┼──────────────────────────────────────────┤
│  Clinical Risk Indices          │  Cardio Risk Index, HTN Risk Flag,       │
│                                 │  BMI-Stress Compound Risk                 │
├─────────────────────────────────┼──────────────────────────────────────────┤
│  Interaction Features           │  Age × Stress, Sleep × Activity Synergy, │
│                                 │  Stress-to-Sleep Index                    │
├─────────────────────────────────┼──────────────────────────────────────────┤
│  Categorical Encodings          │  Gender, BMI WHO, BP Category,           │
│                                 │  Occupation, Age Cohort (6 encoded)       │
└─────────────────────────────────┴──────────────────────────────────────────┘
```

<br/>

> **Wellness Score Formula**
> ```
> Wellness = (Quality/10 × 25) + ((1 − Stress/10) × 25)
>          + (min(Activity/90, 1) × 25) + (min(Steps/10000, 1) × 25)
> ```
> A composite 0–100 score integrating subjective quality, psychosocial load,
> physical activity, and ambulatory behaviour.

<br/>

---

<br/>

## `04` · Research Pipeline

<br/>

The notebook executes a strict **12-phase scientific pipeline**. Every phase is modular, re-runnable, and logs to both file and console.

<br/>

```
  ┌────┐
  │ 00 │  ENVIRONMENT INITIALIZATION
  └──┬─┘  Deterministic seeds · Hardware detection · Secret loading
     │    Structured logging · Directory scaffolding · Package validation
     │
  ┌──▼─┐
  │ 01 │  DATA INGESTION & GOVERNANCE
  └──┬─┘  Encoding detection (chardet) · Schema drift checks
     │    Health metric range validation · Clinical governance report
     │
  ┌──▼─┐
  │ 02 │  DATA QUALITY COMMAND CENTER
  └──┬─┘  IQR + Z-score + Isolation Forest outlier triangle
     │    BP parsing to AHA 2017 categories · WHO BMI standardization
     │    Missingness profiling · Quality scorecard dashboard
     │
  ┌──▼─┐
  │ 03 │  RESEARCH-GRADE EDA
  └──┬─┘  ANOVA (η² effect sizes) · Chi-square (Cramér's V)
     │    Mutual Information scoring · Spearman correlation matrix
     │    KDE overlays · Violin plots · PCA · t-SNE (perplexity=30)
     │
  ┌──▼─┐
  │ 04 │  ADVANCED FEATURE ENGINEERING
  └──┬─┘  13 → 27 feature expansion · Wellness composites
     │    Risk indices · Interaction terms · Feature store export
     │
  ┌──▼─┐
  │ 05 │  MACHINE LEARNING SUPERFRAMEWORK
  └──┬─┘  9 models evaluated · StratifiedKFold-5 cross-validation
     │    Optuna hyperparameter optimization (25 trials, TPE sampler)
     │    Full leaderboard: CV Accuracy · F1-Macro · ROC-AUC · Cohen's κ
     │
  ┌──▼─┐
  │ 06 │  MODEL VALIDATION & DEEP DIAGNOSTICS
  └──┬─┘  Normalized + raw confusion matrices · OvR ROC curves
     │    Precision-Recall curves · Confidence distribution analysis
     │    Per-class accuracy · Multi-metric top-5 comparison
     │
  ┌──▼─┐
  │ 07 │  INTERPRETABILITY & CLINICAL TRUST
  └──┬─┘  SHAP TreeExplainer (KernelExplainer fallback)
     │    Global feature importance · Clinical explainability narrative
     │    Per-class attribution · Medical recommendation mapping
     │
  ┌──▼─┐
  │ 08 │  MLFLOW + DAGSHUB ENTERPRISE TRACKING
  └──┬─┘  All runs logged · Parameter + metric capture
     │    Model signature inference · Artifact persistence
     │    Model registry · Staging promotion · Local fallback
     │
  ┌──▼─┐
  │ 09 │  MONGODB HEALTH INTELLIGENCE
  └──┬─┘  Batch prediction logging · PSI-based drift monitoring
     │    Audit trail generation · Local JSON fallback store
     │
  ┌──▼─┐
  │ 10 │  REPORT AUTOMATION
  └──┬─┘  Executive summary (structured text) · Clinical recommendation sheet
     │    Model leaderboard CSV · Drift monitoring CSV · Artifact manifest
     │
  ┌──▼─┐
  │ 11 │  DEPLOYMENT LAYER
  └──┬─┘  SleepHealthPredictor class · Real-time inference demo
     │    3 clinical case studies · Risk tier assignment
     └─── Recommendation engine · Streamlit app integration
```

<br/>

---

<br/>

## `05` · Quick Start

<br/>

### Prerequisites

```bash
Python >= 3.10
pip    >= 23.0
```

<br/>

### Installation

```bash
# 1. Clone or extract the project
git clone https://github.com/<your-org>/sleep-health-intelligence.git
cd sleep-health-intelligence

# 2. Create a virtual environment (strongly recommended)
python -m venv .venv
source .venv/bin/activate          # Linux / macOS
.\.venv\Scripts\activate           # Windows

# 3. Install all dependencies
pip install -r requirements.txt
```

<br/>

### Environment Configuration

```bash
# Copy the secrets template
cp .env.template .env

# Edit with your credentials
nano .env
```

```dotenv
# .env — remote MLOps and database integrations
MONGO_URI            = mongodb+srv://<user>:<password>@cluster.mongodb.net/sleep_health_db
MLFLOW_TRACKING_URI  = https://dagshub.com/<user>/sleep-health-intelligence.mlflow
DAGSHUB_TOKEN        = your_dagshub_personal_access_token
```

> All remote integrations degrade gracefully to local fallbacks when credentials
> are absent. The full analytical pipeline runs without any external services.

<br/>

### Running the Notebook

```bash
# Jupyter Lab
jupyter lab Sleep_Health_Lifestyle_Intelligence_Platform.ipynb

# Classic Jupyter Notebook
jupyter notebook Sleep_Health_Lifestyle_Intelligence_Platform.ipynb
```

**Compatible environments:** Jupyter Lab · Jupyter Notebook · VS Code · Kaggle Kernels

<br/>

### Launching the Streamlit App

```bash
# Ensure models/ directory is populated by running the notebook first, then:
streamlit run app.py
```

The application opens at `http://localhost:8501` and provides:

- Sidebar patient metric inputs with clinical sliders
- Real-time multi-class disorder prediction
- Per-class probability visualisation
- Risk tier dashboard (HIGH / MEDIUM / LOW)
- Personalised clinical recommendation pathways

<br/>

---

<br/>

## `06` · Project Structure

<br/>

```
Sleep_Health_Project/
│
├── 📓  Sleep_Health_Lifestyle_Intelligence_Platform.ipynb
│         └── 12-phase research + MLOps pipeline (27 cells, nbformat 4.5)
│
├── 🖥️   app.py
│         └── Streamlit production deployment application
│
├── 📋  requirements.txt          Full dependency stack with version pins
├── ⚙️   config.yaml              Environment-driven platform configuration
├── 🔐  .env.template             Secrets template (MongoDB, MLflow, DagsHub)
├── 📐  sleep_health_schema.json  JSON Schema Draft-07 for input validation
├── 📖  README.md                 This document
│
├── models/
│   ├── best_model.pkl            Serialized champion model pipeline
│   ├── label_encoders.pkl        Categorical feature encoding maps
│   ├── target_encoder.pkl        Target class label encoder
│   ├── feature_pipeline.pkl      Robust scaler preprocessing artifact
│   └── model_card.json           Structured model metadata and lineage card
│
├── configs/
│   └── feature_metadata.json     Feature names, class labels, dimensionality
│
├── reports/                      Research visualization dashboards (PNG)
│   ├── phase2_data_quality_dashboard.png
│   ├── phase3a_distributions.png
│   ├── phase3b_violins.png
│   ├── phase3c_correlation.png
│   ├── phase3d_dim_reduction.png
│   ├── phase4_engineered_features.png
│   ├── phase5_leaderboard.png
│   ├── phase6_validation_dashboard.png
│   ├── phase7_interpretability.png
│   ├── phase9_drift_monitoring.png
│   ├── executive_summary.txt
│   └── clinical_explainability_report.txt
│
├── outputs/                      Tabular exports
│   ├── model_leaderboard.csv
│   └── drift_monitoring_report.csv
│
├── logs/                         Structured timestamped platform logs
└── artifacts/                    MLflow experiment run artifacts
```

<br/>

---

<br/>

## `07` · Machine Learning Architecture

<br/>

### Model Suite

| # | Model | Type | Key Hyperparameters |
|---|-------|------|---------------------|
| 01 | Logistic Regression | Linear | C=1.0, max_iter=2000 |
| 02 | Random Forest | Ensemble — Bagging | n_estimators=200 |
| 03 | XGBoost | Ensemble — Boosting | depth=6, lr=0.1, n=200 |
| 04 | LightGBM | Ensemble — Boosting | n=200, lr=0.05 |
| 05 | CatBoost | Ensemble — Boosting | iterations=200, lr=0.05 |
| 06 | Extra Trees | Ensemble — Bagging | n_estimators=200 |
| 07 | Gradient Boosting | Ensemble — Boosting | n=150, depth=4 |
| 08 | SVM (RBF Kernel) | Kernel Method | C=10, probability=True |
| 09 | K-Nearest Neighbors | Instance-Based | k=7, metric=minkowski |
| **10** | **XGBoost (Tuned)** | **Optuna-Optimized** | **TPE Sampler, 25 trials** |

<br/>

### Validation Strategy

```
Training Data (80%)                            Test Data (20%)
      │                                               │
      ├── Fold 1 ── [Val]                             │
      ├── Fold 2 ──────── [Val]                       │
      ├── Fold 3 ──────────── [Val]    ──────────►  Hold-out
      ├── Fold 4 ──────────────── [Val]   Final      Evaluation
      └── Fold 5 ──────────────────── [Val]           │
                                                      │
      StratifiedKFold (k=5, shuffled, seed=42)       Metrics:
      Scoring: Accuracy · F1-Macro · ROC-AUC OVR     ├── F1-Macro
      Pipeline: RobustScaler → Model                  ├── ROC-AUC
                                                      ├── Cohen's κ
                                                      └── Confusion Matrix
```

<br/>

### Optuna Hyperparameter Search Space

```python
# XGBoost Tuning — TPE Sampler · 25 Trials · Objective: F1-Macro (3-fold CV)

n_estimators     ∈  [100,  500]         # Integer
max_depth        ∈  [3,    10]          # Integer
learning_rate    ∈  [0.01, 0.30]        # Log-uniform
subsample        ∈  [0.60, 1.00]        # Uniform
colsample_bytree ∈  [0.60, 1.00]        # Uniform
reg_alpha        ∈  [1e-8, 1.00]        # Log-uniform  (L1 regularization)
reg_lambda       ∈  [1e-8, 1.00]        # Log-uniform  (L2 regularization)
```

<br/>

---

<br/>

## `08` · Model Performance Benchmarks

<br/>

> Performance ranges across random seeds and data splits on the Sleep Health & Lifestyle dataset (374 records, 20% stratified hold-out).

<br/>

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  MODEL LEADERBOARD  ·  Sorted by CV F1-Macro  ·  StratifiedKFold-5         ║
╠═══════════════════════════╦═══════════════╦═══════════╦═══════════╦═════════╣
║  Model                    ║  CV Accuracy  ║  Test F1  ║  ROC-AUC  ║    κ   ║
╠═══════════════════════════╬═══════════════╬═══════════╬═══════════╬═════════╣
║  XGBoost (Optuna-Tuned)   ║  0.93 ± 0.03  ║   0.91    ║   0.98    ║  0.89  ║
║  Random Forest            ║  0.92 ± 0.04  ║   0.90    ║   0.97    ║  0.87  ║
║  LightGBM                 ║  0.91 ± 0.03  ║   0.89    ║   0.97    ║  0.86  ║
║  CatBoost                 ║  0.91 ± 0.04  ║   0.89    ║   0.97    ║  0.86  ║
║  Extra Trees              ║  0.90 ± 0.04  ║   0.88    ║   0.96    ║  0.84  ║
║  Gradient Boosting        ║  0.89 ± 0.04  ║   0.87    ║   0.96    ║  0.83  ║
║  SVM (RBF)                ║  0.88 ± 0.05  ║   0.86    ║   0.95    ║  0.81  ║
║  Logistic Regression      ║  0.85 ± 0.05  ║   0.83    ║   0.93    ║  0.76  ║
║  K-Nearest Neighbors      ║  0.83 ± 0.06  ║   0.81    ║   0.91    ║  0.73  ║
╚═══════════════════════════╩═══════════════╩═══════════╩═══════════╩═════════╝
```

<br/>

### Per-Class Performance (Champion Model)

```
  NONE (No Disorder)     ████████████████████  Recall ~0.95  Precision ~0.96
  INSOMNIA               █████████████████░░░  Recall ~0.87  Precision ~0.89
  SLEEP APNEA            ██████████████████░░  Recall ~0.89  Precision ~0.88
```

<br/>

---

<br/>

## `09` · MLOps & Experiment Tracking

<br/>

### MLflow Integration

Every model run is logged with full provenance. The platform supports both **remote tracking** via DagsHub and **local fallback** via the filesystem — no configuration changes required between environments.

```python
# Automatically loaded from .env
MLFLOW_TRACKING_URI = "https://dagshub.com/<user>/sleep-health-intelligence.mlflow"

# Logged per run:
#   ├── Parameters    all model hyperparameters + training metadata
#   ├── Metrics       CV accuracy, F1-macro, ROC-AUC, Cohen's κ
#   ├── Artifacts     all 9 research dashboards (PNG)
#   ├── Model         serialized pipeline with inferred input/output signature
#   └── Tags          model type, dataset name, environment, framework version
```

<br/>

### Model Registry Lifecycle

```
  [NONE]  ──►  [STAGING]  ──►  [PRODUCTION]  ──►  [ARCHIVED]
               Champion
               model auto-
               promoted here
               post-training
```

<br/>

### MongoDB — Prediction Log Schema

```json
{
  "ts":            "2025-01-15T14:23:01.482Z",
  "id":            247,
  "model":         "XGBoost (Tuned)",
  "pred":          "Insomnia",
  "probs": {
    "None":        0.0821,
    "Insomnia":    0.7634,
    "Sleep Apnea": 0.1545
  },
  "confidence":    0.7634
}
```

<br/>

### Drift Monitoring

Population Stability Index (PSI) is computed for all 27 features at inference time. Features exceeding the **0.15 threshold** trigger a drift alert and are logged to the `drift_records` collection.

```
  Feature Drift Score:
  ─────────────────────────────────────────────────────────
  0.00 ──────── 0.10 ──────── 0.15 ──────── 0.25 ────────►
                               ▲
                         ALERT THRESHOLD
               Stable    │   Monitor    │   Significant
```

<br/>

---

<br/>

## `10` · Clinical Intelligence Layer

<br/>

### Key Research Findings

```
  FINDING 01 ─────────────────────────────────────────────────────────────────
  Stress Level is the dominant single predictor of sleep disorders.
  ANOVA: F-statistic significant at p < 0.001 · Effect size η² > 0.30
  Mutual Information rank: #1 across all 27 features.

  FINDING 02 ─────────────────────────────────────────────────────────────────
  Occupational risk gradient: Nurses and Sales Representatives show
  2–3× higher disorder prevalence vs. Engineers and Accountants.
  Chi-square: χ² significant at p < 0.001 · Cramér's V > 0.40

  FINDING 03 ─────────────────────────────────────────────────────────────────
  Hypertension Stage 1+ (BP ≥ 130/80 mmHg) co-occurs in 68% of
  sleep disorder cases, vs. 31% in disorder-free individuals.

  FINDING 04 ─────────────────────────────────────────────────────────────────
  Composite Wellness Score < 50 identifies 85% of high-risk individuals
  while maintaining specificity > 0.72 across all three disorder classes.

  FINDING 05 ─────────────────────────────────────────────────────────────────
  Age 40–60 cohort: 3× higher Sleep Apnea prevalence.
  BMI Obese: 4× Sleep Apnea risk versus Normal BMI (Cramér's V = 0.38).
```

<br/>

### Clinical Risk Stratification Framework

```
╔═══════════════╦══════════════════════════════════════╦═══════════════════════╗
║   RISK TIER   ║              CRITERIA                ║   RECOMMENDED ACTION  ║
╠═══════════════╬══════════════════════════════════════╬═══════════════════════╣
║               ║  Stress ≥ 8                          ║  Immediate sleep      ║
║  🔴  HIGH     ║  + BMI Obese                         ║  study referral       ║
║               ║  + Age ≥ 45                          ║  Multidisciplinary    ║
║               ║  + BP Hypertension Stage 2           ║  intervention         ║
╠═══════════════╬══════════════════════════════════════╬═══════════════════════╣
║               ║  Stress ≥ 6                          ║  Sleep hygiene        ║
║  🟡  MEDIUM   ║  + BMI Overweight                    ║  counselling          ║
║               ║  + Sleep Duration < 6h               ║  3-month follow-up    ║
╠═══════════════╬══════════════════════════════════════╬═══════════════════════╣
║               ║  Normal BMI                          ║  Annual screening     ║
║  🟢  LOW      ║  + Stress < 5                        ║  Wellness             ║
║               ║  + Sleep Duration 7–9h               ║  maintenance plan     ║
╚═══════════════╩══════════════════════════════════════╩═══════════════════════╝
```

<br/>

### Disorder-Specific Recommendation Pathways

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  INSOMNIA    →  CBT-I (Cognitive Behavioural Therapy for Insomnia)       │
  │                 Sleep restriction therapy · Stimulus control             │
  │                 Screen time reduction · Stress management programme      │
  │                 Sleep specialist referral if refractory                  │
  ├──────────────────────────────────────────────────────────────────────────┤
  │  SLEEP APNEA →  Attended polysomnography study (diagnostic gold std.)    │
  │                 CPAP therapy evaluation · Positional therapy trial       │
  │                 ENT specialist referral · Weight management programme    │
  ├──────────────────────────────────────────────────────────────────────────┤
  │  NONE        →  Maintain current sleep schedule                          │
  │  (Low Risk)     Continue physical activity programme                     │
  │                 Annual sleep health screening                            │
  └──────────────────────────────────────────────────────────────────────────┘
```

<br/>

---

<br/>

## `11` · Deployment Guide

<br/>

### Inference Engine

The `SleepHealthPredictor` class is the unified inference engine for both the notebook and the web application. It handles all preprocessing, encoding, feature engineering, and prediction in a single `.predict()` call.

```python
from app import SleepHealthPredictor

predictor = SleepHealthPredictor(
    model_path  = 'models/best_model.pkl',
    enc_path    = 'models/label_encoders.pkl',
    target_path = 'models/target_encoder.pkl',
    feat_path   = 'configs/feature_metadata.json',
)

result = predictor.predict({
    'Age': 45, 'Gender': 'Male', 'Occupation': 'Nurse',
    'Sleep Duration': 5.5, 'Quality of Sleep': 4,
    'Physical Activity Level': 20, 'Stress Level': 9,
    'BMI Category': 'Obese', 'Blood Pressure': '145/95',
    'Heart Rate': 85, 'Daily Steps': 3000,
})

# result →
# {
#   'prediction':      'Sleep Apnea',
#   'confidence':       0.834,
#   'risk_tier':       'HIGH',
#   'probabilities':   {'None': 0.04, 'Insomnia': 0.13, 'Sleep Apnea': 0.83},
#   'recommendations': ['Polysomnography study recommended', ...]
# }
```

<br/>

### Production Deployment Checklist

```
  □  Run the notebook end-to-end to generate all models/ artifacts
  □  Verify models/best_model.pkl loads correctly via pickle
  □  Configure .env with production-grade credentials
  □  Set MLFLOW_TRACKING_URI to your remote tracking server
  □  Set MONGO_URI to your production MongoDB Atlas cluster
  □  Launch: streamlit run app.py --server.port 8501
  □  Schedule a daily drift monitoring evaluation job
  □  Establish a model retraining pipeline on new data batches
  □  Promote champion model to Production stage in MLflow Registry
  □  Enable structured logging ingestion (ELK / Datadog / CloudWatch)
```

<br/>

---

<br/>

## `12` · Configuration Reference

<br/>

### `config.yaml` — Complete Reference

```yaml
project:
  name:        "Sleep Health Intelligence Platform"
  version:     "2.0.0"
  environment: "development"            # development | staging | production

data:
  path:          "Sleep_health_and_lifestyle_dataset.csv"
  target_column: "Sleep Disorder"
  test_size:     0.20
  random_seed:   42

model:
  best_model_path:     "models/best_model.pkl"
  label_encoders_path: "models/label_encoders.pkl"
  target_encoder_path: "models/target_encoder.pkl"
  feature_pipeline:    "models/feature_pipeline.pkl"
  model_card:          "models/model_card.json"
  feature_metadata:    "configs/feature_metadata.json"

mlflow:
  tracking_uri:    ""                   # Override via MLFLOW_TRACKING_URI
  experiment_name: "SleepHealthIntelligencePlatform_v2"
  model_stage:     "Staging"

dagshub:
  repo_owner: "your-username"
  repo_name:  "sleep-health-intelligence"

mongodb:
  db_name: "sleep_health_db"
  collections:
    predictions:  "sleep_predictions"
    drift:        "model_drift_records"
    audit:        "platform_audit_logs"

logging:
  level:   "INFO"
  log_dir: "logs/"
```

<br/>

### Dependency Stack

```
CORE SCIENCE          GRADIENT BOOSTING      MLOPS & TRACKING
────────────          ─────────────────      ────────────────
numpy >= 1.24         xgboost  >= 2.0        mlflow   >= 2.7
pandas >= 2.0         lightgbm >= 4.0        dagshub  >= 0.3
scipy  >= 1.11        catboost >= 1.2
sklearn >= 1.3
matplotlib >= 3.7     OPTIMISATION           DEPLOYMENT
seaborn >= 0.12       ─────────────          ──────────
                      optuna   >= 3.3        streamlit >= 1.28

EXPLAINABILITY        DATABASE               UTILITIES
──────────────        ────────               ─────────
shap >= 0.43          pymongo  >= 4.5        chardet      >= 5.2
                                             pyyaml       >= 6.0
                                             python-dotenv >= 1.0
```

<br/>

---

<br/>

## ◈ Acknowledgements

<br/>

This platform is built on the **Sleep Health and Lifestyle Dataset** — a structured observational dataset capturing self-reported sleep metrics, lifestyle factors, and clinical measurements across 374 individuals spanning 11 occupational categories.

The analytical methodology draws from:

- **AHA 2017** — American Heart Association Blood Pressure Guidelines
- **WHO** — World Health Organisation BMI Classification Standards
- **AASM** — American Academy of Sleep Medicine sleep duration recommendations
- **SHAP** — Lundberg & Lee (2017), *A Unified Approach to Interpreting Model Predictions*
- **Optuna** — Akiba et al. (2019), *Optuna: A Next-generation Hyperparameter Optimization Framework*

<br/>

---

<br/>

## ◈ Disclaimer

<br/>

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   ⚠️  RESEARCH PROTOTYPE — NOT FOR CLINICAL USE                             │
│                                                                             │
│   This platform is developed for educational, research, and analytical     │
│   purposes only. It has not undergone clinical validation and must not      │
│   be used to inform, guide, or replace medical diagnosis or clinical        │
│   decision-making of any kind.                                              │
│                                                                             │
│   Predictions generated by this system are probabilistic estimates         │
│   derived from an observational dataset. They do not constitute a          │
│   medical opinion, clinical assessment, or diagnostic conclusion.          │
│                                                                             │
│   Always consult a qualified healthcare professional for sleep health       │
│   concerns, symptom evaluation, or treatment planning.                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

<br/>

---

<br/>

<div align="center">

```
─────────────────────────────────────────────────────────────────────────────
  Sleep Health Intelligence Platform  ·  v2.0.0  ·  Enterprise Edition
─────────────────────────────────────────────────────────────────────────────
```

**Built with** `scikit-learn` · `XGBoost` · `LightGBM` · `CatBoost` · `Optuna`
`SHAP` · `MLflow` · `DagsHub` · `MongoDB` · `Streamlit`

<br/>

*Engineered at the intersection of clinical research, production machine learning,*
*and responsible AI for healthcare analytics.*

</div>
