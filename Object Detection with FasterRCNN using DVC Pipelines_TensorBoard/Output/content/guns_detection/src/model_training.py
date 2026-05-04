import os
import time

import mlflow
import mlflow.pytorch
import torch
from torch import optim
from torch.utils.data import DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter

from config.data_ingestion_config import (
    NUM_CLASSES, LEARNING_RATE, EPOCHS, BATCH_SIZE,
    RAW_DATA_PATH, MODEL_SAVE_DIR, MODEL_FILENAME, NUM_SAMPLES,
)
from src.custom_exception import CustomException
from src.data_processing import GunDataset
from src.logger import get_logger
from src.model_architecture import FasterRCNNModel

logger = get_logger(__name__)


class ModelTraining:
    '''
    Full training pipeline for Faster R-CNN on the guns dataset.

    Hyper-parameters are read from config/data_ingestion_config.py
    but can be overridden at instantiation for quick experiments.
    '''

    def __init__(
        self,
        num_classes   : int   = NUM_CLASSES,
        learning_rate : float = LEARNING_RATE,
        epochs        : int   = EPOCHS,
        batch_size    : int   = BATCH_SIZE,
        dataset_path  : str   = RAW_DATA_PATH,
        model_save_dir: str   = MODEL_SAVE_DIR,
        num_samples   : int   = NUM_SAMPLES,
    ):
        self.num_classes    = num_classes
        self.learning_rate  = learning_rate
        self.epochs         = epochs
        self.batch_size     = batch_size
        self.dataset_path   = dataset_path
        self.model_save_dir = model_save_dir
        self.num_samples    = num_samples

        # Device selection (Colab T4 GPU recommended)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Training device: {self.device}")

        os.makedirs(self.model_save_dir, exist_ok=True)

        # TensorBoard writer (unique dir per run)
        ts = time.strftime("%Y%m%d-%H%M%S")
        self.log_dir = f"tensorboard_logs/{ts}"
        os.makedirs(self.log_dir, exist_ok=True)
        self.writer  = SummaryWriter(log_dir=self.log_dir)
        logger.info(f"TensorBoard logs -> {self.log_dir}")

        # Build model and optimizer
        try:
            self.model     = FasterRCNNModel(self.num_classes, self.device).model
            self.optimizer = optim.Adam(
                self.model.parameters(), lr=self.learning_rate
            )
            logger.info("Model and optimizer initialised.")
        except Exception as e:
            raise CustomException("Failed to initialise model training", e)

    @staticmethod
    def collate_fn(batch):
        '''Custom collate needed because each sample has variable-size boxes.'''
        return tuple(zip(*batch))

    def _build_loaders(self):
        '''Create train/val DataLoaders with 80/20 split.'''
        try:
            full_dataset = GunDataset(self.dataset_path, self.device)

            # Cap to NUM_SAMPLES so training stays feasible on free Colab
            if self.num_samples and self.num_samples < len(full_dataset):
                full_dataset = torch.utils.data.Subset(
                    full_dataset, range(self.num_samples)
                )
                logger.info(f"Dataset capped to {self.num_samples} samples.")

            train_size = int(0.8 * len(full_dataset))
            val_size   = len(full_dataset) - train_size
            train_ds, val_ds = random_split(full_dataset, [train_size, val_size])

            loader_kw = dict(
                batch_size=self.batch_size,
                num_workers=0,          # 0 avoids CUDA fork issues in Colab
                collate_fn=self.collate_fn,
            )
            train_loader = DataLoader(train_ds, shuffle=True,  **loader_kw)
            val_loader   = DataLoader(val_ds,   shuffle=False, **loader_kw)

            logger.info(f"Loaders ready | train={len(train_ds)} | val={len(val_ds)}")
            return train_loader, val_loader

        except Exception as e:
            raise CustomException("Failed to build DataLoaders", e)

    def _sum_losses(self, loss_dict) -> torch.Tensor:
        '''Sum all loss tensors returned by Faster R-CNN.'''
        if isinstance(loss_dict, dict):
            return sum(v for v in loss_dict.values() if isinstance(v, torch.Tensor))
        return loss_dict[0]

    def run(self):
        '''
        Execute end-to-end training.
        Saves a checkpoint after every epoch and writes the final model
        to artifacts/models/fasterrcnn.pth (DVC-tracked output).
        '''
        try:
            train_loader, val_loader = self._build_loaders()

            with mlflow.start_run():
                # Log all hyper-params to MLflow / DagsHub
                mlflow.log_params({
                    "num_classes"   : self.num_classes,
                    "learning_rate" : self.learning_rate,
                    "epochs"        : self.epochs,
                    "batch_size"    : self.batch_size,
                    "num_samples"   : self.num_samples,
                    "device"        : self.device,
                    "model"         : "FasterRCNN_ResNet50_FPN",
                })

                global_step = 0

                for epoch in range(1, self.epochs + 1):
                    # ---- Training phase ----
                    self.model.train()
                    epoch_loss = 0.0

                    for batch_idx, (images, targets) in enumerate(train_loader):
                        self.optimizer.zero_grad()

                        loss_dict  = self.model(list(images), list(targets))
                        total_loss = self._sum_losses(loss_dict)

                        total_loss.backward()
                        self.optimizer.step()

                        batch_loss  = total_loss.item()
                        epoch_loss += batch_loss

                        # Per-batch TensorBoard log
                        self.writer.add_scalar(
                            "Loss/train_batch", batch_loss, global_step
                        )
                        global_step += 1

                        if batch_idx % 10 == 0:
                            logger.info(
                                f"Epoch {epoch}/{self.epochs} | "
                                f"Batch {batch_idx}/{len(train_loader)} | "
                                f"Loss: {batch_loss:.4f}"
                            )

                    avg_train = epoch_loss / len(train_loader)
                    self.writer.add_scalar("Loss/train_epoch", avg_train, epoch)
                    mlflow.log_metric("train_loss", avg_train, step=epoch)
                    logger.info(
                        f"Epoch {epoch} done | avg_train_loss={avg_train:.4f}"
                    )

                    # ---- Validation phase ----
                    # Keep model.train() + no_grad() to get a loss dict
                    self.model.train()
                    val_loss_total = 0.0
                    with torch.no_grad():
                        for images, targets in val_loader:
                            val_ld          = self.model(list(images), list(targets))
                            val_loss_total += self._sum_losses(val_ld).item()

                    avg_val = val_loss_total / len(val_loader)
                    self.writer.add_scalar("Loss/val_epoch", avg_val, epoch)
                    mlflow.log_metric("val_loss", avg_val, step=epoch)
                    logger.info(f"   val_loss={avg_val:.4f}")

                    # ---- Epoch checkpoint ----
                    ckpt = os.path.join(
                        self.model_save_dir, f"fasterrcnn_epoch{epoch}.pth"
                    )
                    torch.save(self.model.state_dict(), ckpt)
                    logger.info(f"   Checkpoint -> {ckpt}")

                # ---- Final model (DVC output) ----
                final_path = os.path.join(self.model_save_dir, MODEL_FILENAME)
                torch.save(self.model.state_dict(), final_path)
                logger.info(f"Final model saved -> {final_path}")

                # Log model and checkpoint to MLflow artifacts
                mlflow.pytorch.log_model(
                    self.model, artifact_path="faster_rcnn_model"
                )
                mlflow.log_artifact(final_path, artifact_path="checkpoints")

                self.writer.flush()
                self.writer.close()

            logger.info("Training complete.")
            return final_path

        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise CustomException("Model training pipeline failed", e)


if __name__ == "__main__":
    ModelTraining().run()