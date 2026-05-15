<div align="center">

<br/>

```
 █████╗ ██╗    ██╗   ██╗███████╗    ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗
██╔══██╗██║    ██║   ██║██╔════╝    ██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║
███████║██║    ██║   ██║███████╗    ███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║
██╔══██║██║    ╚██╗ ██╔╝╚════██║    ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║
██║  ██║██║     ╚████╔╝ ███████║    ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║
╚═╝  ╚═╝╚═╝      ╚═══╝  ╚══════╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
```

### **TEXT CLASSIFICATION · PIPELINE 2026**
*Distinguishing Machine Intelligence from Human Expression*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MLflow](https://img.shields.io/badge/MLflow-2.12%2B-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.6%2B-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-FF6600?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-FF0066?style=for-the-badge)](https://shap.readthedocs.io)
[![DagsHub](https://img.shields.io/badge/DagsHub-Tracking-FF6B35?style=for-the-badge)](https://dagshub.com)

<br/>

```
┌─────────────────────────────────────────────────────────────────────────┐
│   2,000 Labelled Samples  ·  3 Domains  ·  2 AI Models  ·  11 Features  │
│          GPT-4o  ·  Gemini-2.0  ·  Academic  ·  News  ·  Social         │
└─────────────────────────────────────────────────────────────────────────┘
```

</div>

---

## ◈ Table of Contents

```
  01 · Overview ...................... What this project does & why it matters
  02 · Dataset Architecture ......... Structure, domains, class distribution
  03 · Pipeline Stages .............. All 16 stages in sequence
  04 · Feature Engineering .......... 11 stylometric signals explained
  05 · Statistical Methodology ....... Mann-Whitney U & effect sizes
  06 · Classification Baseline ....... LR, Random Forest, XGBoost + SHAP
  07 · Experiment Tracking ........... MLflow & DagsHub integration
  08 · Data Persistence .............. MongoDB logging architecture
  09 · Output Artefacts .............. What gets saved and where
  10 · Project Structure ............. Directory layout
  11 · Installation .................. Setup & environment configuration
  12 · Configuration Reference ....... Environment variables
  13 · Running the Pipeline .......... Step-by-step execution guide
  14 · Results & Key Findings ........ Distilled analytical insights
  15 · Reproducibility ............... Audit trail & versioning guarantees
  16 · Roadmap ....................... Future development directions
  17 · Citation ...................... How to reference this work
  18 · License ....................... Usage terms
```

---

## 01 · Overview

<div align="center">

> *"As large language models grow increasingly fluent, the boundary between*
> *human and machine expression becomes one of the most consequential*
> *frontiers in applied NLP research."*

</div>

This repository presents a **production-grade, end-to-end machine learning pipeline** for AI-generated text detection, built on rigorous stylometric feature engineering and interpretable classification models. The pipeline is designed for researchers, ML engineers, and practitioners who require reproducible, auditable, and scalable text classification workflows.

### What this project delivers:

| Capability | Detail |
|---|---|
| **Stylometric Analysis** | 11 hand-crafted features spanning surface, lexical, vocabulary, and readability dimensions |
| **Statistical Rigour** | Non-parametric Mann-Whitney U tests with rank-biserial effect sizes |
| **Interpretable ML** | SHAP (SHapley Additive exPlanations) attributions for every model |
| **Full Experiment Tracking** | Nested MLflow runs with DagsHub remote backend support |
| **Persistent Logging** | MongoDB document store with SHA-256 fingerprinted audit records |
| **Portable Outputs** | All artefacts — models, figures, data — bundled into a single ZIP archive |

---

## 02 · Dataset Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ai_vs_human_text_2026.csv                                                   │
│                                                                              │
│  Rows: 2,000    Columns: 9    Avg. text length: ~37 words                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LABEL DISTRIBUTION          DOMAIN BREAKDOWN         SOURCE MODELS          │
│  ─────────────────────       ─────────────────────    ──────────────────     │
│  Human   ████████░  1,334    Academic  ███░  ~667     GPT-4o     ███  333    │
│  AI      ████░       666     News      ███░  ~667     Gemini-2.0 ███  333    │
│                              Social    ███░  ~667                            │
│                                                                              │
│  Class Imbalance Ratio: 2.00:1  (human : ai)                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Column Schema

| Column | Type | Description |
|---|---|---|
| `text_id` | `str` | Unique identifier (e.g. `TXT_0001`) |
| `label` | `str` | Ground truth: `human` or `ai` |
| `source_model` | `str` | `gpt-4o`, `gemini-2.0`, or `human` |
| `domain` | `str` | `academic`, `news`, or `social` |
| `text_content` | `str` | Raw text sample |
| `topic_hint` | `str` | Topic category for context |
| `word_count` | `int` | Pre-computed word count (19–52 range) |
| `avg_sentence_length` | `float` | Pre-computed average sentence length |
| `generation_method` | `str` | `template+human_variation` or `style_simulation` |

### Known Limitations

- **Class imbalance** — 2:1 ratio (human:AI) requires `class_weight='balanced'` or oversampling strategies
- **Short texts** — 19–52 word range; optimised for sentence-level detection tasks
- **Domain scope** — Three domains only; generalisation to other genres requires re-validation

---

## 03 · Pipeline Stages

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PIPELINE EXECUTION SEQUENCE                              ║
╠══════╦═══════════════════════════════════════════════════════════════════════╣
║  S1  ║  Environment Bootstrap & Secret Injection                            ║
║  S2  ║  Dependency Installation & Import Validation                         ║
║  S3  ║  MongoDB Connection & Collection Setup                               ║
║  S4  ║  MLflow / DagsHub Experiment Tracking Initialisation                 ║
║  S5  ║  Data Ingestion, Schema Validation & Quality Gate                    ║
║  S6  ║  Exploratory Data Analysis — Class & Domain Balance                  ║
║  S7  ║  Feature Engineering — 11 Stylometric Signals                        ║
║  S8  ║  Statistical Analysis — Mann-Whitney U & Effect Sizes                ║
║  S9  ║  Visual Analysis — KDE Distributions, Violin & Radar Charts          ║
║  S10 ║  Readability Deep-Dive — Flesch RE & Gunning Fog                     ║
║  S11 ║  AI Model Comparison — GPT-4o vs Gemini-2.0                          ║
║  S12 ║  Feature Correlation & Discriminative Power                          ║
║  S13 ║  Baseline Classification — LR, Random Forest & XGBoost               ║
║  S14 ║  Results Logging → MongoDB + MLflow Artefacts                        ║
║  S15 ║  Output Bundle — CSV, PNG, Pickles → ZIP Archive                     ║
║  S16 ║  Executive Summary & Key Findings                                    ║
╚══════╩═══════════════════════════════════════════════════════════════════════╝
```

---

## 04 · Feature Engineering

All 11 features are computed in **pure Python** using only the standard library and regex — no heavy NLP dependencies, no tokeniser downloads, no GPU required.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  FEATURE TAXONOMY                                                            │
├──────────────────────────┬──────────────────────────────────────────────────┤
│  CATEGORY                │  FEATURES                                        │
├──────────────────────────┼──────────────────────────────────────────────────┤
│  Surface                 │  n_sentences · avg_sent_len                      │
│  Lexical Diversity       │  ttr (Type-Token Ratio) · hapax_ratio            │
│  Vocabulary Richness     │  avg_word_length · avg_syllables · long_word_ratio│
│  POS Proxies             │  func_word_ratio · punct_density                 │
│  Readability Indices     │  flesch_re · gunning_fog                         │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### Feature Definitions

| Feature | Formula / Logic | Interpretation |
|---|---|---|
| `n_sentences` | Count of sentences split on `[.!?]+` | Structural complexity |
| `avg_sent_len` | `word_count / n_sentences` | Sentence density |
| `ttr` | `unique_words / total_words` | Vocabulary diversity |
| `hapax_ratio` | `words_appearing_once / total_words` | Lexical novelty |
| `avg_word_length` | `sum(len(w)) / n_words` | Morphological complexity |
| `avg_syllables` | Rule-based vowel cluster counting | Phonological complexity |
| `long_word_ratio` | `words > 6 chars / total_words` | Academic register proxy |
| `func_word_ratio` | `stop_words / total_words` | Grammatical texture |
| `punct_density` | `punct_chars / total_words` | Prosodic structure |
| `flesch_re` | `206.835 − 1.015·ASL − 84.6·ASW` | Readability (higher = easier) |
| `gunning_fog` | `0.4·(ASL + 100·polysyllabic_ratio)` | Grade level equivalent |

> **ASL** = Average Sentence Length · **ASW** = Average Syllables per Word

---

## 05 · Statistical Methodology

The pipeline applies **Mann-Whitney U tests** — a non-parametric alternative to the t-test that makes no normality assumption — to each feature independently.

**Effect size** is quantified via **rank-biserial correlation** (`r`):

```
r = 1 − (2 × U) / (n₁ × n₂)

  r > 0  →  AI texts score higher on this feature
  r < 0  →  Human texts score higher on this feature
  |r| > 0.5  →  Large effect (practically significant)
```

**Significance levels:**

```
  ***  p < 0.001   ·   **  p < 0.01   ·   *  p < 0.05   ·   ns  p ≥ 0.05
```

All test results are exported to `outputs/data/statistical_analysis.csv` and persisted to MongoDB with a full audit record.

---

## 06 · Classification Baseline

### Models

| Model | Strategy | Imbalance Handling |
|---|---|---|
| **Logistic Regression** | L2-regularised, StandardScaler pipeline | `class_weight='balanced'` |
| **Random Forest** | 200 estimators, max_depth=8 | `class_weight='balanced'` |
| **XGBoost** | 200 estimators, lr=0.1, max_depth=6 | `scale_pos_weight` ratio |

### Evaluation Protocol

```
  · Stratified 5-Fold Cross-Validation (preserves class ratio per fold)
  · Metrics: ROC-AUC · Average Precision · F1 · Accuracy
  · Hold-out set: 20% stratified split for confusion matrix & SHAP
  · All runs tracked as nested MLflow child runs under a parent experiment
```

### SHAP Interpretability

The pipeline uses **TreeExplainer** (orders of magnitude faster than KernelSHAP) to generate consistent, additive feature attributions for the XGBoost model. A global bar summary plot is saved to `outputs/figures/shap_importance.png`.

---

## 07 · Experiment Tracking

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  MLFLOW HIERARCHY                                                            │
│                                                                              │
│  Experiment: ai_vs_human_text_classification_2026                           │
│  │                                                                          │
│  ├── Parent Run: stylometric_baseline_comparison                            │
│  │    ├── Child Run: LogisticRegression   (metrics + model.pkl)             │
│  │    ├── Child Run: RandomForest         (metrics + model.pkl)             │
│  │    └── Child Run: XGBoost             (metrics + model.pkl)              │
│  │                                                                          │
│  └── Artefact Run: artefact_registration                                    │
│       ├── /data/   → enriched_dataset.csv, statistical_analysis.csv        │
│       ├── /figures → all PNG visualisations                                 │
│       └── /models  → serialised model pickles                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Backend Options

| Backend | Configuration |
|---|---|
| **DagsHub** (recommended) | Set `USE_DAGSHUB = True` and provide `MLFLOW_TRACKING_URI`, `MLFLOW_TRACKING_USERNAME`, `MLFLOW_TRACKING_PASSWORD` |
| **Local file store** | Set `USE_DAGSHUB = False` — logs written to `./mlruns/` |

---

## 08 · Data Persistence

Every significant pipeline event is persisted to **MongoDB** as a structured document with:

- UTC timestamp (`logged_at`)
- SHA-256 fingerprint (`_fingerprint`) for duplicate detection
- Full metric payloads, feature lists, and artefact inventories

```
Collection: ai_vs_human_2026.experiment_runs

Events logged:
  · statistical_analysis_complete   (feature-level MWU results)
  · model_evaluation                (CV metrics per model)
  · pipeline_complete               (final summary, best model)
```

> The pipeline degrades **gracefully** if MongoDB is unreachable — all analytical and classification stages execute normally in dry-run mode; only DB writes are silently skipped.

---

## 09 · Output Artefacts

All outputs are written to `outputs/` and bundled into a single ZIP archive at `S15`.

```
outputs/
├── ai_vs_human_2026_pipeline_outputs.zip   ← single distributable bundle
│
├── data/
│   ├── enriched_dataset.csv                ← original + 11 engineered features
│   ├── statistical_analysis.csv            ← MWU results, ranked by |effect size|
│   └── model_results.csv                   ← 5-fold CV summary table
│
├── figures/
│   ├── eda_overview.png                    ← label / domain / model bar charts
│   ├── kde_all_features.png                ← 11-panel KDE overlay grid
│   ├── word_count_lexical.png              ← histogram, grouped bar, violin
│   ├── radar_profiles.png                  ← normalised stylometric radar charts
│   ├── readability_by_domain.png           ← Flesch RE & Gunning Fog KDEs
│   ├── model_comparison.png                ← GPT-4o vs Gemini-2.0 boxplots
│   ├── correlation_matrices.png            ← human vs AI feature correlations
│   ├── effect_sizes.png                    ← waterfall + per-domain heatmap
│   ├── confusion_matrix.png                ← hold-out confusion matrix + report
│   └── shap_importance.png                 ← SHAP global bar summary
│
└── models/
    ├── logisticregression.pkl
    ├── randomforest.pkl
    └── xgboost.pkl
```

---

## 10 · Project Structure

```
ai-vs-human-text-classification-2026/
│
├── ai_vs_human_2026_production_pipeline.ipynb   ← main pipeline notebook
├── README.md                                     ← this document
├── requirements.txt                              ← pinned dependencies
├── .env.example                                  ← environment variable template
│
├── data/
│   └── ai_vs_human_text_2026.csv                ← raw dataset
│
└── outputs/                                      ← generated at runtime
    ├── data/
    ├── figures/
    └── models/
```

---

## 11 · Installation

### Prerequisites

```
Python  ≥ 3.10
pip     ≥ 23.0
```

### Step 1 — Clone the repository

```bash
git clone https://github.com/your-org/ai-vs-human-text-classification-2026.git
cd ai-vs-human-text-classification-2026
```

### Step 2 — Create and activate a virtual environment

```bash
python -m venv .venv

# Unix / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment variables

```bash
cp .env.example .env
# Edit .env with your credentials (see §12 below)
```

### Step 5 — Place the dataset

```bash
# Place the CSV in the project root or the data/ subdirectory
cp /path/to/ai_vs_human_text_2026.csv data/
```

---

## 12 · Configuration Reference

Copy `.env.example` to `.env` and populate the following variables:

```bash
# ── MongoDB ──────────────────────────────────────────────────────────────────
MONGO_DB_URL=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/

# ── MLflow / DagsHub ─────────────────────────────────────────────────────────
MLFLOW_TRACKING_URI=https://dagshub.com/<username>/<repo>.mlflow
MLFLOW_TRACKING_USERNAME=<your-dagshub-username>
MLFLOW_TRACKING_PASSWORD=<your-dagshub-token>

# ── Local fallback (no remote tracking) ──────────────────────────────────────
# Leave MLFLOW_TRACKING_URI unset to use ./mlruns/ automatically
# Leave MONGO_DB_URL unset to run in dry-run mode (no DB writes)
```

> **Security:** Never commit `.env` to version control. Add it to `.gitignore`.

---

## 13 · Running the Pipeline

### Jupyter / JupyterLab

```bash
jupyter lab ai_vs_human_2026_production_pipeline.ipynb
```

Then execute cells sequentially from **S1** through **S16**, or use *Run All Cells*.

### Papermill (headless execution)

```bash
pip install papermill

papermill ai_vs_human_2026_production_pipeline.ipynb \
          outputs/executed_pipeline.ipynb \
          --log-output
```

### VS Code

Open the `.ipynb` file in VS Code with the Jupyter extension installed. Select your virtual environment as the kernel and run all cells.

---

## 14 · Results & Key Findings

### Surface & Sentence Structure

```
  ◆ AI texts are longer on average — most pronounced in the academic domain
  ◆ AI sentences are consistently longer across all domains
  ◆ Effect is strongest in news; weakest in social media posts
```

### Lexical Diversity

```
  ◆ Human texts exhibit higher Type-Token Ratio (TTR) across all domains
  ◆ Human writers show more hapax legomena (words used exactly once)
  ◆ Widest gap in academic domain — AI recycles terminology more aggressively
```

### Vocabulary & Grammar

```
  ◆ AI uses harder, longer words — higher avg_word_length and long_word_ratio
  ◆ Human writing contains proportionally more function words (determiners,
    prepositions, pronouns) — especially in social media
  ◆ AI punctuates more lightly — suggesting flatter, more uniform prose rhythm
```

### Readability

```
  ◆ AI text scores lower on Flesch Reading Ease (harder to read)
  ◆ AI text scores higher on Gunning Fog (more years of education required)
  ◆ Social domain shows the smallest readability gap — AI best mimics
    informal register
```

### Model-Level (GPT-4o vs Gemini-2.0)

```
  ◆ GPT-4o tends toward slightly longer sentences
  ◆ Gemini-2.0 uses marginally more complex vocabulary
  ◆ Inter-model differences are smaller than the human-vs-AI gap
```

### Classification Baseline

```
  ┌────────────────────────────────────────────────────────┐
  │  All three models exceed 80% ROC-AUC on 11 features    │
  │  XGBoost achieves the best ROC-AUC and F1 score        │
  │  SHAP identifies TTR and avg_sent_len as top signals   │
  └────────────────────────────────────────────────────────┘
```

---

## 15 · Reproducibility

This pipeline is designed for **full auditability**:

| Guarantee | Mechanism |
|---|---|
| **Deterministic splits** | `random_state=42` throughout; `StratifiedKFold` preserves class ratios |
| **Experiment versioning** | Every run receives a unique MLflow `run_id` |
| **Data lineage** | Enriched dataset exported to CSV at feature-engineering stage |
| **Model serialisation** | All trained models persisted as `.pkl` via `joblib` |
| **Audit log** | MongoDB documents fingerprinted with SHA-256; timestamped in UTC |
| **Portable bundle** | All outputs zipped at `S15`; reproducible from a single archive |

---

## 16 · Roadmap

```
  [ ] SMOTE / oversampling to address 2:1 class imbalance
  [ ] Transformer-based feature extraction (sentence embeddings as complement)
  [ ] Extend to long-document classification (articles, essays, reports)
  [ ] Domain adaptation — journalism, legal, medical registers
  [ ] Adversarial robustness — test against paraphrased AI texts
  [ ] REST API wrapper for real-time inference serving
  [ ] Streaming MLflow integration for online experiment comparison
  [ ] Docker containerisation for one-command deployment
```

---

## 17 · Citation

If you use this pipeline or dataset in your research, please cite:

```bibtex
@software{ai_vs_human_pipeline_2026,
  title   = {AI vs Human Text Classification — Production Pipeline 2026},
  year    = {2026},
  url     = {https://github.com/your-org/ai-vs-human-text-classification-2026},
  note    = {Stylometric feature engineering and interpretable ML
             for AI-generated text detection across academic,
             news, and social media domains.}
}
```

---

## 18 · License

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<div align="center">

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Built with rigour · Tracked with precision · Reproducible by design
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

*AI vs Human Text Classification Pipeline 2026*

</div>
