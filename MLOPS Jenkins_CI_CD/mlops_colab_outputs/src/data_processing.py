import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class DataProcessing:
    def __init__(self, input_path, output_path):
        self.input_path  = input_path
        self.output_path = output_path
        self.df          = None
        self.features    = None
        os.makedirs(self.output_path, exist_ok=True)
        logger.info("DataProcessing initialized.")

    def load_data(self):
        try:
            self.df = pd.read_csv(self.input_path)
            logger.info(f"Data loaded: {self.df.shape[0]} rows, {self.df.shape[1]} cols")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise CustomException("Failed to load data", e)

    def preprocess(self):
        try:
            # Drop rows with NaN in target variable before further processing
            initial_rows = self.df.shape[0]
            self.df.dropna(subset=['Efficiency_Status'], inplace=True)
            if self.df.shape[0] < initial_rows:
                logger.warning(f"Dropped {initial_rows - self.df.shape[0]} rows with NaN in 'Efficiency_Status'.")

            self.df["Timestamp"] = pd.to_datetime(self.df["Timestamp"], errors="coerce")
            self.df["Year"]  = self.df["Timestamp"].dt.year
            self.df["Month"] = self.df["Timestamp"].dt.month
            self.df["Day"]   = self.df["Timestamp"].dt.day
            self.df["Hour"]  = self.df["Timestamp"].dt.hour
            self.df.drop(columns=["Timestamp", "Machine_ID"], inplace=True)
            for col in ["Efficiency_Status", "Operation_Mode"]:
                le = LabelEncoder()
                self.df[col] = le.fit_transform(self.df[col])
            logger.info("Preprocessing complete.")
        except Exception as e:
            logger.error(f"Error preprocessing: {e}")
            raise CustomException("Failed to preprocess data", e)

    def split_and_scale_and_save(self):
        try:
            self.features = [
                "Operation_Mode", "Temperature_C", "Vibration_Hz",
                "Power_Consumption_kW", "Network_Latency_ms", "Packet_Loss_%",
                "Quality_Control_Defect_Rate_%", "Production_Speed_units_per_hr",
                "Predictive_Maintenance_Score", "Error_Rate_%",
                "Year", "Month", "Day", "Hour"
            ]
            X = self.df[self.features]
            y = self.df["Efficiency_Status"]
            # Debug print to check value counts of y before splitting
            print(f"DEBUG: Value counts for y before train_test_split:
{y.value_counts()}")
            scaler   = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42, stratify=y
            )
            for name, obj in [("X_train", X_train), ("X_test", X_test),
                               ("y_train", y_train), ("y_test", y_test),
                               ("scaler", scaler)]:
                joblib.dump(obj, os.path.join(self.output_path, f"{name}.pkl"))
            logger.info("Train/test splits and scaler saved.")
        except Exception as e:
            logger.error(f"Error in split_and_scale_and_save: {e}")
            raise CustomException("Failed to split/scale/save data", e)

    def run(self):
        self.load_data()
        self.preprocess()
        self.split_and_scale_and_save()

if __name__ == "__main__":
    DataProcessing("artifacts/raw/data.csv", "artifacts/processed").run()