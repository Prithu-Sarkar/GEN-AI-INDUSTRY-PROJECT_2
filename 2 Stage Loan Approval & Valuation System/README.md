# Loan Approval Prediction

A two-stage machine learning system that predicts loan approval decisions and, for approved applications, estimates the sanctioned loan amount. The pipeline covers data ingestion, exploratory analysis, model training, experiment tracking, and a web interface for inference.

---

## Overview

The system operates in two sequential stages:

- **Stage 1 — Classification:** A Random Forest classifier determines whether an application should be approved or rejected, along with a calibrated approval probability.
- **Stage 2 — Regression:** For approved applications, a separate Random Forest regressor predicts the appropriate sanctioned loan amount based on the applicant's financial profile.

---

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── loader.py        # Model loading utilities
│   ├── predict.py       # Two-stage prediction logic
│   └── utils.py         # Input validation and DataFrame helpers
├── models/
│   ├── stage_1_rf_classifier_pipeline.pkl
│   └── stage_2_rf_regression_pipeline.pkl
├── streamlit_app.py     # Web interface
├── main.py              # CLI entry point
├── config.yaml          # Model paths and UI defaults
└── requirements.txt
```

---

## Setup

**Requirements:** Python 3.10+

```bash
git clone https://github.com/your-username/loan-approval-prediction.git
cd loan-approval-prediction
pip install -r requirements.txt
```

---

## Running the Application

### Web Interface

```bash
streamlit run streamlit_app.py
```

Opens a browser UI where applicant details can be entered and predictions are returned instantly with an approval probability gauge and sanctioned amount estimate.

### Command Line

```bash
python main.py
```

Prompts for each input field interactively, with sensible defaults loaded from `config.yaml`.

---

## Configuration

Model paths and UI default values are managed in `config.yaml`:

```yaml
models:
  classifier: models/stage_1_rf_classifier_pipeline.pkl
  regressor:  models/stage_2_rf_regression_pipeline.pkl

ui:
  default_inputs:
    no_of_dependents: 1
    education: Graduate
    income_annum: 1200000
    cibil_score: 800
    ...
```

---

## ML Pipeline

### Data

Dataset: [Loan Approval Prediction Dataset](https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset)

Features include applicant demographics, income, CIBIL score, loan details, and asset valuations.

### Preprocessing

- Numeric features: median imputation → standard scaling
- Categorical features: mode imputation → one-hot encoding
- Separate preprocessing pipelines fitted independently for each stage to prevent data leakage

### Model Training

Both stages use scikit-learn `Pipeline` objects combining the preprocessor and estimator. Hyperparameters were selected via 5-fold `GridSearchCV`.

| | Stage 1 | Stage 2 |
|---|---|---|
| **Model** | RandomForestClassifier | RandomForestRegressor |
| `n_estimators` | 400 | 200 |
| `max_depth` | None | 8 |
| `max_features` | None | None |
| `min_samples_split` | 2 | 5 |
| **CV metric** | F1 | R² |

### Experiment Tracking

All runs are logged to [DagsHub](https://dagshub.com) via MLflow, including hyperparameters, evaluation metrics, plots, and serialised pipeline artifacts.

Set the following environment variables before training:

```bash
export MLFLOW_TRACKING_URI=<your-dagshub-mlflow-uri>
export MLFLOW_TRACKING_USERNAME=<your-username>
export MLFLOW_TRACKING_PASSWORD=<your-token>
export MONGO_DB_URL=<your-mongodb-connection-string>
```

---

## Input Features

| Feature | Type | Description |
|---|---|---|
| `no_of_dependents` | Numeric | Number of financial dependents |
| `education` | Categorical | `Graduate` / `Not Graduate` |
| `self_employed` | Categorical | `Yes` / `No` |
| `income_annum` | Numeric | Annual income (₹) |
| `loan_amount` | Numeric | Requested loan amount (₹) |
| `loan_term` | Numeric | Loan duration in years |
| `cibil_score` | Numeric | Credit score (300–900) |
| `residential_assets_value` | Numeric | Value of residential assets (₹) |
| `commercial_assets_value` | Numeric | Value of commercial assets (₹) |
| `luxury_assets_value` | Numeric | Value of luxury assets (₹) |
| `bank_asset_value` | Numeric | Value of bank holdings (₹) |

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML | scikit-learn |
| Experiment Tracking | MLflow, DagsHub |
| Data Persistence | MongoDB (PyMongo) |
| Web Interface | Streamlit |
| Serialisation | joblib |
| Configuration | PyYAML |

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
