# streamlit_app.py — Telecom Customer Churn Prediction UI

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler


@st.cache_data
def load_data(path: str = 'Customer-Churn.csv') -> pd.DataFrame:
    """Load the raw customer churn CSV dataset."""
    return pd.read_csv(path)


@st.cache_resource
def build_preprocessor(df: pd.DataFrame) -> dict:
    """Replicate training preprocessing to build a fitted StandardScaler."""
    telco = df.copy()
    telco['TotalCharges'] = pd.to_numeric(telco['TotalCharges'], errors='coerce')
    telco.dropna(how='any', inplace=True)

    bins   = [0, 12, 24, 36, 48, 60, 72]
    labels = ['1-12', '13-24', '25-36', '37-48', '49-60', '61-72']
    telco['tenure_bin'] = pd.cut(telco['tenure'], bins=bins,
                                  labels=labels, include_lowest=True)

    X_template = telco.drop(columns=['customerID', 'Churn', 'tenure'])
    X_template = pd.get_dummies(X_template, drop_first=True)

    scaler = StandardScaler()
    scaler.fit(X_template)

    return {
        'template_columns': list(X_template.columns),
        'scaler':           scaler,
        'tenure_bins':      (bins, labels),
        'sample_df':        telco,
    }


def preprocess_input(user_input: dict, prep: dict) -> np.ndarray:
    """Transform raw customer features into a scaled vector for inference."""
    df_in = pd.DataFrame([user_input])

    bins, labels = prep['tenure_bins']
    df_in['tenure_bin'] = pd.cut(df_in['tenure'], bins=bins,
                                  labels=labels, include_lowest=True)
    df_in = df_in.drop(columns=['tenure'])

    df_enc = pd.get_dummies(df_in, drop_first=True)
    df_enc = df_enc.reindex(columns=prep['template_columns'], fill_value=0)

    return prep['scaler'].transform(df_enc)


@st.cache_resource
def load_model(path: str = 'ada_boost_churn_model.pkl'):
    """Load the serialised churn prediction model."""
    return joblib.load(path)


def main():
    st.set_page_config(page_title='Churn Prediction', layout='centered')
    st.title('Telecom Customer Churn Prediction')

    df    = load_data()
    prep  = build_preprocessor(df)
    model = load_model()

    st.markdown('### Enter customer details to predict churn probability')

    sample  = prep['sample_df']
    exclude = {'customerID', 'Churn', 'tenure', 'tenure_bin'}

    with st.form('input_form'):
        tenure = st.slider(
            'Tenure (months)',
            min_value=int(sample['tenure'].min()),
            max_value=int(sample['tenure'].max()),
            value=12,
        )
        user_input = {'tenure': tenure}

        for col in [c for c in sample.columns if c not in exclude]:
            if sample[col].dtype == 'object' or str(sample[col].dtype) == 'category':
                opts = sorted(sample[col].dropna().unique().tolist())
                user_input[col] = st.selectbox(col, opts)
            else:
                is_int  = pd.api.types.is_integer_dtype(sample[col])
                minv    = int(sample[col].min())    if is_int else float(sample[col].min())
                maxv    = int(sample[col].max())    if is_int else float(sample[col].max())
                default = int(sample[col].median()) if is_int else float(sample[col].median())
                user_input[col] = st.number_input(col, value=default,
                                                   min_value=minv, max_value=maxv)

        submitted = st.form_submit_button('Predict')

    if submitted:
        X_in       = preprocess_input(user_input, prep)
        pred_proba = model.predict_proba(X_in)[0][1]
        pred_class = model.predict(X_in)[0]

        st.write('### Prediction Result')
        st.metric('Churn', 'Yes' if pred_class == 1 else 'No')
        st.metric('Churn Probability', f'{pred_proba:.2%}')

        if st.checkbox('Show debug info'):
            bins, labels = prep['tenure_bins']
            df_dbg = pd.DataFrame([user_input])
            df_dbg['tenure_bin'] = pd.cut(
                df_dbg['tenure'], bins=bins, labels=labels, include_lowest=True
            )
            df_dbg  = df_dbg.drop(columns=['tenure'])
            df_enc  = pd.get_dummies(df_dbg, drop_first=True)
            df_rix  = df_enc.reindex(columns=prep['template_columns'], fill_value=0)
            st.write('Raw input', user_input)
            st.write('One-hot encoded', df_enc)
            st.write('Reindexed (model features)', df_rix)
            st.write('Scaled features (first 20)', X_in.flatten()[:20].tolist())

        st.success('Prediction complete')

    st.caption(
        'Preprocessing mirrors training notebook: tenure is binned into tenure_bin, '
        'categoricals one-hot encoded with drop_first=True, StandardScaler applied.'
    )


if __name__ == '__main__':
    main()
