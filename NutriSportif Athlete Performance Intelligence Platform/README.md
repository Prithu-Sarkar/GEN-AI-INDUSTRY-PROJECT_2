
<div align="center">

# ⚡ NutriSportif Athlete Performance Intelligence Platform

### *End-to-End Machine Learning & Explainable AI Pipeline for Endurance Athlete Dietary Optimisation*

---

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4%2B-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-006400?style=for-the-badge)](https://xgboost.readthedocs.io)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.0%2B-9ACD32?style=for-the-badge)](https://lightgbm.readthedocs.io)
[![Optuna](https://img.shields.io/badge/Optuna-3.x-4B8BBE?style=for-the-badge)](https://optuna.org)
[![SHAP](https://img.shields.io/badge/SHAP-XAI-FF6F61?style=for-the-badge)](https://shap.readthedocs.io)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)](LICENSE)

---

> **Production-grade analytical intelligence system** combining sports nutrition science, advanced statistical inference, 18-model machine learning architecture, Bayesian hyperparameter optimisation, and SHAP-driven explainability — delivering individualised performance and immune risk predictions for high-protein endurance athlete programmes.

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture & Pipeline Phases](#-architecture--pipeline-phases)
- [Dataset & Domain Context](#-dataset--domain-context)
- [Exploratory Data Analysis](#-phase-2--exploratory-data-analysis-20-visuals)
- [Feature Engineering](#-phase-3--advanced-feature-engineering)
- [Statistical Analysis](#-phase-4--rigorous-statistical-analysis)
- [Model Framework](#-phase-5--6--model-preparation--18-model-framework)
- [Hyperparameter Optimisation](#-phase-7--hyperparameter-optimisation)
- [XAI & SHAP Explainability](#-phase-8--xai--shap-explainability)
- [Immune Risk Model](#-phase-9--individualised-immune-risk-prediction-task-3)
- [Performance Results](#-performance-results-at-a-glance)
- [Output Artefacts](#-output-artefacts)
- [Installation & Execution](#-installation--execution)
- [Project Structure](#-project-structure)
- [Technical Stack](#-technical-stack)
- [Key Scientific Findings](#-key-scientific-findings)

---

## 🔬 Overview

The **NutriSportif Athlete Performance Intelligence Platform** is a comprehensive, production-oriented analytical pipeline constructed to address a critical intersection in sports science: **how French high-protein meal-prep recipes influence endurance athlete performance, immune function, and recovery outcomes**.

This system ingests a tri-table nutritional database (recipes, ingredients, food safety protocols) alongside a richly engineered synthetic endurance-athlete cohort of **N = 500 athletes**, constructed from peer-reviewed sports nutrition literature parameters. The pipeline executes ten distinct analytical phases — from raw ingestion through explainable AI — delivering **individually actionable dietary intervention recommendations**.

### Mission Objectives

| Objective | Description | Outcome |
|-----------|-------------|---------|
| **Task 1** | Classify high-performing athletes (top-30th percentile perf score) | XGBoost + SMOTE · AUC **0.951** |
| **Task 2** | Regress continuous performance scores across athlete population | LGB Regressor · R² **> 0.85** |
| **Task 3** | Predict individual immune suppression risk from dietary patterns | LightGBM (Optuna) · AUC **> 0.83** |

---

## 🏗 Architecture & Pipeline Phases

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  NUTRISPORTIF INTELLIGENCE PIPELINE                         │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┤
│ PHASE 0  │ PHASE 1  │ PHASE 2  │ PHASE 3  │ PHASE 4  │ PHASE 5  │ PHASE 6  │
│  Env     │  Data    │  EDA     │  Feature │  Stats   │  Model   │  18-Model│
│  Setup   │ Ingest   │ 20+Viz   │  Eng.    │ Analysis │  Prep    │ Framework│
├──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┤
│ PHASE 7  │ PHASE 8  │  PHASE 9 │         PHASE 10                          │
│  Optuna  │  XAI /   │  Immune  │         Pipeline Summary                  │
│  Tuning  │  SHAP    │  Model   │         + ZIP Export                      │
└──────────┴──────────┴──────────┴───────────────────────────────────────────┘
```

Each phase is **independently documented**, produces named output artefacts, and is designed for reproducibility across environments.

---

## 📊 Dataset & Domain Context

### NutriSportif Recipe Database

The system ingests three structured relational tables representing the NutriSportif French high-protein meal-prep product line:

| Table | Records | Key Columns |
|-------|---------|-------------|
| `df_rec` · Recipes | 3 | `id_recette`, `proteines_g`, `glucides_g`, `lipides_g`, `calories_kcal` |
| `df_ing` · Ingredients | 12 | `nom_ingredient`, `quantite`, `unite` per recipe |
| `df_sec` · Food Safety | 7 | `categorie`, `temperature_min/max_c`, `duree_max_h` |

**Flagship Recipes:**
- 🍗 **Poulet Riz Brocoli** — 45g protein · 490 kcal · highest protein provision
- 🌿 **Lentilles Œufs Épinards** — 38g protein · 471 kcal · lowest immune-risk association
- 🍠 **Dinde Patate Douce Haricots** — 42g protein · 476 kcal · highest carbohydrate for glycogen replenishment

All three recipes maintain protein calorie fractions **above 32%** — substantially exceeding the 15–20% general-population dietary guideline benchmark.

### Synthetic Endurance-Athlete Cohort (N = 500)

A statistically grounded synthetic dataset, parameterised from sports science literature, with the following schema:

| Feature Category | Variables |
|-----------------|-----------|
| **Demographics** | `age`, `gender`, `height_cm`, `weight_kg`, `bmi` |
| **Training Load** | `training_years`, `weekly_hours`, `vo2max`, `resting_hr`, `lactate_threshold` |
| **Nutrition** | `protein_g`, `carbs_g`, `fat_g`, `calories_total`, macro percentages |
| **Meal Timing** | `meal_frequency`, `pre_workout_carbs`, `post_workout_prot`, `hydration_L` |
| **Recipe Usage** | `recipe_id`, `recipe_freq_week` |
| **Immune Biomarkers** | `il6_pgml`, `crp_mgl`, `iga_saliva` |
| **Performance Targets** | `perf_score`, `fatigue_score`, `recovery_score`, `high_performer`, `immune_risk` |

> **Class distribution:** High-performer rate ~30% (stratified) · Immune-risk rate ~35%

---

## 📈 Phase 2 — Exploratory Data Analysis (20+ Visuals)

A comprehensive 20-visual EDA suite, each panel delivering an actionable sports nutrition insight:

| Visual | File | Key Finding |
|--------|------|-------------|
| Macronutrient Bar Chart | `eda_01_macronutrients.png` | Recipe 1 leads protein (45g); Recipe 3 highest carbs (60g) for post-endurance glycogen |
| Caloric Donut Charts | `eda_02_calorie_donuts.png` | All recipes sustain protein-calorie fraction >32% |
| Ingredient Quantities | `eda_03_ingredient_qty.png` | Patate douce (250g) & Brocoli (200g) are highest-volume inputs |
| Feature Distributions | `eda_04_distributions.png` | VO2max near-normal; weekly hours right-skewed (mode 8–15h) |
| Full Correlation Heatmap | `eda_05_corr_heatmap.png` | VO2max–perf_score r ≈ +0.60; IL-6 inversely correlated |
| Perf × Recipe × Gender | `eda_06_perf_recipe_gender.png` | Male athletes on Recipe 1 show highest median performance |
| Pair-plot | `eda_07_pairplot.png` | VO2max/perf_score most linearly separable; IL-6 bimodal in low performers |
| Immune Violin Plots | `eda_08_immune_violin.png` | High performers: ↓IL-6, ↓CRP, ↑IgA — dietary-immune axis confirmed |
| Protein/kg vs VO2max | `eda_09_protein_vo2max.png` | Athletes >2.0 g/kg cluster in high-performer zone |
| Hours vs Fatigue | `eda_10_hours_fatigue.png` | Immune-risk athletes concentrate in high-hours/high-fatigue quadrant |
| Macro KDE per Recipe | `eda_11_macro_kde.png` | Distribution shifts confirm recipe-specific macronutrient profiles |
| Gender × Recipe Heatmap | `eda_12_gender_recipe_heatmap.png` | Mean protein_g and perf_score disaggregated by gender and recipe |
| Recovery × Meal Freq | `eda_13_recovery_meal_freq.png` | 5–6 meals/day athletes show highest recovery (optimised MPS) |
| Hydration vs VO2max | `eda_14_hydration_vo2.png` | Fatigue quartile stratification reveals hydration–aerobic capacity gradient |
| Immune Risk by Recipe | `eda_15_immune_risk_recipe.png` | Recipe 2 (Lentils+Eggs) shows lowest immune-risk proportion |
| Bivariate Scatters | `eda_16_bivariate.png` | Pearson r annotated: VO2max/perf (0.60), IL-6/perf (−0.29) |
| KDE High vs Low | `eda_17_kde_comparison.png` | Clear distributional shifts for all 6 key variables |
| Nutritional Radar | `eda_18_radar.png` | Per-recipe polar profiles for macro + calorie comparison |
| CDF Performance | `eda_19_cdf.png` | Cumulative distribution confirms 70th-percentile threshold selection |
| Nutrition–Immune Corr | `eda_20_nutrition_immune_corr.png` | Protein-to-calorie ratio inversely correlated with inflammatory markers |

---

## ⚙️ Phase 3 — Advanced Feature Engineering

**15 engineered features** derived from domain-aware transformations, yielding a ~3 percentage-point AUC improvement over raw features:

### Ratio & Density Features
| Feature | Formula | Rationale |
|---------|---------|-----------|
| `protein_per_kg` | `protein_g / weight_kg` | Body-relative protein adequacy |
| `carbs_per_kg` | `carbs_g / weight_kg` | Glycogen replenishment normalised |
| `caloric_density` | `calories_total / weight_kg` | Energy availability per unit mass |
| `protein_to_carb` | `protein_g / (carbs_g + ε)` | Macronutrient ratio signal |
| `protein_to_calorie` | `(protein_g × 4) / calories_total` | Protein fraction quality metric |

### Training Load Features
| Feature | Formula | Rationale |
|---------|---------|-----------|
| `training_load` | `weekly_hours × training_years` | Cumulative training stimulus |
| `aerobic_capacity` | `vo2max × weekly_hours / 10` | Integrated aerobic output |
| `recovery_efficiency` | `recovery_score / (fatigue_score + 1)` | Physiological adaptation ratio |
| `resting_hr_per_vo2` | `resting_hr / vo2max` | Cardiovascular efficiency index |

### Immune Composite Features
| Feature | Formula | Rationale |
|---------|---------|-----------|
| `inflamm_index` | `(il6_pgml + crp_mgl) / 2` | Mean inflammatory burden |
| `immune_composite` | `iga_saliva / (inflamm_index + 1)` | Protective-to-inflammatory ratio |
| `il6_crp_ratio` | `il6_pgml / (crp_mgl + ε)` | Cytokine balance indicator |

### Additional Transformations
- **Polynomial interactions** (degree-2): `poly_vo2_prot`, `poly_vo2_hrs`, `poly_prot_hrs`
- **Log transforms**: `log_il6_pgml`, `log_crp_mgl`, `log_training_load` (right-skew correction)
- **Ordinal bins**: `protein_tier` (Low / Moderate / High / VeryHigh), `vo2max_tier` (Beginner → Elite)
- **Timing score**: `0.5 × pre_workout_carbs + 0.5 × post_workout_prot`

> Output visualisations: `fe_01_engineered_features.png` · `fe_02_engineered_corr.png`

---

## 📐 Phase 4 — Rigorous Statistical Analysis

A comprehensive hypothesis-testing framework spanning five statistical methodologies:

### Test Battery

| Test | Target | Result |
|------|--------|--------|
| **Shapiro-Wilk + D'Agostino** | Normality of 5 key features | Mixed; non-normal distribution confirmed for IL-6, CRP |
| **Kruskal-Wallis H-test** | Feature differences across recipe groups | Significant for `perf_score`, `protein_per_kg`, `immune_composite` |
| **Mann-Whitney U** | High vs Low performer group separation | All key features: p < 0.0001 |
| **One-way ANOVA** | Performance score × meal frequency | Significant (p < 0.01) — 5–6 meal cadence optimal |
| **Chi-Square** | `immune_risk` × `high_performer` independence | Significant association confirmed |

### OLS Regression
A full OLS regression of `perf_score` on five predictor blocks (`protein_per_kg`, `vo2max`, `weekly_hours`, `inflamm_index`, `recovery_efficiency`) confirms:

- **R² ≈ 0.62** — model explains majority of performance variance
- `vo2max` is the dominant predictor (β ≫ 0, p < 0.001)
- `inflamm_index` exerts a significant negative effect (p < 0.01)

### Effect Sizes (Cohen's *d*)

| Feature | Cohen's *d* | Interpretation |
|---------|------------|----------------|
| `vo2max` | > 1.0 | **Large effect** |
| `protein_per_kg` | ~ 0.7 | **Medium–Large** |
| `il6_pgml` | ~ −0.55 | **Medium (negative)** |
| `crp_mgl` | ~ −0.45 | **Small–Medium (negative)** |
| `immune_composite` | ~ 0.6 | **Medium** |

> Output visualisations: `stat_01_qqplots.png` · `stat_02_tukey.png` · `stat_03_cohens_d.png` · `stat_04_ols_diagnostics.png`  
> Export: `statistical_results.csv`

---

## 🤖 Phases 5 & 6 — Model Preparation & 18-Model Framework

### Feature Matrix
**36 input features** after engineering and encoding, scaled with `RobustScaler` (outlier-robust). 80/20 stratified train-test split; 5-fold `StratifiedKFold` cross-validation throughout.

### Model Taxonomy

**Baseline Estimators** *(establishing chance-level bounds)*
- Dummy Stratified · Dummy Most-Frequent · Gaussian Naïve Bayes · Logistic Regression

**Advanced Classical & Ensemble Models**
- KNN (k=5) · Decision Tree (max_depth=6) · SVM (RBF kernel)
- Random Forest (200 trees) · Extra Trees (200 trees) · Gradient Boosting (200 estimators)
- AdaBoost (100 estimators) · Bagging (Decision Tree base) · SGD Classifier

**Gradient-Boosted Frameworks**
- XGBoost · LightGBM · CatBoost

**Meta-Ensemble Models**
- Soft Voting (RF + XGB + LGB) · Stacking with Logistic Regression meta-learner

### Raw Baseline Performance (Pre-Tuning)

| Tier | Best Model | ROC-AUC |
|------|-----------|---------|
| Baseline | Logistic Regression | ~0.72 |
| Advanced | Extra Trees | ~0.91 |
| Gradient Boosting | XGBoost | ~0.88 |
| Ensemble | Voting (Soft) | ~0.90 |

> Output visualisations: `model_01_roc_auc.png` · `model_02_metric_heatmap.png`  
> Export: `model_results.csv`

---

## 🎯 Phase 7 — Hyperparameter Optimisation

### Optuna Bayesian Optimisation (TPE Sampler)

Both primary models underwent **30-trial TPE-guided** Bayesian search across 7-dimensional hyperparameter spaces:

**XGBoost Search Space:** `n_estimators` [100–400], `max_depth` [3–9], `learning_rate` [0.01–0.3 log], `subsample` [0.6–1.0], `colsample_bytree` [0.5–1.0], `reg_alpha` [1e-4–10 log], `reg_lambda` [1e-4–10 log]

**LightGBM Search Space:** `n_estimators`, `max_depth`, `learning_rate`, `num_leaves` [20–100], `subsample`, `colsample_bytree`, `min_child_samples` [5–50]

### SMOTE Class Balancing

`imblearn.over_sampling.SMOTE` applied to training set to address class imbalance, improving minority-class recall by approximately **+12 percentage points** vs raw baseline.

### Random Search — Random Forest

`RandomizedSearchCV` (30 iterations, 3-fold CV) over `n_estimators`, `max_depth`, `min_samples_split`, `max_features`, and `class_weight`.

### Tuning Performance Comparison

| Model | Baseline AUC | Tuned AUC | Delta |
|-------|-------------|-----------|-------|
| XGBoost | ~0.88 | ~0.940 | +0.06 |
| XGBoost + SMOTE | — | **~0.951** | — |
| LightGBM | ~0.87 | ~0.935 | +0.065 |
| Random Forest | ~0.91 | ~0.920 | +0.01 |

> Output visualisations: `tuning_01_optuna_history.png` · `tuning_02_baseline_vs_tuned.png` · `tuning_03_confusion_matrices.png` · `model_03_roc_pr.png`  
> Export: `tuning_comparison.csv`

---

## 🧠 Phase 8 — XAI & SHAP Explainability

Full post-hoc explainability suite applied to the tuned XGBoost champion model using the `shap.TreeExplainer` backend.

### SHAP Analysis Suite

| Artefact | Visualisation | Insight |
|----------|--------------|---------|
| **Summary Plot** | `xai_01_shap_summary.png` | `vo2max` and `aerobic_capacity` dominate positive predictions; `il6_pgml` drives low-performer class |
| **Global Bar Importance** | `xai_02_shap_bar.png` | Mean absolute SHAP ranking: vo2max > aerobic_capacity > protein_per_kg > inflamm_index |
| **Waterfall (Single Athlete)** | `xai_03_shap_waterfall.png` | Full decomposition of individual prediction from base rate |
| **Dependence Plot** | `xai_04_shap_dependence.png` | VO2max × protein_per_kg interaction: higher protein amplifies VO2max positive SHAP — confirmed synergy |
| **Permutation Importance** | `xai_05_permutation_importance.png` | Model-agnostic validation of feature ranking; 20-repeat stability estimates |

### Top 3 SHAP Features (Global Importance)

```
  1.  vo2max                  ████████████████████  Primary aerobic capacity driver
  2.  aerobic_capacity         ███████████████       Integrated training output signal
  3.  protein_per_kg           ████████████          Dietary modifiable predictor
  4.  inflamm_index            ████████              Negative — actionable via nutrition
  5.  immune_composite         ███████               Protective dietary marker
```

> The SHAP dependence plot confirms a **synergistic interaction**: athletes consuming >2.0 g protein/kg body weight exhibit amplified positive SHAP contributions from vo2max — supporting combined dietary + training prescription.

---

## 🛡 Phase 9 — Individualised Immune Risk Prediction (Task 3)

A **dedicated immune suppression risk classifier** (LightGBM, Optuna-tuned, 30-trial TPE) trained on the same feature matrix to predict `immune_risk` (binary: IL-6 > 4 pg/mL or CRP > 3 mg/L).

### Model Configuration
- **Architecture:** LightGBM with `class_weight="balanced"` for immune-risk minority handling
- **Optimisation:** 7-parameter Optuna search with `min_child_samples` guard against overfit on minority class
- **Evaluation:** 5-fold stratified CV AUC

### Immune Risk Model Performance

| Metric | Value |
|--------|-------|
| **Test ROC-AUC** | > 0.83 |
| **F1 Score** | Competitive across both classes |
| **Key SHAP Drivers** | `weekly_hours` (↑risk), `protein_per_kg` (↓risk) |

### Actionable Dietary Intervention Targets

> SHAP analysis of the immune model (`xai_07_immune_shap.png`) identifies two **directly modifiable** intervention levers:
> 1. **Reduce weekly training hours** below critical threshold for athletes flagged at-risk
> 2. **Increase protein intake above 2.0 g/kg/day** — the most nutritionally actionable protective factor

### Dynamic Prediction API

The pipeline exposes a `predict_athlete_adaptation()` function for real-time individual inference:

```python
result = predict_athlete_adaptation({
    "age": 32, "gender": "Male", "weight_kg": 74,
    "vo2max": 58, "weekly_hours": 12.5,
    "protein_g": 148, "recipe_id": 1,
    "il6_pgml": 2.1, "crp_mgl": 0.8, ...
})

# Returns:
# {
#   "high_performer_prob":  0.8742,
#   "high_performer_class": 1,
#   "immune_risk_prob":     0.1831,
#   "immune_risk_class":    0
# }
```

---

## 🏆 Performance Results at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│               FINAL BENCHMARK SUMMARY                       │
├────────────────────────────┬────────────┬───────────────────┤
│ Task                       │ Best Model │ Test ROC-AUC      │
├────────────────────────────┼────────────┼───────────────────┤
│ Performance Classification │ XGB+SMOTE  │     0.951         │
│ (high_performer)           │ (Optuna)   │  CV-AUC: 0.909    │
├────────────────────────────┼────────────┼───────────────────┤
│ Performance Regression     │ LGB / XGB  │   R² > 0.85       │
│ (perf_score continuous)    │ Regressor  │   RMSE < 4.2      │
├────────────────────────────┼────────────┼───────────────────┤
│ Immune Risk Classification │ LGB Optuna │     0.830+        │
│ (immune_risk)              │ Balanced   │  F1 competitive   │
└────────────────────────────┴────────────┴───────────────────┘
```

> Performance envelope consistent with **production-grade biomedical prediction systems** (AUC > 0.90 classification benchmark, Janssens & Martens, 2020).

---

## 📦 Output Artefacts

All outputs are written to the `outputs/` directory and bundled into `nutrisportif_full_analysis.zip`:

### Visualisations (39 PNG files)

| Prefix | Phase | Count |
|--------|-------|-------|
| `eda_01` – `eda_20` | Exploratory Data Analysis | 20 |
| `fe_01` – `fe_02` | Feature Engineering | 2 |
| `stat_01` – `stat_04` | Statistical Analysis | 4 |
| `model_01` – `model_04` | Model Framework & Regression | 4 |
| `tuning_01` – `tuning_03` | Hyperparameter Tuning | 3 |
| `xai_01` – `xai_07` | SHAP / Explainability | 6 |

### Structured Data Exports

| File | Contents |
|------|----------|
| `model_results.csv` | Full 18-model metric table (Accuracy, Precision, Recall, F1, AUC, CV-AUC) |
| `statistical_results.csv` | All hypothesis test statistics and p-values |
| `tuning_comparison.csv` | Baseline vs tuned performance delta table |
| `regression_results.csv` | 9-model regression benchmark (RMSE, MAE, R²) |
| `pipeline_summary.csv` | Phase-by-phase key findings summary |

---

## 🚀 Installation & Execution

### Prerequisites

```bash
Python >= 3.10
pip (latest)
```

### Environment Setup

```bash
# Clone repository
git clone https://github.com/your-org/nutrisportif-intelligence-platform.git
cd nutrisportif-intelligence-platform

# Create isolated virtual environment
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
.venv\Scripts\activate          # Windows

# Install all dependencies
pip install -r requirements.txt
```

### Requirements

```text
scikit-learn>=1.4.0
xgboost>=2.0.0
lightgbm>=4.0.0
catboost>=1.2.0
shap>=0.44.0
optuna>=3.4.0
imbalanced-learn>=0.12.0
statsmodels>=0.14.0
matplotlib>=3.8.0
seaborn>=0.13.0
scipy>=1.12.0
numpy>=1.26.0
pandas>=2.1.0
```

### Execute Full Pipeline

```bash
# Run all 10 phases sequentially
jupyter nbconvert --to notebook --execute Athlete_NutriSportif_Immune_Model_Pipeline.ipynb \
    --output Athlete_NutriSportif_Immune_Model_Pipeline_executed.ipynb
```

Or launch interactively:

```bash
jupyter lab Athlete_NutriSportif_Immune_Model_Pipeline.ipynb
```

> All phases execute sequentially. Optuna tuning (Phases 7 & 9) runs 30 trials each — estimated total runtime: **8–15 minutes** on standard hardware.

### Quick Individual Prediction

```python
from pipeline import predict_athlete_adaptation

athlete_profile = {
    "age": 28, "gender": "Female", "weight_kg": 60,
    "vo2max": 52, "weekly_hours": 10.0,
    "protein_g": 132, "carbs_g": 290, "fat_g": 55,
    "calories_total": 2215, "meal_frequency": 5,
    "recipe_id": 2, "il6_pgml": 1.8, "crp_mgl": 0.6,
    # ... full feature set
}

prediction = predict_athlete_adaptation(athlete_profile)
print(prediction)
```

---

## 📁 Project Structure

```
nutrisportif-intelligence-platform/
│
├── Athlete_NutriSportif_Immune_Model_Pipeline.ipynb   ← Main pipeline notebook
│
├── outputs/                                           ← All generated artefacts
│   ├── eda_01_macronutrients.png
│   ├── ... (39 visualisation files)
│   ├── model_results.csv
│   ├── statistical_results.csv
│   ├── tuning_comparison.csv
│   ├── regression_results.csv
│   └── pipeline_summary.csv
│
├── nutrisportif_full_analysis.zip                     ← Bundled export
│
├── requirements.txt                                   ← Python dependencies
└── README.md                                          ← This document
```

---

## 🛠 Technical Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Core ML** | scikit-learn | ≥ 1.4 | Model framework, preprocessing, evaluation |
| **Gradient Boosting** | XGBoost | ≥ 2.0 | Champion classifier (tuned + SMOTE) |
| **Gradient Boosting** | LightGBM | ≥ 4.0 | Immune risk classifier; fast training |
| **Gradient Boosting** | CatBoost | ≥ 1.2 | Additional ensemble member |
| **Hyperparameter Opt.** | Optuna | ≥ 3.4 | Bayesian TPE search, 30-trial budgets |
| **Class Balancing** | imbalanced-learn | ≥ 0.12 | SMOTE synthetic oversampling |
| **Statistical Testing** | SciPy + Statsmodels | ≥ 1.12 / 0.14 | Hypothesis testing, OLS regression |
| **Explainability** | SHAP | ≥ 0.44 | TreeExplainer, waterfall, dependence plots |
| **Visualisation** | Matplotlib + Seaborn | ≥ 3.8 / 0.13 | 39 publication-grade figures |
| **Data Layer** | Pandas + NumPy | ≥ 2.1 / 1.26 | Data manipulation and numerical ops |

---

## 🔑 Key Scientific Findings

The pipeline synthesises findings across all ten phases into the following evidence-based conclusions:

1. **VO2max is the dominant performance predictor** (Cohen's *d* > 1.0; top SHAP feature) — confirming aerobic capacity as the primary determinant of endurance performance.

2. **Protein intake at 2.0+ g/kg/day is the most actionable dietary intervention** — athletes above this threshold cluster strongly in the high-performer zone and exhibit amplified positive SHAP contributions.

3. **The dietary-immune axis is statistically confirmed** — high performers exhibit significantly lower IL-6/CRP and higher salivary IgA (p < 0.0001 by Mann-Whitney U); Recipe 2 (Lentilles-Œufs-Épinards) carries the lowest immune-risk prevalence.

4. **Five to six structured meals per day optimises recovery** — meal frequency is significantly associated with recovery score (ANOVA p < 0.01); NutriSportif's three-recipe system is architecturally compatible with this cadence.

5. **Weekly training load is a primary modifiable immune-risk factor** — SHAP analysis of the immune model identifies `weekly_hours` as the strongest driver of elevated IL-6/CRP risk, with protein intake as the most effective dietary countermeasure.

6. **Ensemble + Bayesian-tuned gradient boosting achieves production-grade AUC** — the XGBoost + SMOTE model (AUC 0.951, CV-AUC 0.909) and the immune LightGBM model (AUC > 0.83) both satisfy biomedical prediction system benchmarks for clinical deployment consideration.

---

<div align="center">

---

*Built for the NutriSportif High-Protein Meal-Prep Research Programme*  
*Advanced Sports Nutrition Analytics Division*

**© 2025 NutriSportif Analytics. All rights reserved.**

</div>
