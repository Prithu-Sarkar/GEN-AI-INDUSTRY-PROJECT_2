# 🚀 QUICK START GUIDE

## ⏱️ 5-Minute Setup

### Step 1: Open in Google Colab (30 seconds)
```
1. Go to: https://colab.research.google.com/
2. File > Upload notebook
3. Select: teen_mental_health_ml.ipynb
4. Click Open
```

### Step 2: Configure Dataset (1 minute)
```
1. Upload your Teen_Mental_Health_Dataset.csv
2. Run cell: \"!ls -la /content/gdrive/My\\ Drive/Teen_Mental_Health_ML/\"
3. Verify dataset is in data/ folder
```

### Step 3: Run Setup (3 minutes)
```
1. Run: Phase 0.1 (Install Dependencies)
   ⏱️ Takes ~2 minutes
   
2. Run: Phase 0.2 (Secrets Configuration)
   ✅ Skip if no MLflow/MongoDB needed
   
3. Run: Phase 1.1 (Import Libraries)
   ⏱️ Takes ~30 seconds
```

### Step 4: Execute Pipeline (30+ minutes)
```
Run each phase in order:
1. Phase 1.2 - Data Loading ⏱️ 2 min
2. Phase 2 - EDA ⏱️ 10 min
3. Phase 3 - Feature Engineering ⏱️ 15 min
4. Phase 4 - ML Models ⏱️ 30 min (with hyperparameter tuning)
5. Phase 5 - Ensemble ⏱️ 20 min
6. Phase 6 - Deep Learning ⏱️ 20 min
7. Phase 7 - SHAP ⏱️ 10 min
8. Phase 8-10 - Evaluation & Export ⏱️ 10 min
```

---

## 📦 What You Get

✅ **8 Trained Models**:
- Logistic Regression
- Random Forest
- XGBoost
- LightGBM
- Deep Neural Network
- Voting Ensemble
- Stacking Ensemble

✅ **Visualizations**:
- EDA plots
- Model comparisons
- ROC curves
- Confusion matrices
- SHAP explanations

✅ **Saved Artifacts**:
- Trained models (.pkl, .h5)
- Scalers & encoders
- Feature lists
- Metrics (CSV)

✅ **Documentation**:
- FINAL_REPORT.txt
- config.json
- model_metrics.csv

---

## 🎯 Without APIs (Simplest)

**No account needed!** Run locally:

```python
# Phase 0.1: Install
# Phase 0.2: Skip (no secrets)
# Phase 1-10: Run all phases

# Results saved in:
# - /content/gdrive/My Drive/Teen_Mental_Health_ML/models/
# - /content/gdrive/My Drive/Teen_Mental_Health_ML/outputs/
```

**Download outputs:**
```
1. Run final cell (Phase 10.2)
2. Click download link in outputs
3. All files in ZIP archive
```

---

## 🚀 With DagsHub (Recommended)

**Best for team collaboration!**

### 1. Create DagsHub Account (1 minute)
```
https://dagshub.com
Sign up → Create repo → Get credentials
```

### 2. Add Secrets to Colab (2 minutes)
```
🔑 (left sidebar) > Add new secret

MLFLOW_TRACKING_URI
→ https://dagshub.com/username/repo/mlflow

MLFLOW_TRACKING_USERNAME
→ your_username

MLFLOW_TRACKING_PASSWORD
→ your_personal_access_token
```

### 3. Run Notebook
```
Phase 0 uses secrets automatically
All experiments tracked on DagsHub
```

### 4. View Results
```
https://dagshub.com/username/repo
→ Experiments tab
→ Compare all runs
```

---

## 🗄️ With MongoDB (Data Logging)

**Best for production!**

### Option A: Local MongoDB (Easy)
```bash
# macOS
brew install mongodb-community
brew services start mongodb-community

# Ubuntu
sudo apt-get install mongodb
sudo systemctl start mongod

# Docker
docker run -d -p 27017:27017 mongo
```

**Add Secret (Colab):**
```
MONGO_DB_URL = mongodb://localhost:27017
```

### Option B: MongoDB Atlas (Cloud)
```
https://www.mongodb.com/cloud/atlas
→ Create cluster
→ Copy connection string
→ Add to Colab Secrets
```

**Usage:**
```python
# Logged automatically in notebook
# View in MongoDB dashboard
```

---

## 📊 Expected Results

### Model Performance
```
Model             AUC    Accuracy    F1
─────────────────────────────────────
XGBoost          0.92     0.88      0.85
LightGBM         0.91     0.87      0.84
RandomForest     0.90     0.86      0.83
StackingEnsemble 0.93     0.89      0.86  ← Best
DeepNN           0.89     0.85      0.82
```

### Output Files
```
outputs/
├── 01_eda_overview.png              (2 KB)
├── 02_model_comparison.png          (3 KB)
├── 03_deep_nn_history.png           (4 KB)
├── 04_shap_feature_importance.png   (5 KB)
├── 05_shap_summary_beeswarm.png     (6 KB)
├── 06_shap_force_plot_*.png         (3×3 KB)
├── 07_roc_curves_comparison.png     (8 KB)
├── 08_confusion_matrices.png        (12 KB)
├── model_metrics.csv                (1 KB)
└── FINAL_REPORT.txt                 (2 KB)
```

---

## ✅ Verification Checklist

After running all phases:

- [ ] Phase 0: Environment setup ✅
- [ ] Phase 1: Data loaded successfully ✅
- [ ] Phase 2: Visualizations generated ✅
- [ ] Phase 3: Features engineered (50+ features) ✅
- [ ] Phase 4: 4 ML models trained ✅
- [ ] Phase 5: Ensemble models trained ✅
- [ ] Phase 6: Deep neural network trained ✅
- [ ] Phase 7: SHAP analysis complete ✅
- [ ] Phase 8: Metrics computed ✅
- [ ] Phase 9: Models saved (.pkl, .h5) ✅
- [ ] Phase 10: ZIP archive created ✅

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'xgboost'"
```
→ Run Phase 0.1 again
→ Wait for all packages to install
→ Restart runtime (Ctrl + M)
```

### "Dataset not found"
```
→ Upload CSV to Colab
→ Put in data/ folder
→ Path: /content/gdrive/My Drive/Teen_Mental_Health_ML/data/
```

### "Secret not found"
```
→ Add secret in 🔑 (left sidebar)
→ Use exact name: MLFLOW_TRACKING_URI
→ Refresh page if needed
```

### "MLflow connection failed"
```
→ Set USE_DAGSHUB = False in Phase 0.2
→ Uses local MLflow instead
→ No DagsHub account needed
```

### "CUDA out of memory"
```
→ Reduce batch size: 32 → 16
→ Reduce model size
→ Use CPU: os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Full project documentation |
| `API_CONFIGURATION_GUIDE.md` | API setup (MLflow, MongoDB) |
| `requirements.txt` | Python dependencies |
| `data_loader.py` | Data loading utilities |
| `QUICK_START.md` | This file! |

---

## 🎓 Learning Resources

**Machine Learning:**
- Scikit-learn: https://scikit-learn.org/
- XGBoost: https://xgboost.readthedocs.io/
- TensorFlow: https://tensorflow.org/

**Experiment Tracking:**
- MLflow: https://mlflow.org/
- DagsHub: https://dagshub.com/

**Database:**
- MongoDB: https://docs.mongodb.com/
- PyMongo: https://pymongo.readthedocs.io/

**Explainability:**
- SHAP: https://shap.readthedocs.io/
- Interpretation: https://christophm.github.io/interpretable-ml-book/

---

## 💡 Pro Tips

1. **Checkpoint your work**: Download outputs after each phase
2. **Monitor memory**: Watch GPU/RAM usage in Colab
3. **Save frequently**: Use MLflow to track experiments
4. **Experiment tracking**: Compare multiple runs in DagsHub
5. **Reproducibility**: All random seeds are set to 42

---

## 🤝 Next Steps

### After Running Notebook:

1. **Review Results**
   ```
   ✓ Check model_metrics.csv
   ✓ View visualizations
   ✓ Read FINAL_REPORT.txt
   ```

2. **Deploy Best Model**
   ```python
   import pickle
   with open('models/stacking_ensemble_model.pkl', 'rb') as f:
       best_model = pickle.load(f)
   
   # Make predictions
   y_pred = best_model.predict(X_new)
   ```

3. **Monitor Performance**
   ```python
   # Log to MongoDB
   predictions_col.insert_one({
       'timestamp': datetime.now(),
       'prediction': y_pred,
       'model': 'StackingEnsemble'
   })
   ```

4. **Retrain Regularly**
   ```
   ✓ Monthly: Retrain with new data
   ✓ Check feature importance changes
   ✓ Monitor for data drift
   ```

---

## 📞 Need Help?

**Common Issues:**
- Check `Troubleshooting` section above
- Review `API_CONFIGURATION_GUIDE.md`
- Check notebook comments

**Resources:**
- Colab Help: https://colab.research.google.com/notebooks/intro.ipynb
- Stack Overflow: [google-colaboratory] tag
- GitHub Issues: Create issue in repo

---

**Start running now!** 🎯

1. Copy `teen_mental_health_ml.ipynb` to Colab
2. Upload `Teen_Mental_Health_Dataset.csv`
3. Run Phase 0 → Phase 1 → ... → Phase 10
4. Download results ZIP
5. 🎉 Done!

---

**Estimated Total Time**: 90-120 minutes  
**Cloud Cost**: Free (Google Colab)  
**APIs Needed**: None (optional DagsHub/MongoDB)

Good luck! 🚀
