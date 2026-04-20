import yaml
from app.loader import load_models
from app.utils import build_applicant_from_dict
from app.predict import two_stage_predict

def get_float(prompt, default):
    raw = input(f"{prompt} [{default}]: ").strip()
    return float(raw) if raw else float(default)

def get_str(prompt, options, default):
    raw = input(f"{prompt} ({chr(47).join(options)}) [{default}]: ").strip()
    return raw if raw in options else default

def run_cli():
    config   = yaml.safe_load(open("config.yaml"))
    cls, reg = load_models(config)
    d        = config["ui"]["default_inputs"]
    print("Loan Approval Predictor (CLI)")
    data = {
        "no_of_dependents":         get_float("No. of dependents",     d["no_of_dependents"])),
        "education":                get_str("Education",               ["Graduate","Not Graduate"], d["education"])),
        "self_employed":            get_str("Self employed",           ["Yes","No"], d["self_employed"])),
        "income_annum":             get_float("Annual income",         d["income_annum"])),
        "loan_amount":              get_float("Loan amount requested", d["loan_amount"])),
        "loan_term":                get_float("Loan term (years)",     d["loan_term"])),
        "cibil_score":              get_float("CIBIL score",           d["cibil_score"])),
        "residential_assets_value": get_float("Residential assets",   d["residential_assets_value"])),
        "commercial_assets_value":  get_float("Commercial assets",    d["commercial_assets_value"])),
        "luxury_assets_value":      get_float("Luxury assets",        d["luxury_assets_value"])),
        "bank_asset_value":         get_float("Bank asset value",     d["bank_asset_value"])),
    }
    df  = build_applicant_from_dict(data, list(cls.feature_names_in_))
    res = two_stage_predict(cls, reg, df)[0]
    print(f"Approval probability: {res['approved_prob']:.2%}")
    if res["approved"] == 1:
        print("Decision: APPROVED")
        print(f"Predicted loan amount: {res['reg_pred']:.2f}")
    else:
        print("Decision: REJECTED")

if __name__ == "__main__":
    run_cli()
