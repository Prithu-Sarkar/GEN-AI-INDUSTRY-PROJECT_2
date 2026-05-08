"""adult_income_train.py — retrain the final model from scratch."""
import joblib, json, os
import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score
from adult_income_preprocessing import preprocess

df = pd.read_csv('adult11.csv')
X_train, X_test, y_train, y_test = preprocess(df)

with open('adult_income_outputs/09_best_hyperparams.json') as f:
    params = json.load(f)

scale_pos = (y_train == 0).sum() / (y_train == 1).sum()
model = xgb.XGBClassifier(**params, scale_pos_weight=scale_pos,
                           eval_metric='logloss', random_state=42, n_jobs=-1)
model.fit(X_train, y_train)
acc = accuracy_score(y_test, model.predict(X_test))
print(f'Test accuracy: {acc:.4f}')
joblib.dump(model, 'adult_income_outputs/final_model.pkl')