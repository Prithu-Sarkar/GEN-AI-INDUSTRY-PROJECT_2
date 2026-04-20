import yaml
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.loader import load_models
from app.utils import build_applicant_from_dict
from app.predict import two_stage_predict

st.set_page_config(page_title="Loan Approval Predictor", page_icon="🏦", layout="wide")

@st.cache_resource
def get_models():
    with open("config.yaml") as f:
        cfg = yaml.safe_load(f)
    return load_models(cfg), cfg

(cls, reg), config = get_models()
defaults = config["ui"]["default_inputs"]

# Sidebar
with st.sidebar:
    st.title("🏦 Loan Predictor")
    st.markdown("---")
    st.subheader("Model Info")
    st.markdown("**Stage 1:** Random Forest Classifier")
    st.markdown("**Stage 2:** Random Forest Regressor")
    try:
        st.caption(f"Classifier features: {len(cls.feature_names_in_)}")
        with st.expander("Show feature names"):
            for feat in cls.feature_names_in_:
                st.text(f"- {feat}")
    except Exception:
        st.caption("Feature names unavailable")
    st.markdown("---")
    st.subheader("How it works")
    st.markdown("1. **Stage 1**: Classifier decides Approved/Rejected + probability.")
    st.markdown("2. **Stage 2**: If approved, Regressor predicts sanctioned loan amount.")

# Main
st.title("🏦 Loan Approval -- Two-Stage Predictor")
st.markdown("Fill in the applicant details and click **Predict**.")
st.markdown("---")
st.subheader("Applicant Details")
col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Personal Info")
    no_of_dependents = st.number_input("No. of Dependents", min_value=0, max_value=10, value=int(defaults["no_of_dependents"]), step=1)
    education = st.selectbox("Education", ["Graduate", "Not Graduate"], index=0 if defaults["education"]=="Graduate" else 1)
    self_employed = st.selectbox("Self Employed", ["Yes", "No"], index=0 if defaults["self_employed"]=="Yes" else 1)
    income_annum = st.number_input("Annual Income", min_value=0.0, value=float(defaults["income_annum"]), step=10000.0)
    cibil_score = st.number_input("CIBIL Score", min_value=300, max_value=900, value=int(defaults["cibil_score"]), step=1)

with col2:
    st.markdown("##### Asset & Loan Info")
    loan_amount = st.number_input("Loan Amount Requested", min_value=0.0, value=float(defaults["loan_amount"]), step=10000.0)
    loan_term = st.number_input("Loan Term (years)", min_value=1, max_value=30, value=int(defaults["loan_term"]), step=1)
    residential_assets_value = st.number_input("Residential Assets", min_value=0.0, value=float(defaults["residential_assets_value"]), step=50000.0)
    commercial_assets_value = st.number_input("Commercial Assets", min_value=0.0, value=float(defaults["commercial_assets_value"]), step=50000.0)
    luxury_assets_value = st.number_input("Luxury Assets", min_value=0.0, value=float(defaults["luxury_assets_value"]), step=10000.0)
    bank_asset_value = st.number_input("Bank Asset Value", min_value=0.0, value=float(defaults["bank_asset_value"]), step=5000.0)

st.markdown("---")

if st.button("🔮 Predict", type="primary", use_container_width=True):
    applicant = {
        "no_of_dependents":         no_of_dependents,
        "education":                education,
        "self_employed":            self_employed,
        "income_annum":             income_annum,
        "loan_amount":              loan_amount,
        "loan_term":                loan_term,
        "cibil_score":              cibil_score,
        "residential_assets_value": residential_assets_value,
        "commercial_assets_value":  commercial_assets_value,
        "luxury_assets_value":      luxury_assets_value,
        "bank_asset_value":         bank_asset_value,
    }
    try:
        expected_cols = list(cls.feature_names_in_)
        applicant_df  = build_applicant_from_dict(applicant, expected_cols)
        results       = two_stage_predict(cls, reg, applicant_df)
        res           = results[0]
        prob = res["approved_prob"]
        st.markdown("---")
        st.subheader("Prediction Result")
        r_col, g_col = st.columns([1, 2])
        with r_col:
            fig, ax = plt.subplots(figsize=(3, 2), subplot_kw=dict(aspect="equal"))
            color = "#28a745" if res["approved"]==1 else "#dc3545"
            ax.pie([prob, 1-prob], colors=[color, "#e9ecef"], startangle=180, counterclock=False, wedgeprops=dict(width=0.4))
            ax.text(0, -0.15, f"{prob:.1%}", ha="center", va="center", fontsize=18, fontweight="bold", color=color)
            ax.set_title("Approval Probability", fontsize=10)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        with g_col:
            if res["approved"] == 1:
                st.success("✅  APPROVED")
                st.metric("Predicted Sanctioned Amount", f"Rs {res['reg_pred']:, .0f}")
                st.metric("Requested Amount", f"Rs {loan_amount:,.0f}", delta=f"Rs {res['reg_pred'] - loan_amount:,.0f}")
            else:
                st.error("❌  REJECTED")
                st.write("Application did not meet approval criteria.")
                st.caption("Tip: improve CIBIL score, reduce loan amount, or increase income/assets.")
        with st.expander("Full input summary"):
            st.dataframe(pd.DataFrame([applicant]).T.rename(columns={0: "Value"}), use_container_width=True)
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.exception(e)
