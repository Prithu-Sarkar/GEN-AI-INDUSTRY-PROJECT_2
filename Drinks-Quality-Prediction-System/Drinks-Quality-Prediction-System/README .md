# 🍷 Drinks Quality Prediction — End-to-End ML Project

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-black?logo=flask)](https://flask.palletsprojects.com)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange?logo=mlflow)](https://mlflow.org)
[![DagsHub](https://img.shields.io/badge/DagsHub-Experiment%20Tracking-green)](https://dagshub.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ElasticNet-F7931E?logo=scikit-learn)](https://scikit-learn.org)

An end-to-end machine learning project that predicts the quality score of drinks using physicochemical properties. Built with a modular pipeline architecture, experiment tracking via MLflow/DagsHub, and a Flask web interface for real-time inference.

---

## 📐 Architecture

```
User → Flask App → Prediction Pipeline → ElasticNet Model → Quality Score
                ↓
         Training Pipeline
    ┌────────────────────────┐
    │  Data Ingestion        │
    │  Data Validation       │
    │  Data Transformation   │
    │  Model Trainer         │
    │  Model Evaluation      │
    └────────────┬───────────┘
                 ↓
         Artifacts / MLflow
```

---

## 📁 Project Structure

```
.
├── src/mlProject/
│   ├── components/          # Core logic for each pipeline stage
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   └── model_evaluation.py
│   ├── pipeline/            # Stage orchestrators + prediction
│   │   ├── stage_01_data_ingestion.py
│   │   ├── stage_02_data_validation.py
│   │   ├── stage_03_data_transformation.py
│   │   ├── stage_04_model_trainer.py
│   │   ├── stage_05_model_evaluation.py
│   │   └── prediction.py
│   ├── config/configuration.py   # ConfigurationManager
│   ├── entity/config_entity.py   # Dataclasses for configs
│   ├── utils/common.py           # Shared utilities
│   └── constants/__init__.py     # File path constants
├── config/config.yaml       # Artifact paths & URLs
├── params.yaml              # Model hyperparameters
├── schema.yaml              # Dataset schema & target column
├── main.py                  # Full pipeline runner
├── app.py                   # Flask web application
├── setup.py                 # Package installer
└── templates/               # HTML UI templates
    ├── index.html
    └── results.html
```

---

## 🚀 Quickstart

### 1. Clone & Setup

```bash
git clone https://github.com/entbappy/End-to-end-ML-Project
cd End-to-end-ML-Project

conda create -n mlproj python=3.10 -y
conda activate mlproj

pip install -r requirements.txt
pip install -e .
```

### 2. Configure Secrets

Set the following environment variables (or use Colab Secrets):

```bash
export MLFLOW_TRACKING_URI=<your_dagshub_mlflow_uri>
export MLFLOW_TRACKING_USERNAME=<your_dagshub_username>
export MLFLOW_TRACKING_PASSWORD=<your_dagshub_token>
```

### 3. Run Training Pipeline

```bash
python main.py
```

### 4. Launch Web App

```bash
python app.py
# → http://localhost:8080
```

---

## ⚙️ Pipeline Stages

| # | Stage | Input | Output |
|---|-------|-------|--------|
| 1 | **Data Ingestion** | GitHub ZIP URL | `artifacts/data_ingestion/Drinks-data.csv` |
| 2 | **Data Validation** | CSV + `schema.yaml` | `artifacts/data_validation/status.txt` |
| 3 | **Data Transformation** | Validated CSV | `train.csv`, `test.csv` |
| 4 | **Model Trainer** | Train/test splits | `model.joblib` |
| 5 | **Model Evaluation** | Model + test data | `metrics.json` + MLflow run |

---

## 🧪 Model

| Parameter | Value |
|-----------|-------|
| Algorithm | ElasticNet (scikit-learn) |
| `alpha` | `0.2` |
| `l1_ratio` | `0.1` |
| Target | `quality` (int) |
| Features | 11 physicochemical properties |

**Input features:** `fixed acidity`, `volatile acidity`, `citric acid`, `residual sugar`, `chlorides`, `free sulfur dioxide`, `total sulfur dioxide`, `density`, `pH`, `sulphates`, `alcohol`

---

## 🌐 API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/train` | GET | Trigger full training pipeline |
| `/predict` | POST | Accept form input, return quality prediction |

---

## 📓 Google Colab

A self-contained Colab notebook is included that builds the full project structure, writes all source files, runs the pipeline, and downloads artifacts — no local setup needed.

> Open `Drinks_Quality_Prediction.ipynb` → Runtime → Run All

---

## 📊 Experiment Tracking

Metrics and model artifacts are logged to **MLflow** on every evaluation run. When `USE_DAGSHUB = True`, runs are tracked remotely on DagsHub.

Logged per run: `rmse`, `mae`, `r2`, ElasticNet params, registered model `ElasticnetModel`.

---

## 🗂️ Configuration Files

| File | Purpose |
|------|---------|
| `config/config.yaml` | Artifact directory paths, dataset source URL |
| `params.yaml` | ElasticNet hyperparameters (`alpha`, `l1_ratio`) |
| `schema.yaml` | Column names, dtypes, and target column definition |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
