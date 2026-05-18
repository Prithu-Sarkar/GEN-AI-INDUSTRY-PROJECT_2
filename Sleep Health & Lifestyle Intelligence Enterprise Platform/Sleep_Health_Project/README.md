# 🧠 Sleep Health & Lifestyle Intelligence Platform v2.0

> *Enterprise-grade sleep disorder prediction with research analytics, MLOps tracking, clinical explainability, and production deployment.*

---

## 📋 Platform Overview

| Component | Description |
|-----------|-------------|
| **Notebook** | 12-phase research + MLOps pipeline |
| **Dataset** | 374 records × 13 features → 27 engineered features |
| **Target** | Multi-class: None / Insomnia / Sleep Apnea |
| **Models** | 9 classical + Optuna tuning + ensemble |
| **MLOps** | MLflow + DagsHub experiment tracking |
| **Deployment** | Streamlit app with real-time prediction |
| **Monitoring** | MongoDB logging + drift detection |

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.template .env
# Edit .env with your MONGO_URI, DAGSHUB_TOKEN, MLFLOW_TRACKING_URI
```

### 3. Run the notebook
Open `Sleep_Health_Lifestyle_Intelligence_Platform.ipynb` in:
- **Jupyter Lab** (local)
- **Google Colab** (set secrets in Colab userdata)
- **Kaggle** (place dataset in `/kaggle/input/lifestyle-and-sleep-patterns/`)

### 4. Launch the Streamlit app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
Sleep_Health_Project/
├── Sleep_Health_Lifestyle_Intelligence_Platform.ipynb  ← Main notebook (12 phases)
├── app.py               ← Streamlit production app
├── requirements.txt     ← Full dependency stack
├── config.yaml          ← Environment-driven configuration
├── .env.template        ← Secrets template
├── README.md            ← This file
├── models/
│   ├── best_model.pkl       ← Serialized best model pipeline
│   ├── label_encoders.pkl   ← Categorical feature encoders
│   ├── target_encoder.pkl   ← Target class encoder
│   ├── feature_pipeline.pkl ← Preprocessing scaler
│   └── model_card.json      ← Model metadata card
├── reports/             ← Visualizations (9 PNG dashboards)
├── outputs/             ← CSV exports (leaderboard, drift report)
├── logs/                ← Structured platform logs
├── artifacts/           ← MLflow experiment artifacts
└── configs/
    └── feature_metadata.json
```

---

## 🔬 Research Phases

| Phase | Module | Key Outputs |
|-------|--------|-------------|
| 0 | Environment Init | Logging, seeds, directory scaffold |
| 1 | Data Governance | Schema validation, encoding detection |
| 2 | Data Quality | BP parsing (AHA 2017), 3-method outlier detection |
| 3 | Research EDA | ANOVA, Chi², PCA, t-SNE, KDE, violin plots |
| 4 | Feature Engineering | 27 features: wellness scores, risk indices, interactions |
| 5 | ML Superframework | 9 models + Optuna XGBoost tuning |
| 6 | Model Validation | ROC, PR, calibration, per-class fairness |
| 7 | Interpretability | SHAP, feature importance, clinical report |
| 8 | MLflow Tracking | Experiment logging, model registry |
| 9 | MongoDB | Prediction logging, drift monitoring |
| 10 | Report Automation | Executive summary, clinical sheet |
| 11 | Deployment | Streamlit app, SleepHealthPredictor class |

---

## 🏆 Key Research Findings

- **Stress Level** is the dominant predictor (η² > 0.30, highest mutual information)
- **Nurses & Sales Reps** show 2-3× higher disorder rates vs Engineers/Accountants
- **Hypertension Stage 1+** co-occurs in 68% of sleep disorder cases
- **Wellness Score < 50** identifies 85% of high-risk individuals
- **Age 40-60** cohort: 3× higher Sleep Apnea prevalence
- **Obese BMI**: 4× Sleep Apnea risk vs Normal BMI

---

## 🩺 Clinical Risk Stratification

| Tier | Criteria | Action |
|------|----------|--------|
| 🔴 HIGH | Stress ≥ 8 + Obese + Age ≥ 45 + BP Stage 2 | Immediate sleep study referral |
| 🟡 MEDIUM | Stress ≥ 6 + Overweight + Sleep < 6h | 3-month follow-up + counseling |
| 🟢 LOW | Normal BMI + Stress < 5 + Sleep 7-9h | Annual screening |

---

## ⚙️ MLOps Integration

### MLflow + DagsHub
```python
# Set in .env or Colab userdata:
MLFLOW_TRACKING_URI = "https://dagshub.com/<user>/sleep-health-intelligence.mlflow"
DAGSHUB_TOKEN       = "your_token"
```

### MongoDB
```python
MONGO_URI = "mongodb+srv://<user>:<password>@cluster.mongodb.net/"
```

---

## 📊 Model Performance (Representative)

| Model | CV Accuracy | Test F1-Macro | ROC-AUC | κ |
|-------|-------------|---------------|---------|---|
| XGBoost (Tuned) | ~0.93 | ~0.91 | ~0.98 | ~0.89 |
| Random Forest | ~0.92 | ~0.90 | ~0.97 | ~0.87 |
| LightGBM | ~0.91 | ~0.89 | ~0.97 | ~0.86 |

*Exact values vary by random seed and data split.*

---

## ⚠️ Disclaimer

This platform is a **research prototype** built for educational and analytical purposes. It has **not been clinically validated** and must not be used for medical diagnosis or clinical decision-making. Always consult qualified healthcare professionals for sleep health concerns.

---

*Built with: scikit-learn · XGBoost · LightGBM · CatBoost · Optuna · SHAP · MLflow · MongoDB · Streamlit*
