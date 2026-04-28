# Telecom Customer Churn Prediction

An end-to-end machine learning pipeline that predicts customer churn for a telecommunications company — from exploratory analysis through to a deployable Streamlit application, with full experiment tracking via MLflow and DagsHub.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Dataset](#dataset)
- [Pipeline Architecture](#pipeline-architecture)
- [Models & Results](#models--results)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [Environment Variables & Secrets](#environment-variables--secrets)
- [Running the Notebook](#running-the-notebook)
- [Running the Streamlit App](#running-the-streamlit-app)
- [MLflow Experiment Tracking](#mlflow-experiment-tracking)
- [MongoDB Integration](#mongodb-integration)
- [Key Findings](#key-findings)
- [Future Work](#future-work)

---

## Project Overview

Customer churn — the rate at which subscribers cancel their service — is one of the most critical business metrics in the telecom industry. Acquiring a new customer costs significantly more than retaining an existing one, making accurate churn prediction a high-value problem.

This project builds a full supervised learning pipeline that:

- Performs in-depth exploratory data analysis to surface actionable churn drivers
- Handles severe class imbalance (~73% no-churn vs 27% churn) using SMOTE, SMOTEENN, and class-weighting strategies
- Trains and compares six classifier families with comprehensive evaluation
- Optimises the best model using both RandomizedSearchCV and Optuna Bayesian optimisation
- Tracks all experiments with MLflow, backed by DagsHub for remote storage
- Persists trained models and preprocessing artefacts for reproducible inference
- Pushes data and metrics to MongoDB Atlas for downstream consumption
- Serves predictions through an interactive Streamlit web application

---

## Repository Structure

```
telecom-churn-prediction/
│
├── Telecom_Churn_Prediction_Colab.ipynb   # Main notebook — full pipeline
├── streamlit_app.py                        # Prediction web application
├── requirements.txt                        # Python dependencies
│
├── ada_boost_churn_model.pkl              # Saved AdaBoost model
├── best_xgboost_churn_model.pkl           # Best XGBoost (RandomizedSearchCV)
├── best_optuna_churn_model.pkl            # Best XGBoost (Optuna)
├── standard_scaler.pkl                    # Fitted StandardScaler
├── feature_columns.json                   # Ordered feature column list
│
└── README.md
```

> **Note:** `Customer-Churn.csv` is not committed to the repository. Upload it at runtime when prompted, or place it in the working directory before launching the app.

---

## Dataset

| Property | Detail |
|---|---|
| Source | IBM Telco Customer Churn dataset |
| Rows | 7,043 customers |
| Features | 21 (demographics, account info, service subscriptions) |
| Target | `Churn` — binary (Yes / No) |
| Class ratio | ~73% No-Churn, 27% Churn |

Key columns include `tenure`, `MonthlyCharges`, `TotalCharges`, `Contract`, `PaymentMethod`, `InternetService`, `TechSupport`, and `OnlineSecurity`.

---

## Pipeline Architecture

```
Raw CSV
   │
   ▼
Data Cleaning
  • TotalCharges → numeric
  • Drop 11 NaN rows (0.15%)
   │
   ▼
Feature Engineering
  • tenure → tenure_bin (6 × 12-month intervals)
  • One-hot encoding (drop_first=True)
  • StandardScaler
   │
   ▼
Imbalance Handling
  • SMOTEENN  (over + undersampling)
  • SMOTE     (oversampling only)
  • Class weights / scale_pos_weight
   │
   ▼
Model Training & Evaluation
  • Decision Tree  • Random Forest
  • XGBoost        • AdaBoost
  • CatBoost       • LightGBM
   │
   ▼
Hyperparameter Optimisation
  • RandomizedSearchCV (50 iterations, CV=5, scoring=F1)
  • Optuna             (100 trials, Bayesian, scoring=F1)
   │
   ▼
MLflow Tracking  ──►  DagsHub Remote
   │
   ▼
Model Persistence (.pkl) + MongoDB Push
   │
   ▼
Streamlit App
```

---

## Models & Results

All models are evaluated on a held-out 20% stratified test set. Scoring is primarily based on **F1 (minority class)** given the class imbalance.

| Model | Imbalance Strategy | Notes |
|---|---|---|
| Decision Tree | None | Baseline |
| Decision Tree | SMOTEENN | Combined resampling |
| Random Forest (n=500) | SMOTEENN | Ensemble baseline |
| Random Forest (balanced) | `class_weight='balanced'` | |
| XGBoost | `scale_pos_weight` | Built-in weighting |
| XGBoost | SMOTE | Oversampling |
| XGBoost | RandomizedSearchCV | 50-iter grid, CV=5 |
| XGBoost | Optuna | 100-trial Bayesian search |
| AdaBoost | Sample weights | Minority-class boosted |
| CatBoost | `auto_class_weights='Balanced'` | |
| LightGBM | `scale_pos_weight` | |

The **Optuna-tuned XGBoost** and **weighted AdaBoost** models are the primary production candidates, with the AdaBoost variant saved as the default app model for its interpretability and compact size.

---

## Tech Stack

| Category | Libraries |
|---|---|
| Data processing | `pandas`, `numpy` |
| Visualisation | `matplotlib`, `seaborn` |
| Machine learning | `scikit-learn`, `xgboost`, `lightgbm`, `catboost` |
| Imbalance handling | `imbalanced-learn` (SMOTE, SMOTEENN, ADASYN) |
| Hyperparameter tuning | `scikit-learn` RandomizedSearchCV, `optuna` |
| Experiment tracking | `mlflow`, `dagshub` |
| Database | `pymongo` (MongoDB Atlas) |
| Model serialisation | `joblib` |
| Web application | `streamlit` |

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/telecom-churn-prediction.git
cd telecom-churn-prediction
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables & Secrets

The pipeline reads credentials from environment variables. Set them before running the notebook or the app.

| Variable | Description |
|---|---|
| `MONGO_DB_URL` | MongoDB Atlas connection string |
| `MLFLOW_TRACKING_URI` | DagsHub MLflow tracking URI |
| `MLFLOW_TRACKING_USERNAME` | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | DagsHub access token |

**When running the notebook**, these are loaded from the platform's Secrets manager — add them in the Secrets panel (🔑) before executing Section 1.

**When running locally**, export them in your shell:

```bash
export MONGO_DB_URL="mongodb+srv://..."
export MLFLOW_TRACKING_URI="https://dagshub.com/<user>/<repo>.mlflow"
export MLFLOW_TRACKING_USERNAME="<dagshub-username>"
export MLFLOW_TRACKING_PASSWORD="<dagshub-token>"
```

To run with local MLflow instead of DagsHub, set `USE_DAGSHUB = False` in Section 1 of the notebook — logs will be written to `./mlruns/`.

---

## Running the Notebook

Open `Telecom_Churn_Prediction_Colab.ipynb` and execute cells from top to bottom:

1. **Section 1** — Set secrets (Secrets panel) → run env setup cell
2. **Section 2** — Install packages
3. **Section 3** — Upload `Customer-Churn.csv` when prompted
4. **Sections 4–7** — EDA, preprocessing, model training, optimisation (run sequentially; each section depends on the previous)
5. **Section 8** — MLflow logging (requires env vars)
6. **Section 9** — Saves `.pkl` artefacts to the working directory
7. **Section 10** — MongoDB push (skipped automatically if `MONGO_DB_URL` is not set)
8. **Section 11** — Writes `streamlit_app.py` and `requirements.txt` to disk

---

## Running the Streamlit App

Ensure `Customer-Churn.csv` and `ada_boost_churn_model.pkl` are in the same directory as `streamlit_app.py`.

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`. Use the sidebar controls to input customer attributes and click **Predict** to get a churn probability estimate.

To expose the app from a remote server:

```bash
nohup streamlit run streamlit_app.py &
```

---

## MLflow Experiment Tracking

All runs are logged under the experiment name `telecom_churn_prediction`. Each run records:

- **Parameters** — all model hyperparameters
- **Metrics** — accuracy, F1, precision, recall
- **Artefact** — the serialised model (sklearn or XGBoost flavour)

View runs on your DagsHub project page under the **Experiments** tab, or locally via:

```bash
mlflow ui --backend-store-uri ./mlruns
```

Then open `http://localhost:5000`.

---

## MongoDB Integration

When `MONGO_DB_URL` is configured, the pipeline pushes two collections to the `telecom_churn` database:

| Collection | Contents |
|---|---|
| `churn_data` | Cleaned, feature-engineered customer records |
| `model_metrics` | F1 and accuracy scores for key model variants |

Both collections are cleared and re-populated on each run (idempotent).

---

## Key Findings

**High-churn segments:**
- Month-to-month contract customers — churn rate ~41%
- Electronic check payment method — churn rate ~44%
- Customers with no Online Security or Tech Support
- Short-tenure customers (1–12 months)
- High Monthly Charges combined with low Total Charges

**Low-churn segments:**
- Two-year contract holders
- Customers with 5+ years of tenure
- Subscribers without internet service

**Features with minimal churn impact:**
- Gender
- Availability of phone service
- Number of phone lines

---

## Future Work

- Add SHAP explainability for individual prediction explanations
- Build a real-time scoring API with FastAPI or Flask
- Set up a retraining trigger when data drift is detected (Evidently AI)
- Extend the Streamlit app with a batch prediction upload interface
- Add CI/CD pipeline for automated model registration on DagsHub

---

## License

This project is released under the MIT License.
