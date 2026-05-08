import os
import joblib
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, processed_data_path, model_output_path):
        self.processed_path = processed_data_path
        self.model_path     = model_output_path
        self.clf            = None
        self.metrics        = {}
        self.X_train = self.X_test = self.y_train = self.y_test = None
        os.makedirs(self.model_path, exist_ok=True)
        logger.info("ModelTraining initialized.")

    def load_data(self):
        try:
            self.X_train = joblib.load(os.path.join(self.processed_path, "X_train.pkl"))
            self.X_test  = joblib.load(os.path.join(self.processed_path, "X_test.pkl"))
            self.y_train = joblib.load(os.path.join(self.processed_path, "y_train.pkl"))
            self.y_test  = joblib.load(os.path.join(self.processed_path, "y_test.pkl"))
            logger.info(f"Train: {len(self.X_train)} | Test: {len(self.X_test)}")
        except Exception as e:
            raise CustomException("Failed to load processed data", e)

    def train_model(self):
        try:
            self.clf = LogisticRegression(random_state=42, max_iter=1000)
            self.clf.fit(self.X_train, self.y_train)
            joblib.dump(self.clf, os.path.join(self.model_path, "model.pkl"))
            logger.info("Model trained and saved.")
        except Exception as e:
            raise CustomException("Failed to train model", e)

    def evaluate_model(self):
        try:
            y_pred = self.clf.predict(self.X_test)
            self.metrics = {
                "accuracy":  round(accuracy_score(self.y_test, y_pred), 4),
                "precision": round(precision_score(self.y_test, y_pred, average="weighted"), 4),
                "recall":    round(recall_score(self.y_test, y_pred, average="weighted"), 4),
                "f1_score":  round(f1_score(self.y_test, y_pred, average="weighted"), 4),
            }
            for k, v in self.metrics.items():
                logger.info(f"  {k}: {v}")
            return self.metrics
        except Exception as e:
            raise CustomException("Failed to evaluate model", e)

    def log_to_mlflow(self):
        """Log params, metrics and model artifact to the configured MLflow backend."""
        try:
            mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", ""))
            mlflow.set_experiment("MLOps-Jenkins-SharedLib")
            with mlflow.start_run(run_name="LogisticRegression-Run"):
                mlflow.log_param("model_type",   "LogisticRegression")
                mlflow.log_param("max_iter",     1000)
                mlflow.log_param("random_state", 42)
                mlflow.log_param("test_size",    0.2)
                mlflow.log_param("stratify",     True)
                for k, v in self.metrics.items():
                    mlflow.log_metric(k, v)
                mlflow.sklearn.log_model(self.clf, "model")
            logger.info("MLflow logging complete.")
        except Exception as e:
            logger.warning(f"MLflow logging failed (non-fatal): {e}")

    def run(self):
        self.load_data()
        self.train_model()
        metrics = self.evaluate_model()
        self.log_to_mlflow()
        return metrics

if __name__ == "__main__":
    ModelTraining("artifacts/processed/", "artifacts/models/").run()