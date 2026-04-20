import pandas as pd

def build_applicant_from_dict(d, expected_cols):
    # Convert raw dict to model-ready DataFrame with correct column order
    df = pd.DataFrame([d])
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing input columns: {missing}")
    return df[expected_cols]
