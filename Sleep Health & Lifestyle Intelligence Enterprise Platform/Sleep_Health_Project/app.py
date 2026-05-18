"""
Sleep Health Intelligence Platform — Streamlit Deployment App
============================================================
Usage: streamlit run app.py
"""
import os, json, pickle, warnings
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import datetime
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Sleep Health Intelligence Platform",
                   page_icon="🧠", layout="wide")

@st.cache_resource
def load_artifacts():
    return {
        'model':    pickle.load(open('models/best_model.pkl','rb')),
        'encoders': pickle.load(open('models/label_encoders.pkl','rb')),
        'target':   pickle.load(open('models/target_encoder.pkl','rb')),
        'meta':     json.load(open('configs/feature_metadata.json')),
        'card':     json.load(open('models/model_card.json')),
    }

def preprocess(inp, encoders, feature_names):
    d = pd.DataFrame([inp])
    bp = str(inp.get('Blood Pressure','120/80')).split('/')
    d['Systolic_BP']  = int(bp[0]); d['Diastolic_BP'] = int(bp[1] if len(bp)>1 else 80)
    d['Pulse_Pressure']= d['Systolic_BP'] - d['Diastolic_BP']
    d['BP_Ratio']  = (d['Systolic_BP']/d['Diastolic_BP']).round(3)
    d['MAP']       = ((d['Systolic_BP']+2*d['Diastolic_BP'])/3).round(1)
    s,di = int(d['Systolic_BP'].iloc[0]), int(d['Diastolic_BP'].iloc[0])
    if s>=180 or di>=120:      d['BP_Category']='Hypertensive Crisis'
    elif s>=140 or di>=90:     d['BP_Category']='Hypertension Stage 2'
    elif s>=130 or di>=80:     d['BP_Category']='Hypertension Stage 1'
    elif 120<=s<130 and di<80: d['BP_Category']='Elevated'
    else:                      d['BP_Category']='Normal'
    d['BMI_WHO'] = {'Normal Weight':'Normal','Normal':'Normal',
                    'Overweight':'Overweight','Obese':'Obese'}.get(inp.get('BMI Category','Normal'),'Normal')
    stress=float(inp['Stress Level']); sl=float(inp['Sleep Duration'])
    bmi_n = {'Normal':0,'Overweight':1,'Obese':2}.get(d['BMI_WHO'].iloc[0],1)
    d['Stress_Sleep_Index']    = stress/max(sl,0.1)
    d['Activity_Efficiency']   = float(inp['Daily Steps'])/max(float(inp['Physical Activity Level']),1)
    d['Sleep_Debt']            = max(0,8.0-sl)
    d['Wellness_Score']        = (float(inp['Quality of Sleep'])/10*25+(1-stress/10)*25+
                                   min(float(inp['Physical Activity Level'])/90,1)*25+
                                   min(float(inp['Daily Steps'])/10000,1)*25)
    d['Cardio_Risk_Index']     = d['Systolic_BP']/140+float(inp['Heart Rate'])/100+bmi_n/2
    d['Age_Stress_Interaction']= float(inp['Age'])*stress
    d['Sleep_Activity_Synergy']= sl*float(inp['Physical Activity Level'])/100
    d['HTN_Risk']              = int(s>=130 or di>=80)
    d['BMI_Stress_Risk']       = bmi_n*stress
    d['Age_Cohort'] = pd.cut([float(inp['Age'])],bins=[0,30,40,50,100],labels=['20s','30s','40s','50+'])[0]
    d['Sleep_Quality_Cat']=pd.cut([float(inp['Quality of Sleep'])],bins=[0,4,6,8,10],
                                   labels=['Poor','Fair','Good','Excellent'],include_lowest=True)[0]
    for col,le in encoders.items():
        src_val = d[col].astype(str).iloc[0] if col in d.columns else 'Unknown'
        try:    d[f'{col}_enc'] = le.transform([src_val])[0]
        except: d[f'{col}_enc'] = 0
    for feat in feature_names:
        if feat not in d.columns: d[feat] = 0
    return d[feature_names].fillna(0)

def main():
    arts = load_artifacts()
    card = arts['card']

    # Header
    st.title("🧠 Sleep Health Intelligence Platform")
    st.markdown(f"**Model:** `{card['model_name']}` | **Version:** {card['version']} | "
                f"**Classes:** {', '.join(card['classes'])}")
    st.warning("⚠️  Research prototype — not validated for clinical decision-making.")
    st.divider()

    col_input, col_result = st.columns([1, 1])

    with col_input:
        st.subheader("📋 Patient Health Metrics")
        age      = st.slider("Age", 18, 80, 35)
        gender   = st.selectbox("Gender", ["Male","Female"])
        occ      = st.selectbox("Occupation", ["Engineer","Doctor","Nurse","Teacher",
                                               "Accountant","Lawyer","Salesperson","Manager","Scientist"])
        st.markdown("---")
        sleep_dur = st.slider("Sleep Duration (hours)", 4.0, 10.0, 7.0, 0.1)
        sleep_q   = st.slider("Quality of Sleep (1-10)", 1, 10, 7)
        stress    = st.slider("Stress Level (1-10)", 1, 10, 5)
        activity  = st.slider("Physical Activity (min/day)", 10, 120, 45)
        steps     = st.slider("Daily Steps", 1000, 15000, 7000, 500)
        st.markdown("---")
        bmi_cat  = st.selectbox("BMI Category", ["Normal","Normal Weight","Overweight","Obese"])
        systolic = st.slider("Systolic BP (mmHg)", 90, 200, 120)
        diastolic= st.slider("Diastolic BP (mmHg)", 60, 130, 80)
        hr       = st.slider("Heart Rate (bpm)", 50, 120, 72)

        predict_btn = st.button("🔮 Predict Sleep Disorder Risk", type="primary", use_container_width=True)

    with col_result:
        st.subheader("🎯 Prediction Results")
        if predict_btn:
            inp = {
                'Age':age,'Gender':gender,'Occupation':occ,
                'Sleep Duration':sleep_dur,'Quality of Sleep':sleep_q,
                'Physical Activity Level':activity,'Stress Level':stress,
                'BMI Category':bmi_cat,'Blood Pressure':f"{systolic}/{diastolic}",
                'Heart Rate':hr,'Daily Steps':steps,
            }
            Xi = preprocess(inp, arts['encoders'], arts['meta']['feature_names'])
            pred_enc = arts['model'].predict(Xi)[0]
            probas   = arts['model'].predict_proba(Xi)[0]
            pred     = arts['target'].classes_[pred_enc]
            prob_d   = {c:float(p) for c,p in zip(arts['target'].classes_,probas)}
            conf     = max(prob_d.values())
            if pred=='None' and conf>0.8:   risk='🟢 LOW'
            elif pred=='None':               risk='🟡 MEDIUM'
            elif conf>0.7:                   risk='🔴 HIGH'
            else:                            risk='🟡 MEDIUM'

            # Results display
            color = {'None':'green','Insomnia':'orange','Sleep Apnea':'red'}.get(pred,'gray')
            st.markdown(f"### Predicted: **:{color}[{pred}]**")
            st.metric("Confidence", f"{conf:.1%}")
            st.metric("Risk Tier", risk)

            st.markdown("**Class Probabilities:**")
            for cls,p in sorted(prob_d.items(), key=lambda x:-x[1]):
                st.progress(p, text=f"{cls}: {p:.1%}")

            wellness = float(steps)/10000*25 + (1-stress/10)*25 + min(activity/90,1)*25 + (sleep_q/10)*25
            st.metric("Wellness Score", f"{wellness:.0f}/100")

            st.markdown("**Recommendations:**")
            recs = {
                'None':['✅ Maintain current sleep schedule','✅ Continue physical activity','🔁 Annual screening'],
                'Insomnia':['💊 CBT-I therapy (first-line)','📵 Reduce screen time before bed',
                            '🧘 Stress management program','👨‍⚕️ Consult sleep specialist'],
                'Sleep Apnea':['🏥 Polysomnography study recommended','😮‍💨 CPAP therapy evaluation',
                               '⚖️ Weight management program','👃 ENT specialist referral']
            }
            for r in recs.get(pred,[]):
                st.markdown(f"  {r}")

    st.divider()
    st.markdown(f"*Model: `{card['model_name']}` | Features: {card['n_features']} | "
                f"Classes: {card['classes']} | Version: {card['version']}*")

if __name__ == '__main__':
    main()
