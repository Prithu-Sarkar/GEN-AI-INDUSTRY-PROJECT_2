# 🔌 API & Configuration Guide

## Table of Contents
1. [MLflow Setup](#mlflow-setup)
2. [MongoDB Configuration](#mongodb-configuration)
3. [Google Colab Secrets](#google-colab-secrets)
4. [DagsHub Integration](#dagshub-integration)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

---

## MLflow Setup

### What is MLflow?
MLflow is an open-source platform for managing ML lifecycles. It tracks:
- Parameters (hyperparameters)
- Metrics (performance scores)
- Artifacts (models, plots, data)
- Runs (experiment executions)

### Option 1: Local MLflow (No API Required)

**Installation:**
```bash
pip install mlflow>=2.0.0
```

**Start Local Server:**
```bash
# Terminal/Command Prompt
mlflow ui --host 127.0.0.1 --port 5000
```

**Access Dashboard:**
- Open browser: http://localhost:5000
- View experiments and runs
- Compare metrics across models

**Configuration in Notebook:**
```python
import os
os.environ['MLFLOW_TRACKING_URI'] = 'file:///path/to/mlruns'
# OR
mlflow.set_tracking_uri('file:///path/to/mlruns')
```

**Advantages:**
- ✅ No account needed
- ✅ Completely private
- ✅ Works offline
- ✅ All data stored locally

**Disadvantages:**
- ❌ Not accessible remotely
- ❌ Hard to share with team
- ❌ No cloud backup

---

### Option 2: DagsHub MLflow (Recommended for Teams)

**What is DagsHub?**
- Cloud platform for ML version control
- Built-in MLflow integration
- GitHub-like interface for ML
- Free tier available

**Step 1: Create DagsHub Account**
1. Visit: https://dagshub.com
2. Sign up with GitHub or email
3. Create new repository
4. Name: `teen-mental-health-ml`

**Step 2: Get MLflow Credentials**
1. Go to repo Settings > Integrations
2. Find "MLflow" section
3. Copy the three values:
   - **MLFLOW_TRACKING_URI**: https://dagshub.com/username/repo/mlflow
   - **MLFLOW_TRACKING_USERNAME**: your_username
   - **MLFLOW_TRACKING_PASSWORD**: personal_access_token

**Step 3: Create Personal Access Token (PAT)**
1. Go to Settings > Access Tokens
2. Click "New Token"
3. Name: "MLflow Experiments"
4. Permissions: `repo`, `read:user`
5. Copy the token (you'll only see it once)

**Step 4: In Google Colab**
```python
import os
os.environ['MLFLOW_TRACKING_URI'] = 'https://dagshub.com/your_username/your_repo/mlflow'
os.environ['MLFLOW_TRACKING_USERNAME'] = 'your_username'
os.environ['MLFLOW_TRACKING_PASSWORD'] = 'your_personal_access_token'
```

**Step 5: Use in Notebook**
```python
import mlflow

mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
mlflow.set_experiment("Teen_Mental_Health_ML")

with mlflow.start_run(run_name="XGBoost"):
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("auc", 0.95)
    mlflow.log_artifact("model.pkl")
```

**View Experiments:**
- DagsHub Dashboard: https://dagshub.com/username/repo
- Click "Experiments" tab
- Compare runs, metrics, parameters

**Advantages:**
- ✅ Cloud storage (no local setup)
- ✅ Team collaboration
- ✅ Version control integration
- ✅ Free for public repos
- ✅ Git-like workflow

**Pricing:**
- Free: Unlimited public projects
- Paid: Private projects ($9/month)

---

### MLflow Usage in Notebook

**Basic Example:**
```python
import mlflow
import mlflow.sklearn

# Set experiment
mlflow.set_experiment("Teen_Mental_Health_ML")

# Start a run
with mlflow.start_run(run_name="RandomForest_V1"):
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    
    # Log metrics
    mlflow.log_metric("train_auc", 0.92)
    mlflow.log_metric("test_auc", 0.88)
    mlflow.log_metric("f1_score", 0.85)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log artifacts (plots, files)
    mlflow.log_artifact("roc_curve.png")
    mlflow.log_artifact("feature_importance.csv")
```

**Compare Multiple Runs:**
```python
# Run 1
with mlflow.start_run(run_name="XGBoost"):
    mlflow.log_metric("auc", 0.91)

# Run 2
with mlflow.start_run(run_name="LightGBM"):
    mlflow.log_metric("auc", 0.93)

# View in MLflow UI and compare
```

---

## MongoDB Configuration

### What is MongoDB?
MongoDB is a NoSQL database for storing:
- Model predictions
- User data
- Experiment results
- Logs and metadata

### Option 1: Local MongoDB

**Installation (macOS):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Installation (Ubuntu/Linux):**
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongod
```

**Installation (Windows):**
1. Download: https://www.mongodb.com/try/download/community
2. Run installer
3. MongoDB starts automatically

**Installation (Docker):**
```bash
docker run -d -p 27017:27017 --name mongodb mongo
```

**Connection String:**
```python
MONGO_DB_URL = "mongodb://localhost:27017"
```

**Usage in Notebook:**
```python
from pymongo import MongoClient

client = MongoClient(os.environ['MONGO_DB_URL'])
db = client['teen_mental_health']
predictions = db['predictions']

# Insert prediction
predictions.insert_one({
    'timestamp': datetime.now(),
    'features': X.tolist(),
    'prediction': float(y_pred),
    'probability': float(y_pred_proba),
    'model': 'XGBoost'
})

# Query predictions
recent = predictions.find().limit(10)
```

**Advantages:**
- ✅ No account needed
- ✅ Works offline
- ✅ Unlimited storage
- ✅ Full data control

**Disadvantages:**
- ❌ Need to manage backups
- ❌ No team access without setup
- ❌ Technical setup required

---

### Option 2: MongoDB Atlas (Cloud)

**What is MongoDB Atlas?**
- Managed MongoDB service
- Automatic backups
- Built-in security
- Web dashboard

**Step 1: Create Account**
1. Visit: https://www.mongodb.com/cloud/atlas
2. Sign up with email or Google
3. Create free cluster (M0, 512MB storage)

**Step 2: Configure Security**
1. Go to Security > Network Access
2. Add IP Address (Allow Access from Anywhere: 0.0.0.0/0)
3. Go to Database Access
4. Create user with username/password

**Step 3: Get Connection String**
1. Click "Connect" on cluster
2. Select "Connect your application"
3. Copy connection string
4. Format: `mongodb+srv://username:password@cluster.mongodb.net/dbname`

**Step 4: In Google Colab**
```python
import os
os.environ['MONGO_DB_URL'] = 'mongodb+srv://username:password@cluster.mongodb.net/teen_mental_health'
```

**Step 5: Use in Notebook**
```python
from pymongo import MongoClient

client = MongoClient(os.environ['MONGO_DB_URL'])
db = client['teen_mental_health']
```

**Advantages:**
- ✅ No local setup
- ✅ Automatic backups
- ✅ Cloud accessibility
- ✅ Team collaboration
- ✅ Free tier available

**Free Tier Limits:**
- 512 MB storage
- Shared clusters
- 3 databases maximum

**Pricing:**
- Free: 512MB storage
- Paid: $9/month (10GB)

---

### MongoDB Usage Examples

**Insert Predictions:**
```python
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(os.environ['MONGO_DB_URL'])
db = client['teen_mental_health']
predictions_col = db['predictions']

# Insert single prediction
predictions_col.insert_one({
    'timestamp': datetime.now(),
    'model': 'XGBoost',
    'features': {'social_media_hours': 5.2, 'sleep_hours': 7.5},
    'prediction': 1,
    'probability': 0.92,
    'features_importance': {'social_media_hours': 0.35, 'sleep_hours': 0.28}
})

# Insert batch predictions
predictions_col.insert_many([
    {'timestamp': datetime.now(), 'model': 'RF', 'prediction': 0, 'probability': 0.45},
    {'timestamp': datetime.now(), 'model': 'LGB', 'prediction': 1, 'probability': 0.88}
])
```

**Query Predictions:**
```python
# Get all predictions
all_preds = list(predictions_col.find())

# Filter by model
xgb_preds = list(predictions_col.find({'model': 'XGBoost'}))

# Get recent predictions (last 24 hours)
from datetime import timedelta
recent = list(predictions_col.find({
    'timestamp': {'$gte': datetime.now() - timedelta(hours=24)}
}))

# Aggregation (average probability by model)
avg_by_model = list(predictions_col.aggregate([
    {'$group': {
        '_id': '$model',
        'avg_prob': {'$avg': '$probability'}
    }}
]))
```

**Update Predictions:**
```python
# Update single prediction
predictions_col.update_one(
    {'_id': prediction_id},
    {'$set': {'verified': True, 'actual_value': 1}}
)
```

**Delete Predictions:**
```python
# Delete old predictions (older than 30 days)
from datetime import timedelta
predictions_col.delete_many({
    'timestamp': {'$lt': datetime.now() - timedelta(days=30)}
})
```

---

## Google Colab Secrets

### What are Colab Secrets?
- Secure storage for sensitive credentials
- API keys, tokens, connection strings
- Environment variables injected at runtime
- Not visible in notebook output

### How to Add Secrets

**Method 1: Using Left Panel**
1. Click 🔑 icon on left sidebar
2. Click "Add new secret"
3. Name: `MLFLOW_TRACKING_URI`
4. Value: `https://dagshub.com/...`
5. Click "Add secret"

**Method 2: Using Code**
```python
from google.colab import userdata

# Get secret
token = userdata.get('MLFLOW_TRACKING_PASSWORD')

# Set environment variable
os.environ['MLFLOW_TRACKING_PASSWORD'] = token
```

### Required Secrets for This Project

**Minimal Setup (Local MLflow, No Database):**
- None required! 🎉

**With DagsHub MLflow:**
- `MLFLOW_TRACKING_URI`: https://dagshub.com/username/repo/mlflow
- `MLFLOW_TRACKING_USERNAME`: your_username
- `MLFLOW_TRACKING_PASSWORD`: your_pat_token

**With MongoDB:**
- `MONGO_DB_URL`: mongodb+srv://username:password@...

### Complete Setup Example
```python
import os
from google.colab import userdata

# MLflow
os.environ['MLFLOW_TRACKING_URI'] = userdata.get('MLFLOW_TRACKING_URI')
os.environ['MLFLOW_TRACKING_USERNAME'] = userdata.get('MLFLOW_TRACKING_USERNAME')
os.environ['MLFLOW_TRACKING_PASSWORD'] = userdata.get('MLFLOW_TRACKING_PASSWORD')

# MongoDB (optional)
try:
    os.environ['MONGO_DB_URL'] = userdata.get('MONGO_DB_URL')
except:
    os.environ['MONGO_DB_URL'] = 'mongodb://localhost:27017'  # Fallback

print("✅ Environment configured from secrets")
```

---

## DagsHub Integration

### Full Workflow

**Step 1: Initialize Repository**
```bash
# Create local repo
mkdir teen-mental-health-ml
cd teen-mental-health-ml
git init

# Add DagsHub remote
git remote add origin https://github.com/your_username/teen-mental-health-ml.git
```

**Step 2: Configure MLflow**
```python
import os
import mlflow

# Set MLflow URI
mlflow.set_tracking_uri('https://dagshub.com/your_username/teen-mental-health-ml/mlflow')
mlflow.set_experiment("Teen_Mental_Health_ML")

# Authenticate
os.environ['MLFLOW_TRACKING_USERNAME'] = 'your_username'
os.environ['MLFLOW_TRACKING_PASSWORD'] = 'your_personal_token'
```

**Step 3: Track Experiments**
```python
with mlflow.start_run(run_name="XGBoost_v1"):
    # Training code
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("auc", 0.95)
```

**Step 4: Push to Repository**
```bash
git add .
git commit -m "Add teen mental health ML pipeline"
git push origin main
```

**Step 5: View on DagsHub**
- Open: https://dagshub.com/username/teen-mental-health-ml
- Click "Experiments" tab
- Compare runs and metrics

---

## Environment Variables

### All Available Variables

```python
# MLflow Configuration
MLFLOW_TRACKING_URI          # Where to store experiments
MLFLOW_TRACKING_USERNAME     # DagsHub username
MLFLOW_TRACKING_PASSWORD     # Personal access token

# Database Configuration
MONGO_DB_URL                 # MongoDB connection string

# Project Directories (set by notebook)
WORK_DIR                     # Project root
DATA_DIR                     # Data folder
MODELS_DIR                   # Models folder
OUTPUTS_DIR                  # Outputs folder

# Random Seeds (for reproducibility)
PYTHONHASHSEED = 42
```

### Setting in Different Environments

**Google Colab:**
```python
from google.colab import userdata
os.environ['VAR_NAME'] = userdata.get('VAR_NAME')
```

**Local Python:**
```python
import os
os.environ['VAR_NAME'] = 'value'

# Or use .env file
from dotenv import load_dotenv
load_dotenv()
var_value = os.getenv('VAR_NAME')
```

**Jupyter Notebook:**
```python
import os
os.environ['VAR_NAME'] = 'value'
```

---

## Troubleshooting

### MLflow Connection Issues

**Problem**: "ConnectionError: Failed to connect to MLflow"
```
Solution:
1. Check MLFLOW_TRACKING_URI is correct
2. For local: Start MLflow UI (mlflow ui)
3. For DagsHub: Verify internet connection
4. Check credentials in environment variables
```

**Problem**: "Unauthorized 401" with DagsHub
```
Solution:
1. Regenerate personal access token
2. Check token has 'repo' permission
3. Verify username matches
4. Update environment variables
```

### MongoDB Connection Issues

**Problem**: "ServerSelectionTimeoutError"
```
Solution:
1. Verify MongoDB is running (local)
2. Check connection string format
3. For Atlas: Add IP to whitelist (0.0.0.0/0)
4. Verify username/password are correct
```

**Problem**: "AuthenticationFailed"
```
Solution:
1. Check username and password
2. Ensure special characters are URL-encoded
3. Verify database exists
4. Check user has access to database
```

### Colab Secrets Issues

**Problem**: "SecretNotFound"
```
Solution:
1. Ensure secret is added (🔑 icon)
2. Use exact secret name
3. Try to add secret again
4. Refresh page if needed
```

### General Issues

**Problem**: "No module named 'xgboost'"
```
Solution: Run Phase 0.1 (Install Dependencies)
```

**Problem**: "Out of memory"
```
Solution:
1. Reduce batch size (32 → 16)
2. Use CPU instead of GPU
3. Reduce model complexity
4. Close other Colab tabs
```

---

## Quick Reference

### Minimum Setup (Local Only)
No API keys needed! Just run the notebook.

### Recommended Setup (Team Collaboration)
1. Create DagsHub account (free)
2. Create repo
3. Add credentials to Colab Secrets
4. Run notebook

### Full Production Setup
1. DagsHub for ML tracking
2. MongoDB Atlas for data logging
3. GitHub for code version control
4. Automated retraining pipeline

### Cost Summary
| Service | Free Tier | Price |
|---------|-----------|-------|
| MLflow Local | ✅ Unlimited | $0 |
| DagsHub | ✅ Public | $9+/month |
| MongoDB Local | ✅ Unlimited | $0 |
| MongoDB Atlas | ✅ 512MB | $9+/month |
| Google Colab | ✅ 12h/session | $10+/month Pro |

---

**Last Updated**: May 2026
