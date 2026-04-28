# Telecom Customer Churn Analysis — EDA

> A structured, industry-standard Exploratory Data Analysis (EDA) pipeline for diagnosing customer churn in a telecom dataset. Produces publication-ready visualisations, statistical reports, and a model-ready encoded dataset — all packaged into a single ZIP export.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Analysis Pipeline](#analysis-pipeline)
- [Key Findings](#key-findings)
- [Outputs](#outputs)
- [Getting Started](#getting-started)
- [Running on Google Colab](#running-on-google-colab)
- [Dependencies](#dependencies)
- [Notebook Standards](#notebook-standards)
- [Next Steps](#next-steps)
- [License](#license)

---

## Project Overview

Customer churn — the rate at which customers stop doing business with a company — is one of the most critical KPIs in subscription-based industries. This project performs a comprehensive EDA on a telecom churn dataset to:

- Profile data quality and identify cleaning requirements
- Understand the distribution of the target variable and class imbalance
- Quantify how each feature (demographic, service, billing) relates to churn
- Derive actionable business insights to inform retention strategy
- Produce a clean, encoded dataset ready for downstream machine learning

---

## Dataset

| Property | Value |
|---|---|
| **File** | `Customer-Churn.csv` |
| **Rows** | ~7,043 customers |
| **Columns** | 21 features + 1 target |
| **Target** | `Churn` (Yes / No) |
| **Source** | IBM Sample Telecom Dataset |

**Feature categories:**

- **Demographics** — `gender`, `SeniorCitizen`, `Partner`, `Dependents`
- **Account info** — `tenure`, `Contract`, `PaperlessBilling`, `PaymentMethod`
- **Services** — `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`
- **Billing** — `MonthlyCharges`, `TotalCharges`

---

## Project Structure

```
churn-analysis-eda/
│
├── Churn_Analysis_Industry_Standard.ipynb   # Main analysis notebook
├── Customer-Churn.csv                        # Raw dataset (upload manually in Colab)
├── README.md                                 # This file
│
└── churn_eda_outputs/                        # Auto-generated on notebook run
    ├── images/
    │   ├── 03a_missing_matrix.png
    │   ├── 05_target_distribution.png
    │   ├── 06_univariate_cat_group*.png
    │   ├── 06_numeric_distributions.png
    │   ├── 07_bivariate_stacked_pct.png
    │   ├── 07_bivariate_crosstab_heatmaps.png
    │   ├── 07_scatter_charges_churn.png
    │   ├── 07_violin_numeric_churn.png
    │   ├── 08_churn_correlation_bar.png
    │   ├── 08_correlation_heatmap.png
    │   ├── 09_kde_charges_churn.png
    │   ├── 09_tenure_vs_charges_risk.png
    │   └── 10_top15_churn_rates.png
    │
    ├── data/
    │   ├── 01_raw_data.csv
    │   ├── 04_cleaned_data.csv
    │   ├── 08_encoded_data.csv
    │   └── 11_model_ready_encoded.csv
    │
    └── reports/
        ├── 03_numeric_stats.csv
        ├── 03_categorical_stats.csv
        ├── 03_cardinality.csv
        ├── 06_churn_rate_by_category.csv
        ├── 06_ttest_results.csv
        ├── 08_churn_correlations.csv
        ├── 10_key_metrics.json
        └── 10_business_summary.txt
```

---

## Analysis Pipeline

The notebook is organised into 11 sequential phases, each saving its outputs before proceeding.

| Phase | Section | Description |
|---|---|---|
| 1 | Environment Setup | Install dependencies, configure plot styles, create output directories |
| 2 | Data Ingestion | Load CSV, initial peek, save raw snapshot |
| 3 | Data Profiling & Quality | Schema audit, descriptive stats, missing value matrix, cardinality report |
| 4 | Data Cleaning & Feature Engineering | Fix dtypes, drop nulls, encode target, create tenure bands and charge tiers |
| 5 | Target Variable Analysis | Class distribution, imbalance ratio, 3-panel distribution chart |
| 6 | Univariate Analysis | Countplots per categorical feature, histograms + boxplots for numerics, Welch's t-tests |
| 7 | Bivariate Analysis | Stacked % bars, crosstab heatmaps, scatter plots, violin plots |
| 8 | Correlation Analysis | Pearson correlation bar chart, triangular heatmap of top 20 features |
| 9 | KDE Analysis | Charge density by churn, tenure × charges risk-quadrant scatter |
| 10 | Business Insights | Key metric computation, top-15 churn rate chart, written summary |
| 11 | Export & ZIP | Package all images, CSVs, and JSON reports into a timestamped ZIP |

---

## Key Findings

| Driver | Observation |
|---|---|
| **Contract type** | Month-to-month customers churn at ~42% vs ~11% for two-year contracts |
| **Payment method** | Electronic check users have the highest churn rate (~45%) |
| **Tenure** | First-year customers (1–12 months) are the most vulnerable cohort |
| **Monthly charges** | High monthly spend combined with short tenure is the strongest churn signal |
| **Online Security / Tech Support** | Customers without these services churn at significantly higher rates |
| **Senior citizens** | Churn rate ~42% vs ~26% for non-seniors |
| **Gender / Phone Service** | Minimal churn differentiation — low-priority features for modelling |

---

## Outputs

Running the notebook end-to-end generates:

- **13 PNG charts** — saved at 150 DPI, white background, ready for reports
- **4 CSV data files** — from raw snapshot through to model-ready one-hot-encoded data
- **6 CSV reports** — descriptive stats, cardinality, churn rates, t-test results, correlations
- **1 JSON file** — key business metrics (churn rates by contract, payment, tenure, LTV)
- **1 TXT file** — written business summary
- **1 ZIP archive** — timestamped, containing all of the above

---

## Getting Started

### Local (Jupyter / VS Code)

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/churn-analysis-eda.git
cd churn-analysis-eda

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Place the dataset in the project root
#    → Customer-Churn.csv

# 5. Launch the notebook
jupyter notebook Churn_Analysis_Industry_Standard.ipynb
```

### `requirements.txt`

```
numpy>=1.24
pandas>=2.0
matplotlib>=3.7
seaborn>=0.12
missingno>=0.5
scipy>=1.11
phik>=0.12
statsmodels>=0.14
ipykernel>=6.0
```

---

## Running on Google Colab

1. Open [Google Colab](https://colab.research.google.com/) and upload `Churn_Analysis_Industry_Standard.ipynb`
2. In the **Files** panel (left sidebar), upload `Customer-Churn.csv`
3. Run all cells — **Runtime → Run all**
4. The final cell triggers a browser download of the ZIP archive automatically

> **Note:** Colab resets the file system on session end. Download the ZIP before closing.

---

## Dependencies

| Library | Purpose |
|---|---|
| `pandas` | Data manipulation and aggregation |
| `numpy` | Numerical operations |
| `matplotlib` | Base plotting engine |
| `seaborn` | Statistical visualisations |
| `missingno` | Missing value matrix visualisation |
| `scipy` | Welch's t-test, Pearson correlation |
| `phik` | Phi-K correlation for mixed-type features |
| `statsmodels` | Extended statistical support |

All packages install automatically via the first notebook cell if not already present.

---

## Notebook Standards

This notebook follows these conventions to ensure clean version control and reproducibility:

- **Stable cell IDs** — every cell has a fixed UUID; Git diffs are clean and meaningful
- **No output state in VCS** — run `jupyter nbconvert --clear-output` before committing, or use `nbstripout` as a pre-commit hook
- **Correct `nbformat`** — set to `4/5` with full kernelspec metadata; never shows as "invalid" in GitHub
- **Deterministic results** — `np.random.seed(42)` set globally
- **Working copy discipline** — `raw_df` is never mutated; all transformations operate on `df = raw_df.copy()`
- **Incremental saves** — each phase writes its outputs before the next phase begins

### Recommended `.gitignore` entries

```gitignore
# Notebook checkpoints
.ipynb_checkpoints/

# Generated outputs (regenerate by running the notebook)
churn_eda_outputs/
*.zip

# Virtual environment
venv/
__pycache__/
*.pyc

# OS
.DS_Store
Thumbs.db
```

### Recommended pre-commit hook (`nbstripout`)

```bash
pip install nbstripout
nbstripout --install          # strips outputs automatically on every git commit
```

---

## Next Steps

This EDA is designed as the foundation for a full churn prediction pipeline:

1. **Address class imbalance** — apply SMOTE or use `class_weight='balanced'` in models
2. **Feature selection** — use the Pearson and Phi-K correlation results to prune low-signal columns
3. **Baseline modelling** — Logistic Regression and Decision Tree as interpretable starting points
4. **Advanced modelling** — XGBoost / LightGBM for performance; SHAP for explainability
5. **Retention strategy** — target month-to-month customers in their first 12 months with long-term contract incentives; investigate electronic check payment friction

---

## License

This project is licensed under the [MIT License](LICENSE).

---

*Analysis performed on IBM Telecom Sample Dataset. All outputs are reproducible by running the notebook with the original CSV.*
