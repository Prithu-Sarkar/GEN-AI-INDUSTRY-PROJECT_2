<div align="center">

# ☀️ Solar Energy Worldwide — End-to-End Analytics Pipeline

**A production-grade data science project delivering elite analytical depth across 48 global cities**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.x-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![MLflow](https://img.shields.io/badge/MLflow-Tracked-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org)
[![DagsHub](https://img.shields.io/badge/DagsHub-Integrated-FF6B35?style=for-the-badge)](https://dagshub.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

---

*Audit · EDA · Feature Engineering · Segmentation · Business Intelligence · Experiment Tracking*

</div>

---

## 📌 Project Overview

This project delivers a **comprehensive, end-to-end analytics pipeline** on a global solar energy dataset spanning **48 cities**, **30 countries**, and **7 continental regions**. Every stage — from raw data ingestion to executive-ready business insights — is implemented with modular, reusable, production-quality code.

The pipeline is structured to answer three core business questions:

> **1.** Where in the world does solar investment generate the highest return?  
> **2.** Which city and regional clusters represent the strongest deployment opportunities?  
> **3.** What financial, environmental, and operational signals should guide solar infrastructure strategy?

---

## 🗂️ Repository Structure

```
solar-energy-analytics/
│
├── Solar_Energy_Analytics_FAANG.ipynb     ← Main analytics notebook
├── solar_energy_worldwide.csv             ← Raw dataset (48 cities × 17 features)
├── Column_Definitions.xlsx                ← Feature schema & business definitions
├── README.md                              ← This file
│
└── solar_analytics_outputs/
    ├── 01_charts/                         ← All publication-grade visualisations
    │   ├── executive_dashboard.png
    │   ├── geo_bubble_map.png / .html / .svg
    │   ├── correlation_matrix.png
    │   ├── univariate_distribution_gallery.png
    │   ├── bivariate_scatter_matrix.png
    │   ├── region_segment_boxplots.png
    │   ├── pca_cluster_visualisation.png
    │   ├── kmeans_elbow_silhouette.png
    │   ├── regional_opportunity_matrix.png / .html / .svg
    │   ├── engineered_features_analysis.png
    │   ├── vif_multicollinearity.png
    │   ├── audit_dqs_dashboard.png
    │   └── target_correlation_bars.png
    │
    ├── 02_tables/                         ← Structured analytical tables (CSV)
    │   ├── schema_intelligence.csv
    │   ├── missing_diagnostics.csv
    │   ├── type_optimisation.csv
    │   ├── outlier_framework.csv
    │   ├── city_rankings.csv
    │   ├── cluster_profiles.csv
    │   ├── regional_opportunity_matrix.csv
    │   └── vif_report.csv
    │
    ├── 03_reports/                        ← Analytical reports
    │   ├── data_quality_score.csv
    │   └── strategic_insight_report.md
    │
    ├── 04_processed_datasets/             ← Feature-engineered dataset
    │   └── solar_engineered_features.csv
    │
    └── 05_insights/                       ← Machine-readable insight exports
        └── strategic_insights.json
```

---

## 📊 Dataset at a Glance

| Attribute | Value |
|-----------|-------|
| **Cities** | 48 |
| **Countries** | 30 |
| **Regions** | 7 (North America, Europe, Asia, Africa, Middle East, Oceania, South America) |
| **Features** | 17 raw → 30+ engineered |
| **Data Quality Score** | **99.7 / 100 — Grade A** |
| **Missing Values** | Zero |
| **Duplicates** | Zero |

### Feature Taxonomy

| Category | Columns |
|----------|---------|
| **Geographic** | City, Country, Latitude, Longitude, Region |
| **Solar Resource** | Annual_Sunlight_Hours, Daily_Peak_Sun_Hours, GHI_kWh_per_m2 |
| **Economic** | Electricity_Price_USD_per_kWh, Avg_System_Cost_USD |
| **Market** | Solar_Installations_Count |
| **Output** | Avg_Annual_Production_kWh |
| **Financial** | Estimated_Annual_Savings_USD, Payback_Period_Years, ROI_Percentage |
| **Environmental** | CO2_Reduction_Tons_per_Year |
| **Target** | Solar_Viability_Score |

---

## 🔬 Pipeline Architecture

The notebook is organised into **11 self-contained, modular sections**:

```
┌──────────────────────────────────────────────────────────────────┐
│  0  Secrets & Environment Configuration (MongoDB, MLflow/DagsHub)│
├──────────────────────────────────────────────────────────────────┤
│  1  Dependency Installation & Aesthetic Configuration            │
├──────────────────────────────────────────────────────────────────┤
│  2  Output Directory Architecture (auto-created, auto-zipped)    │
├──────────────────────────────────────────────────────────────────┤
│  3  Data Loading & Schema Intelligence                           │
├──────────────────────────────────────────────────────────────────┤
│  4  Deep Data Auditing  ←  DataAuditor class                     │
│     · Missing value diagnostics  · Type optimisation             │
│     · Duplicate analysis         · IQR + Z-score outliers        │
│     · Composite Data Quality Score (DQS)                         │
├──────────────────────────────────────────────────────────────────┤
│  5  Advanced EDA                                                 │
│     · Univariate KDE gallery     · Correlation heatmap           │
│     · Bivariate scatter matrix   · Kruskal-Wallis segment tests  │
│     · Geospatial bubble map (interactive HTML + static PNG)      │
├──────────────────────────────────────────────────────────────────┤
│  6  Feature Engineering  ←  FeatureEngineer class                │
│     · Resource efficiency ratios · Financial KPI tiers           │
│     · Market scale signals       · Label encoding + scaling      │
│     · K-Means segmentation (auto-K via silhouette)               │
│     · PCA 2D cluster visualisation                               │
│     · VIF multicollinearity diagnostics                          │
├──────────────────────────────────────────────────────────────────┤
│  7  Business & Consumer Insights                                 │
│     · Multi-KPI city leaderboards  · Regional opportunity matrix │
│     · Investment quadrant analysis · ESG impact quantification   │
├──────────────────────────────────────────────────────────────────┤
│  8  MLflow Experiment Tracking (DagsHub)                         │
├──────────────────────────────────────────────────────────────────┤
│  9  Executive Dashboard (6-panel publication-grade summary)      │
├──────────────────────────────────────────────────────────────────┤
│  10 Strategic Insight Report (JSON + Markdown export)            │
├──────────────────────────────────────────────────────────────────┤
│  11 Auto-Zip & Download All Outputs                              │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Key Analytical Modules

### `DataAuditor` — Reusable Data Quality Engine

```python
auditor = DataAuditor(df)
miss_df, type_df, dup_dict, out_df, dqs_dict = auditor.full_audit()
```

Produces a **Composite Data Quality Score (DQS)** weighted across four dimensions:

| Dimension | Weight | Score |
|-----------|--------|-------|
| Completeness | 35% | 100.0 |
| Uniqueness | 25% | 100.0 |
| Consistency | 20% | 100.0 |
| Validity (outlier-adjusted) | 20% | 99.0 |
| **Composite DQS** | — | **99.7 / 100 [A]** |

---

### `FeatureEngineer` — Modular Transformation Pipeline

```python
fe = FeatureEngineer(df)
df_eng = fe.engineer_all()
```

Generates **13+ derived features** across four strategic categories:

- **Solar Resource:** GHI Efficiency Ratio, Peak Hour Concentration, Effective Daily kWh, Hemisphere flag
- **Financial:** Cost per kWh Produced, Savings Yield %, Savings per CO₂ Ton, Payback Tier, ROI Band
- **Market:** Log-transformed Installations, Viability Tier, CO₂ per MWh
- **ML-Ready:** Label-encoded categoricals, StandardScaler-normalised numeric features

---

### K-Means City Segmentation

Optimal cluster count selected automatically via **silhouette score maximisation**. Cities are segmented into strategic groups for targeted investment and policy recommendations:

| Cluster | Avg GHI | Avg ROI | Avg Payback | Avg Viability | Profile |
|---------|---------|---------|-------------|---------------|---------|
| **0** | 5.19 kWh/m² | 12.5% | 8.1 yrs | 61.0 | ✅ High-Performing |
| **1** | 3.44 kWh/m² | 8.1% | 12.5 yrs | 43.7 | ⚠️ Development Markets |

---

## 📈 Key Findings

### 🏆 Top Markets by Solar Viability Score

| Rank | City | Country | Viability Score | ROI | Payback |
|------|------|---------|----------------|-----|---------|
| 1 | **Phoenix** | United States | 73 | 17.2% | 5.8 yrs |
| 2 | **Dubai** | UAE | 70 | 15.9% | 6.3 yrs |
| 3 | **Cairo** | Egypt | 68 | 15.4% | 6.5 yrs |
| 4 | **Tel Aviv** | Israel | 67 | 14.5% | 6.9 yrs |
| 5 | **Los Angeles** | United States | 67 | 14.5% | 6.9 yrs |

### 🌍 Regional Opportunity Matrix

| Region | Avg Viability | Avg ROI | Avg Payback | Total Installs |
|--------|--------------|---------|-------------|----------------|
| **Middle East** | 67.0 | 14.5% | 6.9 yrs | 920 |
| **Africa** | 66.3 | 14.3% | 7.0 yrs | 3,850 |
| **Oceania** | 60.0 | 12.2% | 8.3 yrs | 26,700 |
| **North America** | 58.1 | 12.0% | 8.7 yrs | 718,200 |
| **Asia** | 57.3 | 11.4% | 9.0 yrs | 1,469,100 |
| **South America** | 56.0 | 10.5% | 9.7 yrs | 12,170 |
| **Europe** | 46.1 | 8.9% | 11.9 yrs | 97,600 |

### 💰 Global Financial Benchmarks

| KPI | Value |
|-----|-------|
| Average ROI | **10.86%** |
| Average Payback Period | **9.78 years** |
| Average Annual Savings | **$1,627.73 / installation** |
| Total CO₂ Offset (48 cities) | **208.35 metric tons / year** |

---

## 💡 Strategic Recommendations

| Priority | Recommendation |
|----------|----------------|
| 🌟 **#1 Target Market** | Phoenix leads all metrics — highest viability (73), fastest payback (5.8 yrs), greatest CO₂ impact (6.84 t/yr). First-mover investment is strongly warranted. |
| 🌍 **Regional Scale-Up** | Middle East and Africa offer the highest avg ROI (14.5% and 14.3%) with minimal market saturation — prime greenfield expansion territories. |
| ⚡ **Investor-Grade Markets** | Cities with sub-7-year payback (Phoenix, Dubai, Cairo) are ideal for institutional capital seeking predictable infrastructure returns. |
| ⚠️ **Development Zone** | Europe's avg viability (46.1) and 11.9-year payback reflect high system costs relative to irradiance. Policy subsidy modelling required before deployment decisions. |
| 🌱 **ESG Value Proposition** | 208+ metric tons of annual CO₂ offset across the portfolio constitutes a quantifiable, auditable sustainability credential for ESG-mandated funds. |
| 🔗 **Modelling Advisory** | GHI, Daily Peak Hours, and Annual Production exhibit high multicollinearity (VIF > 10). Regularised regression (Ridge / Lasso / ElasticNet) is mandatory for predictive modelling tasks. |

---

## 📦 Outputs Reference

### Charts (`01_charts/`)

| File | Description |
|------|-------------|
| `executive_dashboard.png` | 6-panel dark-theme C-suite summary |
| `geo_bubble_map.png / .html` | Interactive geospatial viability map |
| `univariate_distribution_gallery.png` | KDE + histogram for all 14 numeric features |
| `correlation_matrix.png` | Full Pearson heatmap |
| `bivariate_scatter_matrix.png` | 4 key pairwise scatter plots with regression lines |
| `region_segment_boxplots.png` | Kruskal-Wallis regional KPI distributions |
| `pca_cluster_visualisation.png` | 2D PCA city segmentation map |
| `kmeans_elbow_silhouette.png` | Elbow + silhouette for optimal K selection |
| `regional_opportunity_matrix.png / .html` | ROI × Viability bubble chart by region |
| `vif_multicollinearity.png` | Variance Inflation Factor diagnostic |
| `audit_dqs_dashboard.png` | Data quality score components |
| `target_correlation_bars.png` | Feature correlations with Solar Viability Score |

### Tables (`02_tables/`)

| File | Description |
|------|-------------|
| `schema_intelligence.csv` | Column roles, types, and business definitions |
| `city_rankings.csv` | Top-10 cities across 6 KPI dimensions |
| `regional_opportunity_matrix.csv` | Region-aggregated strategic metrics |
| `cluster_profiles.csv` | K-Means cluster centroids and feature means |
| `outlier_framework.csv` | IQR + Z-score outlier exposure per column |
| `vif_report.csv` | VIF scores for multicollinearity assessment |

---

## ⚙️ Technical Stack

| Layer | Technology |
|-------|-----------|
| **Data Manipulation** | pandas, NumPy |
| **Statistics** | SciPy, statsmodels |
| **Machine Learning** | scikit-learn (KMeans, PCA, StandardScaler, VIF) |
| **Visualisation** | matplotlib, seaborn, Plotly |
| **Experiment Tracking** | MLflow + DagsHub |
| **Database** | MongoDB (via PyMongo) |
| **Environment** | Python 3.10+ |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/solar-energy-analytics.git
cd solar-energy-analytics
```

### 2. Install dependencies

```bash
pip install pandas numpy scipy statsmodels scikit-learn matplotlib seaborn \
            plotly mlflow dagshub pymongo missingno
```

### 3. Configure secrets

Set the following environment variables (or use your secrets manager):

```bash
export MONGO_DB_URL="your_mongodb_connection_string"
export MLFLOW_TRACKING_URI="your_dagshub_mlflow_uri"
export MLFLOW_TRACKING_USERNAME="your_dagshub_username"
export MLFLOW_TRACKING_PASSWORD="your_dagshub_token"
```

### 4. Add your data

Place `solar_energy_worldwide.csv` in the project root.

### 5. Run the notebook

```bash
jupyter notebook Solar_Energy_Analytics_FAANG.ipynb
```

All outputs are automatically saved to `solar_analytics_outputs/` and zipped for download at the end of the run.

---

## 🔁 Reproducibility

- Global random seed fixed at `np.random.seed(42)` throughout
- All parameters, metrics, and artifacts logged to MLflow for full experiment auditability
- Pipeline is fully stateless — re-running from scratch produces identical outputs
- Engineered dataset (`solar_engineered_features.csv`) is exported at each run for downstream use

---

## 📄 License

This project is released under the [MIT License](LICENSE). You are free to use, adapt, and distribute with attribution.

---

<div align="center">

**Built with analytical rigour. Designed for decision-makers.**

*Data Quality Score: 99.7/100 · 48 Cities · 30 Countries · 7 Regions · 208 tCO₂/yr offset potential*

</div>
