# 🧠 Autism Spectrum Disorder — Multi-Group Comparative Analysis

> A comprehensive, multi-method statistical and machine learning study identifying the most prominent predictive factors of ASD diagnosis across child, adolescent, and adult cohorts.

---

## Overview

This project performs a high-granularity comparative analysis of Autism Spectrum Disorder (ASD) screening data across three distinct age groups using the **AQ-10 (Autism Quotient 10-item)** instrument. The analysis integrates classical statistical testing, machine learning feature importance, logistic regression, and cross-validated classification benchmarking to identify which behavioural and demographic features most strongly predict an ASD diagnosis at each stage of development.

**Total sample:** 1,100 participants across three cohorts  
**Key finding:** The AQ-10 total score is the dominant predictor across all groups (~50–55% RF importance), with *A4: Communication* leading in children, *A5: Imagination* in adolescents, and *A9: Faces/Emotions* in adults.

---

## Datasets

| File | Group | N | ASD+ | ASD Rate |
|------|-------|---|------|----------|
| `Autism_Child_Data.csv` | Children (4–11 yrs) | 292 | 141 | 48.3% |
| `Autism_Adolescent_Data.csv` | Adolescents (12–16 yrs) | 104 | 63 | 60.6% |
| `Autism_Adult_Data.csv` | Adults (18+ yrs) | 704 | 189 | 26.9% |

Each dataset contains 22 variables: 10 binary AQ-10 item scores (A1–A10), an AQ-10 total score, demographic variables (age, gender, ethnicity, country of residence, relation to respondent), and two medical history flags (jaundice at birth, family history of autism). The binary outcome variable `Class/ASD` (YES/NO) is the dependent variable.

> **Note:** Place all three CSV files in the same directory as the notebook before running, or update `DATA_DIR` in Cell 2 to point to your data location.

---

## Project Structure

```
├── ASD_Comprehensive_Analysis.ipynb   # Main analysis notebook (14 phases)
├── Autism_Child_Data.csv              # Child cohort dataset
├── Autism_Adolescent_Data.csv         # Adolescent cohort dataset
├── Autism_Adult_Data.csv              # Adult cohort dataset
├── ASD_Comprehensive_Report.docx      # Full academic report with embedded figures
├── autism_outputs/                    # Auto-generated output directory
│   ├── P1_ASD_distribution_by_group.png
│   ├── P1_age_distribution.png
│   ├── P1_AQ10_score_distribution.png
│   ├── P2_ASD_prevalence_by_group.png
│   ├── P2_AQ10_boxplot_group_ASD.png
│   ├── P3_AQ_item_means_by_group.png
│   ├── P3_AQ_item_delta_heatmap.png
│   ├── P3_AQ_item_positive_rate.png
│   ├── P4_gender_ASD.png
│   ├── P4_jaundice_family_history_ASD.png
│   ├── P4_ethnicity_ASD_rate.png
│   ├── P5_stat_heatmap_AQ_items.png
│   ├── P5_statistical_tests.csv
│   ├── P6_RF_feature_importance_plots.png
│   ├── P6_RF_importance_heatmap.png
│   ├── P6_RF_feature_importance.csv
│   ├── P7_correlation_matrices.png
│   ├── P8_logistic_odds_ratios.png
│   ├── P8_LR_<Group>_odds_ratios.csv  # Per-group logistic regression tables
│   ├── P9_CV_AUC_benchmarking.png
│   ├── P9_ROC_curves.png
│   ├── P9_CV_benchmarking.csv
│   ├── P10_key_findings_summary.png
│   └── P10_summary_table.csv
└── README.md
```

---

## Analytical Pipeline

The notebook is structured into **14 sequential phases**:

| Phase | Description |
|-------|-------------|
| **1** | Environment setup, dependency installation, data loading |
| **2** | Data quality audit — null detection, `?` placeholder handling, class balance |
| **3** | Univariate EDA — ASD distribution, age histograms, AQ-10 score distributions |
| **4** | Cross-group comparative EDA — prevalence rates, AQ-10 boxplots |
| **5** | AQ-10 item-level deep dive — mean scores, delta heatmap, positive response rates |
| **6** | Demographic factor analysis — gender, jaundice, family history, ethnicity |
| **7** | Statistical testing — Chi-Square, Cramér's V, Point-Biserial correlation |
| **8** | Random Forest feature importance — per group and combined |
| **9** | Correlation and multicollinearity analysis |
| **10** | Logistic regression with odds ratios |
| **11** | 5-model cross-validated benchmarking (5-fold stratified, AUC metric) |
| **12** | ROC curve analysis |
| **13** | Key findings summary — numeric table and visual dashboard |
| **14** | Export all outputs and ZIP for download |

All figures and CSV tables are saved to `autism_outputs/` with phase-prefixed filenames (`P1_`, `P2_`, ...) at each stage.

---

## Methods

### Statistical Testing
- **Point-Biserial correlation** — AQ-10 binary items vs. binary ASD outcome
- **Pearson's Chi-Square + Cramér's V** — categorical demographics vs. ASD status
- Significance threshold: α = 0.05

### Machine Learning
- **Random Forest** (300 trees, balanced class weights) — Gini MDI feature importance
- **Gradient Boosting** — cross-validation benchmarking
- **Logistic Regression** — odds ratios via `statsmodels.Logit`
- **SVM (RBF kernel)** and **KNN** — comparative benchmarking
- **5-fold stratified cross-validation** with ROC-AUC as the primary metric
- All features standardised (StandardScaler) prior to model fitting

### Key Features Analysed
- `A1`–`A10`: Binary AQ-10 item scores
- `result`: AQ-10 total score (0–10)
- `age`, `gender`, `ethnicity`
- `jundice`: Born with jaundice (yes/no)
- `austim`: Family member with autism (yes/no)
- `used_app_before`: Prior use of AQ-10 app (yes/no)

---

## Key Results

### ASD Prevalence
| Group | N | ASD Rate | Mean AQ-10 (ASD+) | Mean AQ-10 (ASD−) |
|-------|---|----------|-------------------|-------------------|
| Child | 292 | 48.3% | 8.21 | 4.40 |
| Adolescent | 104 | 60.6% | 8.19 | 4.46 |
| Adult | 704 | 26.9% | 8.26 | 3.63 |

### Top Predictive Features by Group

| Group | Rank 1 | Rank 2 | Rank 3 |
|-------|--------|--------|--------|
| **Child** | A4: Communication (r = 0.569) | A9: Faces/Emotions (r = 0.486) | A10: Other Minds (r = 0.440) |
| **Adolescent** | A5: Imagination (r = 0.534) | A4: Communication (r = 0.507) | A3: Attention to Detail (r = 0.488) |
| **Adult** | A9: Faces/Emotions (r = 0.636) | A6: Social Situations (r = 0.592) | A5: Imagination (r = 0.537) |

*All reported r values are Point-Biserial correlations, p < 0.001.*

### Classification Performance (5-Fold CV AUC)

| Model | Child | Adolescent | Adult | Combined |
|-------|-------|-----------|-------|----------|
| Logistic Regression | 1.000 | 0.996 | 1.000 | 1.000 |
| Random Forest | 1.000 | 1.000 | 1.000 | 1.000 |
| Gradient Boosting | 1.000 | 1.000 | 1.000 | 1.000 |
| SVM (RBF) | 0.997 | 0.983 | 0.999 | 1.000 |
| KNN | 0.968 | 0.954 | 0.991 | 0.991 |

> High AUC values are expected given that the AQ-10 total score (a composite of the item scores) is included in the feature set. See the Limitations section of the report for a full discussion.

---

## Requirements

```
python >= 3.9
pandas
numpy
matplotlib
seaborn
scipy
scikit-learn
statsmodels
shap
openpyxl
```

Install all dependencies:

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn statsmodels shap openpyxl
```

---

## Usage

1. Clone the repository and navigate to the project folder:
   ```bash
   git clone https://github.com/<your-username>/asd-multigroup-analysis.git
   cd asd-multigroup-analysis
   ```

2. Place the three dataset CSVs in the project root (or update `DATA_DIR` in Cell 2 of the notebook).

3. Launch the notebook:
   ```bash
   jupyter notebook ASD_Comprehensive_Analysis.ipynb
   ```

4. Run all cells in order. All outputs are saved to `autism_outputs/`. The final cell zips and packages all outputs for download.

---

## Outputs

Running the full notebook produces:
- **19 publication-quality figures** (PNG, 130 DPI) covering all analytical phases
- **5 CSV tables** with numeric results (statistical tests, RF importance, CV benchmarking, summary)
- **1 ZIP archive** containing all of the above, timestamped for reproducibility
- **1 Word document report** (`ASD_Comprehensive_Report.docx`) — full academic write-up with embedded figures, tables, odds ratios, and clinical recommendations (~35 pages)

---

## Limitations

- Datasets are **screening convenience samples**, not population-representative cohorts. Adolescent ASD prevalence (60.6%) likely reflects referral bias.
- Including both the AQ-10 **total score and individual items** in the same model creates information redundancy, inflating classification AUC. Item-only models yield more conservative but still strong estimates.
- The adolescent sample (n = 104) is **underpowered** relative to the other cohorts.
- Ethnic subgroup analyses are limited by small cell sizes in the child and adolescent datasets.
- This is a **cross-sectional study**; developmental trends cannot be inferred causally from cross-cohort comparisons.

---

## Citation

If you use this analysis or the methodology described here, please cite appropriately and reference the original AQ-10 instrument:

> Baron-Cohen, S., Wheelwright, S., Skinner, R., Martin, J., & Clubley, E. (2001). The Autism-Spectrum Quotient (AQ): Evidence from Asperger Syndrome/High-Functioning Autism, Males and Females, Scientists and Mathematicians. *Journal of Autism and Developmental Disorders, 31*(1), 5–17.

---

## License

This project is released for research and educational use. Dataset licensing terms apply as per the original data source. Please verify dataset terms before redistribution.
