# 💎 Diamonds Price Tier Classification — Production ML Pipeline

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Colab%20Ready-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2D6A4F?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-52B788?style=for-the-badge)

**A fully self-contained, end-to-end machine learning pipeline for multi-class diamond price tier prediction — featuring custom Kernel SHAP and LIME implementations, five production-grade classifiers, and 13 publication-quality visualisations.**

[Overview](#-overview) · [Results](#-model-results) · [Pipeline](#-pipeline-architecture) · [Features](#-feature-engineering) · [XAI](#-explainability-xai) · [Usage](#-quick-start) · [Outputs](#-outputs) · [Structure](#-repository-structure)

</div>

---

## 📌 Overview

This project implements a **production-grade machine learning pipeline** to classify diamonds into four price tiers — **Budget**, **Mid-Low**, **Mid-High**, and **Premium** — based on their physical and quality attributes. The price tiers are defined by population quartiles ($950 / $2,401 / $5,324), yielding a perfectly balanced 4-class target.

Beyond standard classification, the pipeline includes **from-scratch implementations of Kernel SHAP and LIME** — no external XAI libraries — providing full transparency into both global model behaviour and individual prediction explanations.

| Property | Value |
|---|---|
| **Dataset** | Diamonds.csv — 53,940 records, 10 raw features |
| **Task** | 4-class Price Tier Classification |
| **Best Model** | Hist Gradient Boosting — **94.32% accuracy, AUC 0.9954** |
| **Features** | 26 total (10 raw + 16 engineered) |
| **XAI Methods** | Kernel SHAP + LIME (both built from scratch) |
| **Figures** | 13 publication-quality visualisations |
| **Environment** | Google Colab / Local Jupyter / Pure Python |

---

## 🏆 Model Results

All models were evaluated on a held-out 20% stratified test set (10,788 samples, ~2,698 per class).

| Model | Accuracy | Weighted F1 | ROC-AUC (OvR) | Log-Loss |
|---|:---:|:---:|:---:|:---:|
| Logistic Regression | 91.53% | 0.9154 | 0.9907 | 0.2182 |
| MLP Neural Network | 93.69% | 0.9369 | 0.9945 | 0.1623 |
| Extra Trees | 94.01% | 0.9401 | 0.9938 | 0.2118 |
| Random Forest | 94.34% | 0.9434 | 0.9952 | 0.1572 |
| **Hist Gradient Boosting** ⭐ | **94.32%** | **0.9433** | **0.9954** | **0.1453** |

### Best Model — Per-Class Breakdown (Hist Gradient Boosting)

| Class | Precision | Recall | F1-Score | Support |
|---|:---:|:---:|:---:|:---:|
| Budget | 0.9690 | 0.9607 | 0.9648 | 2,698 |
| Mid-Low | 0.9244 | 0.9329 | 0.9286 | 2,699 |
| Mid-High | 0.9182 | 0.9254 | 0.9218 | 2,694 |
| Premium | 0.9619 | 0.9537 | 0.9577 | 2,697 |
| **Weighted Avg** | **0.9434** | **0.9432** | **0.9433** | **10,788** |

> **Key observation:** Budget and Premium tiers achieve near-perfect classification (F1 ≥ 0.96). Mid-tier confusion is the primary error source — expected, as Mid-Low/Mid-High share overlapping price ranges and physical characteristics.

---

## 🏗 Pipeline Architecture

```
Diamonds.csv (53,940 × 10)
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  MODULE 1 — EDA & Statistical Validation                    │
│  • Kruskal-Wallis tests (cut, color, clarity vs price)      │
│  • Spearman correlation analysis                            │
│  • QQ plots, KDE overlays, hexbin density maps              │
│  • Distribution dashboards (9-panel)                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  MODULE 2 — Feature Engineering (10 → 26 features)         │
│  • Ordinal encodings for cut, color, clarity                │
│  • Geometry: volume, density, girdle area, symmetry ratios  │
│  • Quality composites: 4C score, pairwise interactions      │
│  • Transforms: log(carat), log(volume), carat², carat×4C   │
│  • Target: 4-class price tier via population quartiles      │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  MODULE 3 — Multi-Model Training (60/20/20 split)           │
│  • Random Forest        (balanced class weights, MDI)       │
│  • Extra Trees          (balanced class weights, MDI)       │
│  • Hist Gradient Boost  (L2 regularisation, depth=6)        │
│  • MLP Neural Network   (Power-transformed input, 256-128)  │
│  • Logistic Regression  (StandardScaler, SAGA solver)       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  MODULE 4 — Evaluation Suite                                │
│  • Normalised + raw count confusion matrices                │
│  • ROC curves (One-vs-Rest per class, AUC annotated)        │
│  • Precision-Recall curves (Average Precision annotated)    │
│  • Reliability / Calibration diagram                        │
│  • Per-class precision, recall, F1 grouped bars             │
│  • Log-loss and comparative metric tables                   │
│  • PCA 2D projection with error overlay                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  MODULE 5 — Explainability (XAI)                            │
│                                                             │
│  Kernel SHAP (from scratch)                                 │
│  ├─ Global importance bar (mean |SHAP| across instances)    │
│  ├─ Per-class SHAP heatmap (top-15 features)                │
│  ├─ Beeswarm plot (feature value vs SHAP value)             │
│  ├─ Waterfall plots (base → prediction decomposition)       │
│  └─ Dependence plots (feature value vs SHAP + interaction)  │
│                                                             │
│  LIME (from scratch)                                        │
│  ├─ 4 representative instances (one per class)              │
│  ├─ Local surrogate (weighted Ridge regression)             │
│  └─ Coefficient charts (true class + predicted class)       │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Feature Engineering

16 features were derived from the 10 raw attributes, falling into four categories:

### Geometry & Physics
| Feature | Formula | Rationale |
|---|---|---|
| `volume` | `x × y × z` | Physical volume proxy (mm³) |
| `density_proxy` | `carat / volume` | Mass-to-volume ratio |
| `girdle_area` | `π × ((x+y)/4)²` | Estimated girdle cross-section |
| `depth_pct_calc` | `z / mean(x,y) × 100` | Independent depth% verification |
| `xy_ratio`, `xz_ratio`, `yz_ratio` | `x/y`, `x/z`, `y/z` | Dimensional symmetry |
| `table_depth_rat` | `table / depth` | Proportionality ratio |

### Quality Composites
| Feature | Formula | Rationale |
|---|---|---|
| `4c_score` | `cut_enc + color_enc + clarity_enc` | Additive quality index |
| `cut_color` | `cut_enc × color_enc` | Pairwise interaction |
| `cut_clarity` | `cut_enc × clarity_enc` | Pairwise interaction |
| `color_clarity` | `color_enc × clarity_enc` | Pairwise interaction |
| `4c_product` | `cut_enc × color_enc × clarity_enc` | 3-way interaction |

### Log & Polynomial Transforms
| Feature | Formula | Rationale |
|---|---|---|
| `log_carat` | `log(1 + carat)` | Linearises skewed carat-price relationship |
| `log_volume` | `log(1 + volume)` | Reduces heteroscedasticity |
| `carat_sq` | `carat²` | Captures quadratic price curvature |
| `carat_x_4c` | `carat × 4c_score` | Cross-feature interaction (top MDI feature: 13.3%) |

---

## 🧠 Explainability (XAI)

Both methods are implemented entirely from scratch using only `numpy` and `sklearn.linear_model.Ridge`. No `shap` or `lime` library is required.

### Kernel SHAP

Based on Lundberg & Lee (2017) — *"A Unified Approach to Interpreting Model Predictions"*.

**Algorithm:**
1. Sample random binary coalitions **z ∈ {0,1}ⁿ**
2. For each coalition, create a perturbed input: keep masked features from the instance, replace others with background mean
3. Collect model predictions for all perturbed inputs
4. Weight each coalition by the Shapley kernel:  
   `w(z) = (n−1) / [C(n,|z|) × |z| × (n−|z|)]`
5. Solve weighted Ridge regression to obtain Shapley coefficients

**Outputs:** Global importance bar · Per-class heatmap · Beeswarm · Waterfall · Dependence plots

### LIME

Based on Ribeiro, Singh & Guestrin (2016) — *"'Why Should I Trust You?': Explaining the Predictions of Any Classifier"*.

**Algorithm:**
1. Generate `n` perturbed samples via Gaussian noise around the instance
2. Get model probability predictions for all perturbed samples
3. Compute exponential kernel weights: `w_i = exp(−d²/2σ²)` where `σ = √n × 0.25`
4. Fit weighted Ridge surrogate per class on normalised feature space
5. Surrogate coefficients = local feature importances

**Outputs:** Coefficient bar charts for true class and predicted class (4 instances, one per tier)

### Top SHAP Drivers

| Rank | Feature | Mean \|SHAP\| | Interpretation |
|---|---|---|---|
| 1 | `carat_x_4c` | Highest | Combined mass-quality interaction dominates |
| 2 | `volume` | High | Physical size strongly determines price tier |
| 3 | `log_carat` | High | Log-transformed weight (linearised signal) |
| 4 | `4c_score` | Medium | Composite 4C quality index |
| 5 | `girdle_area` | Medium | Cross-sectional geometry |

---

## 📊 Statistical Validation

Non-parametric tests were applied prior to modelling to confirm feature significance:

| Test | Variables | Statistic | p-value | Conclusion |
|---|---|:---:|:---:|---|
| Kruskal-Wallis | price ~ cut | H = 978.6 | < 2×10⁻²¹⁰ | Significant |
| Kruskal-Wallis | price ~ color | H = 1335.6 | < 2×10⁻²⁸⁵ | Significant |
| Kruskal-Wallis | price ~ clarity | H = 2718.2 | ≈ 0 | Highly significant |
| Spearman ρ | carat ↔ price | ρ = 0.9629 | ≈ 0 | Near-perfect rank correlation |
| Spearman ρ | volume ↔ price | ρ = 0.9625 | ≈ 0 | Near-perfect rank correlation |

---

## 🚀 Quick Start

### Option A — Google Colab (recommended)

```
1. Open Diamonds_ML_Production.ipynb in Google Colab
2. Runtime → Run All
3. Upload Diamonds.csv when Cell 1 prompts
4. All 13 figures + report auto-save to outputs/
5. Final cell downloads outputs as diamonds_ml_outputs.zip
```

### Option B — Local Jupyter

```bash
# Clone the repository
git clone https://github.com/prithu-sarkar/diamonds-ml-pipeline.git
cd diamonds-ml-pipeline

# Create virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch notebook
jupyter notebook Diamonds_ML_Production.ipynb
```

### Option C — Run pipeline scripts directly

```bash
python pipeline_01_eda.py          # EDA + feature engineering + figs 01–03
python pipeline_02_modeling.py     # Model training + evaluation + figs 04–09
python pipeline_03_xai.py          # SHAP + LIME + figs 10–13
```

---

## 📦 Requirements

```text
numpy>=1.24
pandas>=1.5
scikit-learn>=1.2
matplotlib>=3.7
seaborn>=0.12
scipy>=1.10
```

> **No external XAI libraries needed.** SHAP and LIME are implemented from scratch.

Install with:
```bash
pip install -r requirements.txt
```

---

## 📁 Repository Structure

```
diamonds-ml-pipeline/
│
├── Diamonds_ML_Production.ipynb    # Main Colab notebook (36 cells)
├── Diamonds.csv                    # Source dataset
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── nbstrip.sh                      # Strip notebook metadata before git push
├── .gitattributes                  # Line-ending rules (LF for text, binary for PNG)
├── .gitignore                      # Excludes checkpoints, caches, pickle files
│
├── pipeline_01_eda.py              # Module 1: EDA & feature engineering
├── pipeline_02_modeling.py         # Module 2: Model training & evaluation
│
└── outputs/
    ├── diamonds_engineered.csv          # 53,940 × 26 engineered feature matrix
    ├── fig01_eda_dashboard.png          # 9-panel EDA overview
    ├── fig02_feature_engineering.png    # 12-panel derived feature analysis
    ├── fig03_statistical_qq.png         # QQ plots + skewness/kurtosis
    ├── fig04_model_comparison.png       # 4-metric comparison (Acc, AUC, F1, LogLoss)
    ├── fig05_best_model_deep_eval.png   # Full evaluation dashboard (6 panels)
    ├── fig06_all_cms.png                # All 5 confusion matrices side-by-side
    ├── fig07_pca_errors.png             # PCA projection with error overlay
    ├── fig08_feature_importance.png     # MDI importance (RF, ET, HGB)
    ├── fig09_best_model_deep_eval.png   # Extended evaluation dashboard
    ├── fig10_shap_global.png            # SHAP global bar + heatmap + beeswarm
    ├── fig11_lime_explanations.png      # LIME local surrogate (8 sub-panels)
    ├── fig12_shap_waterfall.png         # SHAP waterfall (4 classes)
    ├── fig13_shap_dependence.png        # SHAP dependence (8 sub-panels)
    ├── granular_report.txt              # Full text ML report
    └── model_summary.json               # Machine-readable metrics
```

---

## 📈 Outputs Reference

| Figure | Description | Panels |
|---|---|:---:|
| `fig01_eda_dashboard.png` | Price KDE, log-price, cut/color/clarity dual-axis, hexbin, boxplot, correlation heatmap, tier pie | 9 |
| `fig02_feature_engineering.png` | Volume vs price, log-carat vs log-price, 4C by tier, violins, correlation bars, scatter | 12 |
| `fig03_statistical_qq.png` | QQ plots for carat, price, depth, table, volume, price-per-carat | 6 |
| `fig04_model_comparison.png` | Accuracy, ROC-AUC, F1, Log-Loss bars across all 5 models | 4 |
| `fig05_best_model_deep_eval.png` | Normalised CM, raw CM, per-class P/R/F1, calibration, ROC, PR | 6 |
| `fig06_all_cms.png` | Normalised confusion matrix for each of the 5 models | 5 |
| `fig07_pca_errors.png` | True labels, predicted labels, error locations in PCA space | 3 |
| `fig08_feature_importance.png` | MDI importance for RF, ET, Hist-GBM | 3 |
| `fig10_shap_global.png` | Global importance bar, per-class heatmap, beeswarm | 3 |
| `fig11_lime_explanations.png` | LIME coefficients (true + predicted class) for 4 instances | 8 |
| `fig12_shap_waterfall.png` | SHAP waterfall decomposition (base → prediction) per class | 4 |
| `fig13_shap_dependence.png` | SHAP value vs feature value + interaction colouring | 8 |

---

## 🔧 Git Hygiene

This repository is configured for clean version control of notebooks and data files.

### Prevent metadata/state-key corruption on push

```bash
# Strip cell outputs and execution counts before committing
bash nbstrip.sh
```

Or manually:
```bash
pip install nbstripout
nbstripout Diamonds_ML_Production.ipynb
git add Diamonds_ML_Production.ipynb
git commit -m "Strip notebook outputs"
```

### `.gitattributes` enforces

- `*.ipynb`, `*.csv`, `*.txt`, `*.json`, `*.py`, `*.md` → `text eol=lf` (LF on all platforms)
- `*.png`, `*.pkl` → `binary` (no line-ending conversion)

### `.gitignore` excludes

```
.ipynb_checkpoints/     ← Jupyter auto-save checkpoints
__pycache__/            ← Python bytecode cache
*.pyc                   ← Compiled Python files
*.pkl                   ← Binary model/data pickles
.DS_Store               ← macOS metadata
```

---

## 📐 Methodology Notes

### Why quartile-based tiers?
Quartile splits produce a **perfectly balanced** 4-class target (≈25% each), eliminating the need for class-weight correction in most models and making all per-class metrics directly comparable without macro/micro ambiguity.

### Why Hist Gradient Boosting over XGBoost/LightGBM?
`HistGradientBoostingClassifier` is part of scikit-learn, requires zero external dependencies, and matches XGBoost/LightGBM performance on this dataset while keeping the pipeline fully self-contained. Its native support for missing values and built-in L2 regularisation also simplify production deployment.

### Why implement SHAP/LIME from scratch?
External `shap` (0.46+) and `lime` libraries have version-pinning conflicts with scikit-learn ≥1.6 as of mid-2025. From-scratch implementations using only `Ridge` regression and `numpy` are fully portable, dependency-free, and educational — the algorithm is transparently visible in the notebook code.

### Model selection criterion
Models are ranked by **weighted ROC-AUC (One-vs-Rest)** rather than accuracy, as AUC is threshold-independent and more informative for multi-class probability calibration quality. Log-loss is reported as a secondary calibration metric.

---

## 🗂 Dataset

The Diamonds dataset is sourced from the `ggplot2` R package and is widely used as a benchmark for regression and classification tasks.

| Attribute | Type | Description |
|---|---|---|
| `carat` | float | Weight of the diamond |
| `cut` | ordinal | Cut quality: Fair / Good / Very Good / Premium / Ideal |
| `color` | ordinal | Diamond colour: D (best) → J (worst) |
| `clarity` | ordinal | Clarity grade: IF (best) → I1 (worst) |
| `depth` | float | Total depth percentage: z / mean(x,y) × 100 |
| `table` | float | Width of top facet relative to widest point |
| `x` | float | Length in mm |
| `y` | float | Width in mm |
| `z` | float | Depth in mm |
| `price` | int | Price in USD ($326 – $18,823) |

---

## 📜 References

1. **Lundberg, S. M., & Lee, S.-I.** (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems*, 30. https://arxiv.org/abs/1705.07874

2. **Ribeiro, M. T., Singh, S., & Guestrin, C.** (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. *KDD 2016*. https://arxiv.org/abs/1602.04938

3. **Pedregosa, F., et al.** (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12, 2825–2830.

4. **Wickham, H.** (2016). ggplot2: Elegant Graphics for Data Analysis. Springer-Verlag. *(Source of the Diamonds dataset)*

---

## 👤 Author

**Prithu Sarkar**

> *Built with precision — because every carat counts.*

---

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025 Prithu Sarkar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

<div align="center">

**💎 diamonds-ml-pipeline** · Made by [Prithu Sarkar](https://github.com/prithu-sarkar)

</div>
