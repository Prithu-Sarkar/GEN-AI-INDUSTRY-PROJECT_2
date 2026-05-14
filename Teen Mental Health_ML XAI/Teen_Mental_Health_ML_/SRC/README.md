# 🧠 Teen Mental Health & Social Media - Industry-Grade ML Analysis

## 📋 Project Overview

This is a comprehensive machine learning pipeline for analyzing the impact of social media on teen mental health. The project includes:

- **Data Processing**: EDA, cleaning, preprocessing
- **Feature Engineering**: Interaction features, polynomial features, ratio features
- **Traditional ML Models**: Logistic Regression, Random Forest, XGBoost, LightGBM
- **Ensemble Methods**: Voting Classifier, Stacking Classifier
- **Deep Learning**: Multi-layer Neural Networks with Regularization
- **Explainability**: SHAP analysis for model interpretability
- **Experiment Tracking**: MLflow integration with DagsHub support
- **Production Ready**: Model serialization, checkpoint management

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Colab account (for cloud execution)
- Internet connection
- ~2GB RAM minimum

### Installation

1. **Open the notebook in Google Colab**:
   - Upload `teen_mental_health_ml.ipynb` to Google Colab
   - Or click: `File > Upload notebook > Select file`

2. **Run Phase 0 cells** to install dependencies:
   ```
   Phase 0.1: Install Dependencies
   Phase 0.2: Colab Secrets Configuration
   Phase 0.3: Environment Setup
   ```

3. **Configure Secrets** (in Google Colab):
   ```
   Secrets > Add new secret
   - Name: MONGO_DB_URL
     Value: mongodb://username:password@host:port
   
   - Name: MLFLOW_TRACKING_URI
     Value: https://dagshub.com/username/repo/mlflow
   
   - Name: MLFLOW_TRACKING_USERNAME
     Value: your_dagshub_username
   
   - Name: MLFLOW_TRACKING_PASSWORD
     Value: your_dagshub_token
   ```

---

## 📦 Project Structure

```
Teen_Mental_Health_ML/
├── data/
│   └── Teen_Mental_Health_Dataset.csv    # Input dataset
├── models/
│   ├── logisticregression_model.pkl
│   ├── randomforest_model.pkl
│   ├── xgboost_model.pkl
│   ├── lightgbm_model.pkl
│   └── deep_nn_model.h5
├── outputs/
│   ├── 01_eda_overview.png
│   ├── 02_model_comparison.png
│   ├── 03_deep_nn_history.png
│   ├── 04_shap_feature_importance.png
│   ├── 05_shap_summary_beeswarm.png
│   ├── 06_shap_force_plot_*.png
│   ├── 07_roc_curves_comparison.png
│   ├── 08_confusion_matrices.png
│   ├── model_metrics.csv
│   └── FINAL_REPORT.txt
├── artifacts/
│   ├── scaler.pkl                       # StandardScaler
│   ├── label_encoders.pkl               # Categorical encoders
│   ├── feature_names.pkl                # Selected features
│   ├── selected_features.pkl
│   └── config.json                      # Project configuration
├── logs/
│   └── mlruns/                          # MLflow logs
└── teen_mental_health_ml.ipynb          # Main notebook
```

---

## 🔧 API & External Services Required

### 1. **MLflow (Optional - Local or DagsHub)**

**Local MLflow Setup:**
```bash
pip install mlflow>=2.0.0
mlflow ui --host 127.0.0.1 --port 5000
```

**DagsHub Integration:**
- Create account: https://dagshub.com
- Create new repo for ML tracking
- Get credentials from Settings > Tokens
- Store in Colab Secrets

**Credentials:**
```
MLFLOW_TRACKING_URI = https://dagshub.com/username/repo/mlflow
MLFLOW_TRACKING_USERNAME = your_username
MLFLOW_TRACKING_PASSWORD = your_personal_token
```

### 2. **MongoDB (Optional - Data Logging)**

**Local MongoDB:**
```bash
# Installation
brew install mongodb-community  # macOS
# or docker
docker run -d -p 27017:27017 mongo

# Connection string
MONGO_DB_URL = mongodb://localhost:27017
```

**MongoDB Atlas (Cloud):**
- Sign up: https://www.mongodb.com/cloud/atlas
- Create cluster
- Get connection string
- Format: `mongodb+srv://username:password@cluster.mongodb.net/dbname`

### 3. **Google Colab Secrets (Required for Colab)**

Enable Google Secrets API:
```python
from google.colab import userdata
secret = userdata.get('SECRET_NAME')
```

**Required Secrets:**
- `MONGO_DB_URL` (optional)
- `MLFLOW_TRACKING_URI` (optional)
- `MLFLOW_TRACKING_USERNAME` (optional)
- `MLFLOW_TRACKING_PASSWORD` (optional)

---

## 📊 Dataset Information

### Dataset Overview
- **Source**: Teen_Mental_Health_Dataset.csv
- **Records**: 1,200 teenagers (ages 13-19)
- **Features**: 13+ columns
- **Target Variable**: Mental health indicators (depression, anxiety, stress)

### Key Features
- **Social Media Usage**: Hours per day, platforms used
- **Sleep Patterns**: Sleep hours, quality
- **Screen Time**: Device usage duration
- **Physical Activity**: Exercise frequency
- **Mental Health Indicators**: Stress, anxiety, depression levels

### Data Quality
- Handles missing values (median for numerical, mode for categorical)
- Outlier detection using IQR method
- Class imbalance handling via stratified splitting

---

## 🏃 Execution Phases

### Phase 0: Environment Setup (5-10 min)
- Install dependencies
- Configure secrets
- Create directory structure
- Set random seeds for reproducibility

### Phase 1: Data Loading (2-3 min)
- Load dataset
- Display basic statistics
- Check data types and missing values

### Phase 2: EDA (10-15 min)
- Distribution analysis
- Correlation analysis
- Missing value visualization
- Feature relationships

### Phase 3: Preprocessing (15-20 min)
- Handle missing values
- Encode categorical variables
- Outlier detection
- Feature engineering (interactions, polynomials, ratios)
- Feature selection (SelectKBest, Mutual Info)
- Feature scaling (StandardScaler)
- Train-test split (80-20 stratified)

### Phase 4: Traditional ML Models (30-40 min)
- Hyperparameter optimization with Optuna (20 trials each)
- Train 4 models:
  - Logistic Regression
  - Random Forest
  - XGBoost
  - LightGBM
- Cross-validation and evaluation
- MLflow experiment tracking

### Phase 5: Ensemble Learning (15-25 min)
- Voting Classifier (soft voting)
- Stacking Classifier (5-fold CV)
- Performance comparison

### Phase 6: Deep Learning (20-30 min)
- Dense Neural Network (128-64-32-16-1)
- Batch normalization
- L2 regularization
- Dropout layers
- Early stopping
- Learning rate reduction

### Phase 7: SHAP Explainability (10-15 min)
- SHAP TreeExplainer (for XGBoost)
- Feature importance ranking
- Summary plots (bar and beeswarm)
- Force plots for sample predictions

### Phase 8: Final Evaluation (10-15 min)
- Comprehensive metrics for all models
- ROC curve comparison
- Confusion matrices
- Best model identification

### Phase 9: Model Persistence (5 min)
- Save all trained models
- Save preprocessing artifacts
- Save feature names and configuration
- Create deployment-ready files

### Phase 10: Report & Export (10 min)
- Generate comprehensive report
- Create ZIP archive
- Prepare for download

---

## 📈 Model Performance Metrics

The notebook evaluates models on:
- **AUC (Area Under ROC Curve)**: Probability of correct ranking
- **Accuracy**: Overall correctness
- **Precision**: True positives among positive predictions
- **Recall**: True positives among actual positives
- **F1-Score**: Harmonic mean of precision and recall
- **Balanced Accuracy**: For imbalanced datasets

---

## 🔍 SHAP Explainability

SHAP (SHapley Additive exPlanations) provides:
- **Feature Importance**: Which features matter most
- **Impact Direction**: How features affect predictions
- **Individual Predictions**: Why specific predictions were made
- **Model Debugging**: Identify potential biases

### SHAP Outputs
1. **Summary Plot (Bar)**: Average feature importance
2. **Summary Plot (Beeswarm)**: Feature value distributions
3. **Force Plots**: Individual prediction explanations
4. **Dependence Plots**: Feature interaction analysis

---

## 🔗 MLflow Integration

### Local MLflow
```python
mlflow.set_experiment("Teen_Mental_Health_ML")
with mlflow.start_run(run_name="ModelName"):
    mlflow.log_param("param_name", value)
    mlflow.log_metric("metric_name", value)
    mlflow.log_artifact("path/to/file")
```

### DagsHub Integration
```python
import os
os.environ['MLFLOW_TRACKING_URI'] = 'https://dagshub.com/...'
os.environ['MLFLOW_TRACKING_USERNAME'] = '...'
os.environ['MLFLOW_TRACKING_PASSWORD'] = '...'
```

### View Results
- **Local**: http://localhost:5000
- **DagsHub**: https://dagshub.com/username/repo/experiments

---

## 💾 Model Persistence

### Loading Trained Models
```python
import pickle
import tensorflow as tf

# Load scikit-learn models
with open('models/xgboost_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load Deep Learning model
nn_model = tf.keras.models.load_model('models/deep_nn_model.h5')

# Load preprocessing artifacts
with open('artifacts/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
```

### Making Predictions
```python
# Preprocess data
X_scaled = scaler.transform(X_new)

# Get predictions
y_pred = model.predict(X_scaled)
y_pred_proba = model.predict_proba(X_scaled)[:, 1]
```

---

## 🚨 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'xgboost'"
**Solution**: Run Phase 0.1 (Install Dependencies)

### Issue: "Missing MONGO_DB_URL secret"
**Solution**: Create secret in Colab or use local MongoDB, or skip MongoDB integration

### Issue: "MLflow tracking URI not accessible"
**Solution**: 
- Use local MLflow: `mlflow ui`
- Or set `USE_DAGSHUB = False` in Phase 0.2

### Issue: "CUDA out of memory"
**Solution**: 
- Reduce batch size in Deep Learning phase
- Use CPU instead: `os.environ['CUDA_VISIBLE_DEVICES'] = '-1'`

### Issue: "Data not loading"
**Solution**: 
- Ensure CSV file is in `data/` folder
- Check file path in Phase 1.2

---

## 📝 Reproducibility

The notebook ensures reproducibility by:
- Setting random seeds (NumPy, TensorFlow, Random, Scikit-learn)
- Using stratified train-test split
- Saving all preprocessing artifacts
- Logging all hyperparameters to MLflow

```python
np.random.seed(42)
tf.random.set_seed(42)
random.seed(42)
```

---

## 🔐 Best Practices

1. **Version Control**:
   - Keep `.ipynb_checkpoints` in `.gitignore`
   - Don't commit large model files to Git
   - Use DagsHub for experiment tracking

2. **Data Security**:
   - Never hardcode credentials
   - Use Colab Secrets for sensitive data
   - Don't share MLflow passwords

3. **Model Deployment**:
   - Always test on test set first
   - Monitor prediction distributions
   - Log predictions to MongoDB
   - Set up alerts for data drift

4. **Maintenance**:
   - Retrain models monthly/quarterly
   - Monitor feature importance changes
   - Check for performance degradation
   - Update preprocessing pipeline

---

## 📚 Documentation

- **Notebook**: Inline comments in every cell
- **Markdown Cells**: Section headers and explanations
- **FINAL_REPORT.txt**: Summary of all results
- **config.json**: Project metadata
- **model_metrics.csv**: Performance benchmarks

---

## 🎯 Next Steps

1. **Upload Dataset**: Place `Teen_Mental_Health_Dataset.csv` in `data/` folder
2. **Configure Secrets** (optional):
   - MLflow credentials
   - MongoDB connection
3. **Run All Cells**: Start from Phase 0
4. **Review Outputs**: Check visualizations and metrics
5. **Deploy Model**: Use saved artifacts for production

---

## 📞 Support & Resources

- **TensorFlow Docs**: https://tensorflow.org/
- **Scikit-learn**: https://scikit-learn.org/
- **XGBoost**: https://xgboost.readthedocs.io/
- **SHAP**: https://shap.readthedocs.io/
- **MLflow**: https://mlflow.org/
- **DagsHub**: https://dagshub.com/

---

## 📄 License

This project is provided as-is for educational and research purposes.

---

**Last Updated**: May 2026  
**Author**: Claude AI  
**Version**: 1.0.0
