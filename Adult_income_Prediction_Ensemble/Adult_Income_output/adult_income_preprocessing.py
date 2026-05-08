"""adult_income_preprocessing.py
Standalone preprocessing module.
Usage: from adult_income_preprocessing import preprocess
       X_train, X_test, y_train, y_test = preprocess(df)
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

COLUMNS = [
    'age','workclass','fnlwgt','education','education-num',
    'marital-status','occupation','relationship','race','gender',
    'capital-gain','capital-loss','hours-per-week','native-country','salary'
]

def preprocess(df, test_size=0.3, random_state=42):
    df = df.copy()
    if list(df.columns) != COLUMNS:
        df.columns = COLUMNS
    df = df.drop(['fnlwgt', 'education'], axis=1)
    df['marital-status'] = df['marital-status'].replace(
        [' Divorced',' Married-spouse-absent',' Never-married',' Separated',' Widowed'],'Single')
    df['marital-status'] = df['marital-status'].replace(
        [' Married-AF-spouse',' Married-civ-spouse'],'Couple')
    X = df.drop(['salary'], axis=1)
    y = (df['salary'].str.strip().isin(['>50K','>50K.'])).astype(int)
    cat_cols = [c for c in X.columns if X[c].dtype == 'object']
    for c in cat_cols:
        X[c] = np.where(X[c].str.strip() == '?', X[c].mode()[0], X[c])
    X = pd.concat([X, pd.get_dummies(X.select_dtypes(include='object'))], axis=1)
    X = X.drop(cat_cols, axis=1)
    return train_test_split(X, y, test_size=test_size,
                            random_state=random_state, stratify=y)