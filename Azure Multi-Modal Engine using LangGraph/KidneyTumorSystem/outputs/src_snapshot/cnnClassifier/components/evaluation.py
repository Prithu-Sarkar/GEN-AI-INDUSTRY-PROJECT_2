import os
import tensorflow as tf
import mlflow
import mlflow.keras
from urllib.parse import urlparse
from pathlib import Path
from cnnClassifier.entity.config_entity import EvaluationConfig
from cnnClassifier.utils.common import save_json


class Evaluation:
    """Evaluates the trained model and logs metrics/artifacts to MLflow."""

    def __init__(self, config: EvaluationConfig):
        self.config = config

    def _valid_generator(self) -> None:
        """Build a validation ImageDataGenerator (30% split)."""
        datagenerator_kwargs = dict(rescale=1.0 / 255, validation_split=0.30)
        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear",
        )
        valid_dg = tf.keras.preprocessing.image.ImageDataGenerator(**datagenerator_kwargs)
        self.valid_generator = valid_dg.flow_from_directory(
            directory=str(self.config.training_data),
            subset="validation", shuffle=False, **dataflow_kwargs,
        )

    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(str(path))

    def evaluation(self) -> None:
        """Run model.evaluate() on the validation set."""
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = self.model.evaluate(self.valid_generator)

    def save_score(self) -> None:
        """Persist loss & accuracy to scores.json."""
        scores = {"loss": float(self.score[0]), "accuracy": float(self.score[1])}
        save_json(path=Path("scores.json"), data=scores)

    def log_into_mlflow(self) -> None:
        """
        Log params, metrics, and Keras model artifact to MLflow.
        Supports both remote (DagsHub) and local file-store tracking URIs.
        """
        mlflow_uri = self.config.mlflow_uri or os.environ.get("MLFLOW_TRACKING_URI", "")
        mlflow.set_tracking_uri(mlflow_uri)
        tracking_scheme = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            mlflow.log_params(dict(self.config.all_params))
            mlflow.log_metrics({
                "loss":     float(self.score[0]),
                "accuracy": float(self.score[1]),
            })
            if tracking_scheme != "file":
                # Remote registry (DagsHub / MLflow server)
                mlflow.keras.log_model(
                    self.model, "model",
                    registered_model_name="VGG16_KidneyTumor",
                )
            else:
                # Local file store - model registry not supported
                mlflow.keras.log_model(self.model, "model")
