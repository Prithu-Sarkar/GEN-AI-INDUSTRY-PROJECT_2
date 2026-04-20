import pandas as pd

def two_stage_predict(cls, reg, applicant_df):
    # Stage 1: probability + hard approval decision
    proba = cls.predict_proba(applicant_df)
    preds = cls.predict(applicant_df)
    results = []
    for i in range(len(preds)):
        approved      = int(preds[i])
        approved_prob = float(proba[i, 1])
        reg_pred = None
        if approved == 1:
            # Regressor expects loan_status present (value seen during training)
            row_reg = applicant_df.iloc[[i]].copy()
            row_reg["loan_status"] = "Approved"
            reg_pred = float(reg.predict(row_reg)[0])
        results.append({"approved": approved, "approved_prob": approved_prob, "reg_pred": reg_pred})
    return results
