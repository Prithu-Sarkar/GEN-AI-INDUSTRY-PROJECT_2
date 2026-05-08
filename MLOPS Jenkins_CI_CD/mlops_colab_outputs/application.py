from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

model  = joblib.load("artifacts/models/model.pkl")
scaler = joblib.load("artifacts/processed/scaler.pkl")

FEATURES = [
    "Operation_Mode", "Temperature_C", "Vibration_Hz",
    "Power_Consumption_kW", "Network_Latency_ms", "Packet_Loss_%",
    "Quality_Control_Defect_Rate_%", "Production_Speed_units_per_hr",
    "Predictive_Maintenance_Score", "Error_Rate_%",
    "Year", "Month", "Day", "Hour"
]

LABELS = {0: "High", 1: "Low", 2: "Medium"}

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        try:
            input_data = [float(request.form[f]) for f in FEATURES]
            scaled     = scaler.transform([input_data])
            pred       = model.predict(scaled)[0]
            prediction = LABELS.get(pred, "Unknown")
        except Exception as e:
            prediction = f"Error: {e}"
    return render_template("index.html", prediction=prediction, features=FEATURES)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)