# 🎓 Student Learning Engagement Analyzer

A machine learning system that predicts student dropout risk from early engagement signals and generates personalized recommendations.

## Overview

The model uses a Decision Tree classifier trained on five behavioral features captured in the first days of a course. It outputs a risk level (High / Medium / Low), human-readable observations, and actionable next steps — without exposing ML internals to the end user.

## Project Structure

```
├── config/
│   └── config.yaml           # Risk & engagement thresholds
├── core/
│   ├── feature_builder.py    # Input → DataFrame
│   ├── predictor.py          # Main predict + explain logic
│   └── recommender.py        # Rule-based recommendation engine
├── dataset/artefacts/        # Versioned student engagement CSVs (v1–v3)
├── models/artefacts/         # Saved joblib model
├── utils/
│   ├── model_loader.py
│   ├── path_utils.py
│   └── validators.py
├── streamlit_app.py          # Interactive UI
├── main.py                   # CLI entry point
└── test/experiment/notebook/ # Exploration notebooks (N1–N4)
```

## Features Used

| Feature | Description |
|---|---|
| `total_click` | Total learning interactions during the course |
| `early_click` | Interactions in the first few days |
| `early_active_days` | Distinct active days in the early period |
| `first_activity_day` | Days after course start of first login (negative = pre-enrolled) |
| `pre_course_engaged` | Whether student interacted before the course started |

## Quickstart

```bash
pip install -r requirements.txt
python main.py
```

To run the Streamlit UI:

```bash
streamlit run streamlit_app.py
```

## Google Colab

Open `student_engagement_colab.ipynb` in Colab. Before running, add the following secrets via **Settings → Secrets**:

- `MONGO_DB_URL`
- `MLFLOW_TRACKING_URI`
- `MLFLOW_TRACKING_USERNAME`
- `MLFLOW_TRACKING_PASSWORD`

The notebook trains the model, tracks experiments to DagsHub via MLflow, and downloads all outputs as a ZIP.

## MLflow Tracking

Set `USE_DAGSHUB = True` in the notebook (or env vars) to log to DagsHub. Set to `False` to log locally to `./mlruns`.
