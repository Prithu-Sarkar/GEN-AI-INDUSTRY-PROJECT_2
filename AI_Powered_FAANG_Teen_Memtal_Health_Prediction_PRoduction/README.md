<div align="center">

<br/>

```
████████╗███╗   ███╗██╗          ██████╗ ██╗██████╗ ███████╗██╗     ██╗███╗   ██╗███████╗
   ██╔══╝████╗ ████║██║         ██╔════╝ ██║██╔══██╗██╔════╝██║     ██║████╗  ██║██╔════╝
   ██║   ██╔████╔██║██║         ██║  ███╗██║██████╔╝█████╗  ██║     ██║██╔██╗ ██║█████╗  
   ██║   ██║╚██╔╝██║██║         ██║   ██║██║██╔══██╗██╔══╝  ██║     ██║██║╚██╗██║██╔══╝  
   ██║   ██║ ╚═╝ ██║███████╗    ╚██████╔╝██║██║  ██║███████╗███████╗██║██║ ╚████║███████╗
   ╚═╝   ╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝
```

# 🧠 Teen Mental Health — End-to-End Production ML Pipeline

*A rigorous, interpretable, and fully traceable machine learning system for adolescent mental health risk stratification*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4.2-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-00ADD8?style=for-the-badge)](https://xgboost.readthedocs.io)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.3.0-00B050?style=for-the-badge)](https://lightgbm.readthedocs.io)
[![MLflow](https://img.shields.io/badge/MLflow-2.13.0-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.7.2-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![SHAP](https://img.shields.io/badge/SHAP-0.45.1-FF6B6B?style=for-the-badge)](https://shap.readthedocs.io)
[![Optuna](https://img.shields.io/badge/Optuna-3.6.1-6C4AB6?style=for-the-badge)](https://optuna.org)
[![GPU](https://img.shields.io/badge/GPU-Accelerated-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-toolkit)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

---

*"Mental health is not a destination, but a process. This pipeline makes that process measurable."*

---

</div>

<br/>

## 📌 Table of Contents

- [Overview](#-overview)
- [Architecture](#-pipeline-architecture)
- [Pipeline Phases](#-pipeline-phases-at-a-glance)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Configuration & Secrets](#-configuration--secrets)
- [Model Experimentation](#-model-experimentation-framework)
- [Interpretability](#-model-interpretability)
- [Experiment Tracking](#-experiment-tracking--mlflow)
- [Data Persistence](#-data-persistence--mongodb)
- [Deliverables](#-production-deliverables)
- [Results Snapshot](#-results-snapshot)
- [Contributing](#-contributing)

<br/>

---

## 🔭 Overview

This project delivers a **production-grade, end-to-end machine learning pipeline** for teen mental health classification — built to the standards expected in senior data science roles at top-tier technology companies. It combines rigorous statistical methodology, advanced ensemble modelling, and enterprise-level MLOps infrastructure into a single cohesive, reproducible system.

The pipeline is designed around three core principles:

| Principle | Implementation |
|-----------|---------------|
| **Rigour** | Multi-method statistical validation, normality tests, effect sizes, multivariate outlier detection |
| **Interpretability** | SHAP (global + local), LIME, PDP, ICE — every prediction is explainable |
| **Traceability** | MLflow experiment lineage, MongoDB audit trails, timestamped artefact versioning |

> **Domain Context:** Adolescent mental health assessment is a high-stakes classification problem where both false positives and false negatives carry real consequences. The pipeline's emphasis on multi-metric evaluation (F1-Macro, ROC-AUC, MCC, Cohen's Kappa) and interpretability is a deliberate design choice reflecting this sensitivity.

<br/>

---

## 🏗 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     TEEN MENTAL HEALTH ML PIPELINE v3.0.0                   │
└─────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────────────────┐
│   PHASE 0       │     │   PHASE 1        │     │   PHASE 2                   │
│  Environment    │────▶│  Data Ingestion  │────▶│  Exploratory Data Analysis  │
│  GPU · Secrets  │     │  Validation      │     │  6 Executive Visuals        │
│  Folders · Logs │     │  Schema Audit    │     │  3 Correlation Methods      │
└─────────────────┘     └─────────────────┘     └─────────────────────────────┘
                                                           │
         ┌─────────────────────────────────────────────────┘
         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────────────────┐
│   PHASE 3       │     │   PHASE 4        │     │   PHASE 5                   │
│  Statistical    │────▶│  Feature Eng.    │────▶│  Model Experimentation      │
│  Analysis       │     │  KNN Impute      │     │  15+ Algorithms             │
│  ANOVA · χ²     │     │  Yeo-Johnson     │     │  Optuna Tuning              │
│  Effect Sizes   │     │  SMOTE           │     │  Stacking Ensemble          │
└─────────────────┘     └─────────────────┘     └─────────────────────────────┘
                                                           │
         ┌─────────────────────────────────────────────────┘
         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────────────────┐
│   PHASE 6       │     │   PHASE 7        │     │   PHASE 8                   │
│  Interpretab.   │────▶│  MLflow Track.   │────▶│  MongoDB Persistence        │
│  SHAP · LIME    │     │  DagsHub / Local │     │  Experiment Docs            │
│  PDP · ICE      │     │  Model Registry  │     │  Prediction Audit Trail     │
└─────────────────┘     └─────────────────┘     └─────────────────────────────┘
                                                           │
         ┌─────────────────────────────────────────────────┘
         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│   PHASE 9 — Production Deliverables                                          │
│   pkl · joblib · metadata JSON · Markdown Report · ZIP Archive               │
└─────────────────────────────────────────────────────────────────────────────┘
```

<br/>

---

## 🗺 Pipeline Phases at a Glance

### ⚙️ Phase 0 — Environment Setup
- **GPU verification** via `nvidia-smi` with runtime guidance
- **Dependency installation** with pinned versions for reproducibility
- **Secrets management** via secure credential injection (no hardcoded credentials)
- **Production folder initialisation** — `logs/`, `outputs/`, `models/`, `reports/`, `artifacts/`
- **Dual-output logging** — timestamped console + persistent file audit trail

---

### 📥 Phase 1 — Data Ingestion & Validation
- **Direct CSV upload** — no cloud storage mount required
- **Intelligent target detection** via regex pattern matching against 10+ mental health terminology patterns
- **Automated schema inference** — numeric, categorical, and date column role assignment
- **Comprehensive quality audit** — per-column missingness, cardinality, constant detection, duplicate flagging, high-cardinality alerts

---

### 📊 Phase 2 — Advanced Exploratory Data Analysis
| Visual | Method | Purpose |
|--------|--------|---------|
| Target Distribution | Bar + Pie | Class imbalance assessment |
| Numeric Distributions | KDE + Histogram | Skewness & kurtosis profiling |
| Missing Values | missingno Matrix + Bar | MCAR / MAR / MNAR pattern detection |
| Correlation Matrices | Pearson + Spearman + Kendall | Linear, monotonic & ordinal associations |
| Bivariate Analysis | Violin + Quartile Overlay | Class-conditional distribution shift |
| Categorical vs Target | Row-Normalised Cross-tabs | Subgroup risk factor identification |

---

### 📐 Phase 3 — Advanced Statistical Analysis
- **Normality Testing** — Shapiro-Wilk, D'Agostino-Pearson, Anderson-Darling (three independent tests per feature)
- **Group Comparison** — one-way ANOVA (parametric) + Kruskal-Wallis (non-parametric rank-based alternative)
- **Effect Sizes** — Cohen's *d* (pairwise, with magnitude labelling) + Eta-squared (omnibus variance explained)
- **Categorical Independence** — Chi-squared test + Cramér's *V* for standardised effect size
- **Multivariate Outlier Detection** — Mahalanobis distance with Chi-squared critical value at 99.9% confidence

---

### 🔧 Phase 4 — Feature Engineering Pipeline

```
Raw Features
     │
     ├── Numeric ──── KNN Imputation (k=5)
     │                     │
     │               Yeo-Johnson Power Transform
     │                     │
     │               StandardScaler
     │
     └── Categorical ─ Mode Imputation
                           │
                       OrdinalEncoder (unknown → -1)
                           │
               ColumnTransformer (no leakage)
                           │
               ┌───────────────────────┐
               │  Consensus Selection  │
               │  Mutual Information   │
               │  + Random Forest      │
               │  → Top-K Features     │
               └───────────────────────┘
                           │
                        SMOTE
                   (training only)
```

---

### 🤖 Phase 5 — Model Experimentation Framework

**15+ algorithms across all major learning paradigms:**

| Family | Algorithms |
|--------|-----------|
| **Linear / Probabilistic** | Logistic Regression, SGD Classifier, Linear Discriminant Analysis, Gaussian Naive Bayes |
| **Distance-Based** | KNN (k=5), KNN (k=11) |
| **Kernel** | SVM — RBF kernel, SVM — Linear kernel |
| **Tree** | Decision Tree |
| **Bagging Ensembles** | Random Forest (200 trees), Extra Trees (200 trees), Bagging |
| **Boosting Ensembles** | Gradient Boosting, AdaBoost, XGBoost, LightGBM, CatBoost |
| **Meta-Ensemble** | Stacking (top-3 base learners + Logistic Regression meta-learner) |

**Evaluation protocol:**
- Stratified 5-fold cross-validation on all models
- Metrics: Accuracy, F1-Macro, ROC-AUC (OVR weighted), Precision, Recall
- Optuna Bayesian optimisation — 50 trials, TPE sampler, 5-minute compute cap
- Hold-out test set evaluation with MCC and Cohen's Kappa

---

### 🔍 Phase 6 — Model Interpretability

| Method | Scope | What It Reveals |
|--------|-------|----------------|
| **SHAP TreeExplainer** | Global | Feature importance ranked by mean absolute SHAP value across all test samples |
| **SHAP Beeswarm** | Global | Distribution of SHAP contributions — direction and magnitude per feature |
| **SHAP Waterfall** | Local | Per-sample breakdown of how each feature pushes prediction from baseline |
| **LIME** | Local (×3) | Linear surrogate explanation in the neighbourhood of individual predictions |
| **PDP** | Global | Marginal effect of top features on model output, averaged across samples |
| **ICE** | Local overlay | Per-sample PDP — divergence from mean reveals feature interaction effects |

---

### 📊 Phase 7 — MLflow Experiment Tracking
- **Switchable backends** — DagsHub (remote) or local file-based tracking
- **Nested run hierarchy** — parent benchmark run containing one child run per model
- **Logged per run:** CV metrics (mean + std), model hyperparameters, tags, figures, tables
- **Model Registry** — best model registered with semantic name for deployment

---

### 🍃 Phase 8 — MongoDB Integration
- **Collections:** `experiments`, `prediction_audit`, `model_registry`
- **Experiment document** — full pipeline metadata, benchmark results, hyperparameters, run lineage
- **Prediction audit trail** — every test-set prediction logged with true label, predicted label, correctness flag, and UTC timestamp
- **Graceful mock mode** — pipeline continues without connectivity; documents printed to console

---

### 📦 Phase 9 — Production Deliverables
- **Model artefacts** — `.pkl` (standard), `.joblib` (optimised for numpy arrays), preprocessor, label encoder
- **Model card** — JSON metadata including feature list, class names, sklearn version, training provenance
- **Automated report** — structured Markdown summary with benchmark table and best-model scorecard
- **ZIP archive** — complete project tree excluding raw data, browser-downloadable in one click

<br/>

---

## 🛠 Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                        CORE STACK                               │
├─────────────────┬───────────────────────────────────────────────┤
│ Runtime         │ Python 3.10+ · GPU (NVIDIA T4 / A100)         │
│ Data            │ pandas 2.x · NumPy · SciPy · statsmodels       │
│ ML              │ scikit-learn 1.4 · XGBoost · LightGBM          │
│                 │ CatBoost · imbalanced-learn                    │
│ Optimisation    │ Optuna (TPE Sampler · Bayesian Search)         │
│ Interpretab.    │ SHAP · LIME · sklearn PDP/ICE                  │
│ Tracking        │ MLflow 2.13 · DagsHub                         │
│ Storage         │ MongoDB (pymongo 4.7)                          │
│ Visualisation   │ matplotlib · seaborn · plotly · missingno      │
│ Statistics      │ pingouin · scipy.stats · statsmodels           │
│ Packaging       │ joblib · pickle · zipfile                      │
└─────────────────┴───────────────────────────────────────────────┘
```

<br/>

---

## 📂 Project Structure

```
teen_mental_health_project/
│
├── 📓 teen_mental_health_faang_pipeline.ipynb   ← Main pipeline notebook
│
├── 📁 data/
│   ├── raw/                    ← Original uploaded CSV (preserved, unmodified)
│   ├── interim/                ← Intermediate transformation outputs
│   └── processed/              ← X_train.csv · X_test.csv · y_train.npy · y_test.npy
│
├── 📁 models/
│   ├── serialized/             ← best_model_<timestamp>.pkl · .joblib
│   │                             preprocessor.joblib · label_encoder.pkl
│   └── metadata/               ← model_metadata.json (model card)
│
├── 📁 outputs/
│   ├── figures/                ← 11 publication-quality PNG visualisations
│   └── tables/                 ← CSV exports: quality audit · normality · ANOVA
│                                 chi-squared · effect sizes · benchmark results
│
├── 📁 artifacts/
│   ├── shap/                   ← shap_global_summary.png · shap_waterfall_sample0.png
│   │                             pdp_ice_plots.png
│   └── lime/                   ← lime_sample_0.png · lime_sample_1.png · lime_sample_2.png
│
├── 📁 reports/
│   ├── classification_report.txt
│   └── final_report.md
│
└── 📁 logs/
    └── pipeline_<timestamp>.log   ← Full dual-output audit trail
```

<br/>

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Details |
|-------------|---------|
| Python | 3.10 or above |
| GPU Runtime | NVIDIA T4 or equivalent (recommended) |
| Dataset | Teen mental health survey CSV (any schema — auto-detected) |

### Quickstart

**Step 1 — Open the notebook in your GPU-enabled environment**

**Step 2 — Configure secrets** *(see [Configuration & Secrets](#-configuration--secrets))*

**Step 3 — Run Phase 0** to install all dependencies

**Step 4 — Upload your CSV** when prompted in Phase 1 — no storage mounts required

**Step 5 — Execute all phases sequentially** — each phase saves its outputs automatically

**Step 6 — Download the ZIP archive** from Phase 9 for your complete project deliverables

> **Note:** The pipeline runs fully offline with local MLflow tracking and MongoDB mock mode if external credentials are not configured. No connectivity is required for core functionality.

<br/>

---

## 🔐 Configuration & Secrets

All credentials are loaded securely at runtime. Add the following keys via your environment's **Secrets / Environment Variables** panel — never commit credentials to source control.

| Secret Key | Required | Purpose |
|------------|----------|---------|
| `MONGO_URI` | Optional | MongoDB Atlas connection string. Pipeline runs in mock mode if absent. |
| `DAGSHUB_TOKEN` | Optional | Personal access token for DagsHub remote MLflow tracking. |
| `DAGSHUB_REPO_OWNER` | Optional | DagsHub username / organisation name. |
| `DAGSHUB_REPO_NAME` | Optional | Target repository name for MLflow experiment logging. |

**MLflow backend selection is automatic:**
- `DAGSHUB_TOKEN` present → **DagsHub remote tracking**
- `DAGSHUB_TOKEN` absent → **Local file-based tracking** (`file:./mlruns`)

<br/>

---

## 🤖 Model Experimentation Framework

### Cross-Validation Benchmark

Every model is evaluated under identical conditions — stratified 5-fold cross-validation on SMOTE-resampled training data, with five metrics reported as `mean ± std`.

```
Model                   Accuracy          F1-Macro    ROC-AUC     Time (s)
─────────────────────── ─────────────     ─────────   ─────────   ────────
XGBoost                 x.xxxx ± x.xxxx   x.xxxx      x.xxxx      xx.x
LightGBM                x.xxxx ± x.xxxx   x.xxxx      x.xxxx      xx.x
Random Forest           x.xxxx ± x.xxxx   x.xxxx      x.xxxx      xx.x
Extra Trees             x.xxxx ± x.xxxx   x.xxxx      x.xxxx      xx.x
CatBoost                x.xxxx ± x.xxxx   x.xxxx      x.xxxx      xx.x
Gradient Boosting       x.xxxx ± x.xxxx   x.xxxx      x.xxxx      xx.x
Stacking Ensemble       x.xxxx ± x.xxxx   x.xxxx      x.xxxx      xx.x
... (15+ models total)
```

*Scores populate automatically on execution with your dataset.*

### Optuna Hyperparameter Optimisation

```python
# Search strategy
Sampler   : TPE (Tree-structured Parzen Estimator)
Trials    : 50
Inner CV  : 3-fold stratified
Objective : F1-Macro
Timeout   : 300 seconds (compute-safe cap)

# Search space includes
n_estimators     : [100, 600]
max_depth        : [3, 12]
learning_rate    : [0.01, 0.30]  (log scale)
subsample        : [0.50, 1.00]
colsample_bytree : [0.50, 1.00]
reg_alpha/lambda : [1e-4, 10]    (log scale)
```

<br/>

---

## 🔍 Model Interpretability

This pipeline treats interpretability as a first-class requirement, not an afterthought.

### Global Methods — *Why does the model behave as it does overall?*

**SHAP TreeExplainer** computes exact Shapley values for tree-based models in polynomial time. The beeswarm plot reveals both the ranking and the direction of each feature's influence across the entire test set.

**Partial Dependence Plots (PDP)** show the marginal effect of a feature on the predicted outcome, averaging out all other features — isolating the relationship between input and output.

### Local Methods — *Why did the model make this specific prediction?*

**SHAP Waterfall** decomposes a single prediction into a sum of feature contributions, showing precisely how the model arrived at its output for one individual.

**LIME** fits a locally faithful linear surrogate in the neighbourhood of each sample by perturbing inputs and observing prediction changes — model-agnostic and applicable even to black-box models.

**ICE Curves** overlay individual sample responses onto the PDP, surfacing heterogeneous effects and feature interactions that the mean-based PDP would otherwise obscure.

<br/>

---

## 📊 Experiment Tracking — MLflow

```
Experiment: teen_mental_health_<timestamp>
│
├── Run: benchmark_<timestamp>                    ← Parent run
│   ├── Params: n_models, cv_folds, smote, seed
│   ├── Artifacts: figures/*.png, tables/*.csv
│   │
│   ├── Run: XGBoost                              ← Nested child runs
│   │   ├── Metrics: cv_accuracy_mean/std, cv_f1_macro_mean ...
│   │   └── Tags: model_family=XGBoost, best_model=True/False
│   │
│   ├── Run: LightGBM
│   ├── Run: Random Forest
│   └── ... (one run per model)
│
└── Registered Model: TML_<BestModelName>
```

<br/>

---

## 🗄 Data Persistence — MongoDB

```javascript
// Collection: experiments
{
  "run_id"        : "20240315_143022",
  "mlflow_run_id" : "abc123...",
  "timestamp"     : "2024-03-15T14:30:22Z",
  "dataset"       : "teen_mental_health.csv",
  "target_column" : "mental_health_status",
  "best_model"    : {
    "name"       : "XGBoost",
    "cv_f1"      : 0.9123,
    "cv_accuracy": 0.9241,
    "best_params": { "n_estimators": 387, "max_depth": 6, ... }
  },
  "all_results"   : [ ... ]
}

// Collection: prediction_audit
{
  "run_id"    : "20240315_143022",
  "sample_idx": 42,
  "predicted" : "Moderate Risk",
  "true"      : "Moderate Risk",
  "correct"   : true,
  "timestamp" : "2024-03-15T14:35:11Z"
}
```

<br/>

---

## 📦 Production Deliverables

Every pipeline run auto-generates the following artefacts:

| Artefact | Format | Description |
|----------|--------|-------------|
| Best model | `.pkl` + `.joblib` | Serialised tuned estimator |
| Preprocessor | `.joblib` | Fitted ColumnTransformer (imputer + scaler + encoder) |
| Label encoder | `.pkl` | Fitted LabelEncoder for target class mapping |
| Model card | `.json` | Feature list, class names, metrics, training provenance |
| EDA figures | `.png` (×11) | Publication-quality visualisations at 150–180 DPI |
| Statistical tables | `.csv` (×5) | Quality audit, normality, ANOVA, chi-squared, effect sizes |
| SHAP artefacts | `.png` (×3) | Global summary, waterfall, PDP/ICE |
| LIME artefacts | `.png` (×3) | Local explanations for 3 representative samples |
| Classification report | `.txt` | Per-class precision, recall, F1, support |
| Final report | `.md` | Structured executive summary with benchmark table |
| Audit log | `.log` | Timestamped pipeline event log |
| ZIP archive | `.zip` | Complete deliverable bundle, browser-downloadable |

<br/>

---

## 📈 Results Snapshot

The pipeline surfaces a fully populated comparison table on execution. Key metrics tracked:

```
Primary   → F1-Macro    (class-imbalance-robust; primary ranking metric)
Secondary → ROC-AUC     (ranking quality; OVR weighted for multi-class)
Tertiary  → MCC         (Matthews Correlation Coefficient; balanced measure)
Auxiliary → Cohen's κ   (agreement beyond chance; clinical relevance)
```

**Feature Importance methods compared:** Mutual Information (model-free, non-linear) vs Random Forest Gini importance — consensus ranking reduces selection bias.

<br/>

---

## 📐 Statistical Rigour

This pipeline applies a three-tier statistical validation framework before any modelling begins:

```
Tier 1 — Univariate
  Normality : Shapiro-Wilk + D'Agostino-Pearson + Anderson-Darling
  Outliers  : IQR-based per feature

Tier 2 — Bivariate
  Continuous vs Target  : ANOVA (parametric) + Kruskal-Wallis (non-parametric)
  Categorical vs Target : Chi-squared + Cramér's V
  Effect Sizes          : Cohen's d (pairwise) + Eta-squared (omnibus)

Tier 3 — Multivariate
  Outlier detection : Mahalanobis distance (χ² threshold, 99.9% CI)
  Correlation       : Pearson + Spearman + Kendall (triangular heatmaps)
```

<br/>

---

## 🤝 Contributing

Contributions that extend the pipeline's rigour, coverage, or reproducibility are welcome.

```bash
# Clone and set up
git clone https://github.com/<your-org>/teen-mental-health-ml-pipeline.git
cd teen-mental-health-ml-pipeline

# Install dependencies
pip install -r requirements.txt

# Run validation
python -m pytest tests/ -v
```

**Areas open for contribution:**
- Additional model families (TabNet, NODE, deep tabular architectures)
- Fairness auditing across demographic subgroups
- Drift detection module for production monitoring
- REST API wrapper for model serving

Please open an issue before submitting large pull requests to align on scope and approach.

<br/>

---

## 📄 License

This project is released under the **MIT License** — see [`LICENSE`](LICENSE) for full terms.

<br/>

---

<div align="center">

```
Built with precision. Designed for impact. Grounded in evidence.
```

**Teen Mental Health ML Pipeline v3.0.0**

*Advancing data-driven mental health research through rigorous, interpretable, and reproducible machine learning*

<br/>

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f?style=flat-square&logo=python)](https://python.org)
[![MLOps Ready](https://img.shields.io/badge/MLOps-Ready-success?style=flat-square)](https://mlflow.org)
[![Interpretable AI](https://img.shields.io/badge/Interpretable-AI-informational?style=flat-square)](https://shap.readthedocs.io)
[![Production Grade](https://img.shields.io/badge/Production-Grade-blueviolet?style=flat-square)]()

</div>
