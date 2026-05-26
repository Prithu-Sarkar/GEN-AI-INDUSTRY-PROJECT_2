<div align="center">

# 🎓 Student Habits & Academic Performance
### End-to-End Machine Learning Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-Tuned-189AB4?style=for-the-badge)](https://xgboost.readthedocs.io)
[![Optuna](https://img.shields.io/badge/Optuna-HPO-6C63FF?style=for-the-badge)](https://optuna.org)
[![SHAP](https://img.shields.io/badge/SHAP-XAI-FF4B4B?style=for-the-badge)](https://shap.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-2ECC71?style=for-the-badge)](LICENSE)

<br/>

> *Predicting academic exam scores from student lifestyle data using a fully orchestrated*  
> *ML/DL pipeline — from raw CSV to ranked models with explainability and export.*

<br/>

```
 EDA  ──►  Feature Eng.  ──►  Baseline ML  ──►  Advanced ML  ──►  Deep Learning  ──►  XAI  ──►  Export
```

</div>

---

## 📌 Overview

This project builds a **production-grade, end-to-end predictive pipeline** on a synthetic dataset of 1,000 university students, where the goal is to predict **final exam scores** from 15+ lifestyle and habit features including study hours, sleep patterns, social media usage, diet quality, and mental health ratings.

The pipeline spans **9 structured phases** — advanced EDA with statistical annotations, domain-driven feature engineering, 20+ model comparisons across three tiers (Baseline ML, Advanced ML, Deep Learning), full XAI with SHAP, and automated artifact export.

---

## 📂 Dataset

| Property | Details |
|---|---|
| **Source** | `student_habits_performance.csv` |
| **Records** | 1,000 synthetic student entries |
| **Features** | 15+ (numeric + categorical) |
| **Target** | `exam_score` (continuous, regression) |
| **Origin** | Kaggle — Student Habits vs Academic Performance |

**Key features:** `study_hours_per_day`, `sleep_hours`, `attendance_percentage`, `mental_health_rating`, `social_media_hours`, `netflix_hours`, `diet_quality`, `exercise_frequency`, `parental_education_level`, `internet_quality`

---

## 🗂️ Project Structure

```
📦 student-performance-ml/
├── 📓 student_advanced_pipeline.ipynb   ← Main notebook (run in Colab)
├── 📄 README.md
└── 📁 output_artifacts/                 ← Auto-generated on run
    ├── 📁 eda/                          ← 9 EDA plots (PNG)
    ├── 📁 features/                     ← Feature importance charts
    ├── 📁 models/                       ← Model comparison charts + CSVs
    └── 📁 xai/                          ← SHAP + PDP + permutation plots
```

---

## 🚀 Pipeline Phases

### `Phase 1` — Environment Setup & Data Ingestion
Auto-installs all dependencies. Uploads CSV directly from local machine via Colab file picker. No Drive mounting required.

### `Phase 2` — Advanced EDA *(9 annotated visuals)*
| Visual | What it reveals |
|---|---|
| Histogram + KDE per feature | Distribution shape with Shapiro-Wilk normality test |
| Pearson Correlation Heatmap | Pairwise correlations masked by statistical significance (α=0.05) |
| Pairplot (top-4 features) | Joint distributions of highest-correlated predictors |
| Box + Strip plots | Exam score spread by each categorical feature with Levene variance test |
| Mahalanobis Outlier Detection | Multivariate outliers via Robust Covariance (top 2.5%) |
| FacetGrid (Diet × Internet) | Study-time ROI stratified by lifestyle quality |
| Mutual Information chart | Non-linear feature relevance beyond Pearson correlation |

Every chart saves automatically and prints a plain-English interpretation inline.

### `Phase 3` — Advanced Feature Engineering
13 engineered features derived from domain knowledge:

```python
study_effectiveness  = study_hours × (attendance / 100)
distraction_ratio    = total_screen_time / study_hours
wellbeing_index      = 0.4×mental_health + 0.3×sleep + 0.3×exercise
academic_load        = study_hours × attendance
study_x_mental       = study_hours × mental_health_rating
# + polynomial squares for top 3 drivers
# + binary label encoding + one-hot encoding
```

Feature selection via **Mutual Information threshold** (bottom 25% dropped). Scaling with **RobustScaler** (outlier-resistant).

### `Phase 4` — Baseline ML Framework *(9 models)*
Mirrors the original notebook as a reproducible benchmark:
`LinearRegression · Ridge · Lasso · DecisionTree · RandomForest · KNN · SVR · XGBoost · CatBoost`

Metrics tracked: **R², RMSE, MAE, MAPE, CV_R²** (5-fold cross-validation).

### `Phase 5` — Advanced ML Framework *(10 models)*
| Model | Method |
|---|---|
| XGBoost Tuned | Optuna TPE — 60 trials, 9 hyperparameters |
| LightGBM Tuned | Optuna TPE — 60 trials, 9 hyperparameters |
| CatBoost Tuned | Optuna TPE — 40 trials, 7 hyperparameters |
| RidgeCV / LassoCV | Alpha search over 30 log-spaced values |
| ElasticNet | L1+L2 combined regularisation |
| Huber Regressor | Outlier-robust linear model |
| Bayesian Ridge | Probabilistic regularisation |
| **Stacking Ensemble** | XGB+LGB+CAT+RF+ET → Ridge meta-learner (5-fold CV) |
| **Voting Ensemble** | Averaged predictions of top-3 boosters |

### `Phase 6` — Ultra-Advanced Deep Learning *(4 architectures)*

| Architecture | Design |
|---|---|
| **ANN Baseline** | 3 × 64 Dense + Dropout (original notebook replica) |
| **ANN Deep** | 256→128→64→32 + BatchNormalization + L2 regularisation |
| **ResNet-Style** | Two skip-connection residual blocks (128 units) |
| **Wide & Deep** | Parallel wide path (raw features) + deep path concatenated |

All architectures use `EarlyStopping (patience=15)` + `ReduceLROnPlateau (factor=0.5)` — training curves saved per model.

### `Phase 7` — Model Orchestration & Full Comparison
- **Master ranking table** across all 23+ models sorted by R²
- Colour-coded by tier: Baseline (blue) · Advanced ML (orange) · Deep Learning (purple)
- **Predicted vs Actual** scatter for top-3 models
- **Residual analysis** (scatter + distribution + Q-Q plot) for the overall best model

### `Phase 8` — Explainable AI (XAI)

| Method | Output |
|---|---|
| SHAP Bar | Global mean \|SHAP\| feature ranking |
| SHAP Beeswarm | Feature direction, magnitude, and value distribution |
| SHAP Waterfall | Per-student local explanation (why that prediction?) |
| SHAP Dependence | Non-linear feature–SHAP relationships |
| Permutation Importance | Drop in R² per feature, 20-repeat average with std bars |
| Partial Dependence Plots | Marginal effect of top-3 features on predicted score |

### `Phase 9` — Export
All plots (PNG), metrics tables (CSV), and SHAP importance files are collected into `output_artifacts/` and compressed into a single **downloadable ZIP** triggered automatically.

---

## 📊 Key Results (indicative — actual values vary by run)

| Tier | Best Model | Typical R² |
|---|---|---|
| Baseline ML | XGBoost / RandomForest | ~0.88–0.91 |
| Advanced ML | Stacking / XGB Tuned | ~0.91–0.95 |
| Deep Learning | Wide & Deep / ResNet | ~0.89–0.93 |

---

## ⚙️ Requirements

All dependencies are installed automatically at notebook start. For reference:

```
numpy · pandas · matplotlib · seaborn · scipy
scikit-learn · xgboost · lightgbm · catboost
tensorflow · optuna · shap
```

> **Runtime recommendation:** GPU (T4 or better) for faster DL training.  
> Enable via `Runtime → Change runtime type → T4 GPU` in Colab.

---

## 🏃 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/student-performance-ml.git
cd student-performance-ml

# 2. Open the notebook in Google Colab
#    File → Open notebook → GitHub → paste repo URL

# 3. Run all cells (Runtime → Run all)
#    Upload student_habits_performance.csv when prompted in Phase 1

# 4. Collect your ZIP from browser downloads after Phase 9
```

---

## 📈 Output Artifacts

After a full run the following files are produced and downloaded:

```
output_artifacts/
  eda/
    numeric_distributions.png
    correlation_heatmap.png
    pairplot_top4.png
    categorical_boxplots.png
    mahalanobis_outliers.png
    facetgrid_diet_internet.png
    mutual_information.png
  features/
    extratrees_feature_importance.png
  models/
    baseline_model_comparison.png
    advanced_ml_comparison.png
    dl_training_curves.png
    master_model_comparison.png
    predicted_vs_actual_top3.png
    residual_analysis.png
    baseline_results.csv
    advanced_ml_results.csv
    dl_results.csv
    all_models_comparison.csv
  xai/
    shap_bar_global.png
    shap_beeswarm.png
    shap_waterfall_student0.png
    shap_dependence_top2.png
    permutation_importance.png
    partial_dependence_top3.png
    shap_feature_importance.csv
```

---

## 🧠 Key Findings

- **`study_hours_per_day`** and **`attendance_percentage`** are consistently the strongest predictors across all model tiers and XAI methods.
- **`mental_health_rating`** emerges as a critical non-linear moderator — captured clearly by SHAP dependence plots.
- Engineered features (`study_effectiveness`, `wellbeing_index`, `distraction_ratio`) improve model R² measurably over raw features alone.
- **Stacking ensembles** deliver the most stable performance; tuned individual boosters are competitive and faster.
- Deep Learning architectures approach but do not consistently surpass the best tree ensembles on this dataset size (n=1,000).

---

## 📐 Design Principles

- **Modular, phase-based cells** — each phase is independently readable and runnable
- **No Drive mounting** — CSV uploaded locally, no path dependencies
- **All outputs persisted** — every plot saved to disk before display
- **Statistical rigour** — p-value masking, Levene tests, Shapiro-Wilk, cross-validation throughout
- **Git-safe notebook** — valid nbformat 4.5, clean metadata, no stale execution counts

---

## 📄 License

This project is released under the [MIT License](LICENSE). Dataset is synthetic and intended for educational use.

---

<div align="center">

*Built with precision. Explained with SHAP. Ready for production.*

</div>
