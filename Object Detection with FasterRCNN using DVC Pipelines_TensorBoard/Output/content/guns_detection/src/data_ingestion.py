import os
import shutil
import zipfile

import kagglehub

from src.logger import get_logger
from src.custom_exception import CustomException
from config.data_ingestion_config import DATASET_NAME, TARGET_DIR

logger = get_logger(__name__)


class DataIngestion:
    '''
    Handles end-to-end data acquisition:
      1. Download dataset from Kaggle using kagglehub
      2. Walk the downloaded folder recursively
      3. Copy images  -> artifacts/raw/Images/
         Copy labels  -> artifacts/raw/Labels/
    '''

    def __init__(self, dataset_name: str = DATASET_NAME, target_dir: str = TARGET_DIR):
        self.dataset_name = dataset_name
        self.target_dir   = target_dir
        logger.info(f"DataIngestion init | dataset={dataset_name} | target={target_dir}")

    def _create_raw_dir(self) -> str:
        '''Create artifacts/raw/ and return its path.'''
        raw_dir = os.path.join(self.target_dir, "raw")
        os.makedirs(raw_dir, exist_ok=True)
        return raw_dir

    def _flatten_dataset(self, dataset_path: str, raw_dir: str) -> None:
        '''
        Recursively walk dataset_path, then copy:
          - image files (.jpg / .jpeg / .png) -> raw_dir/Images/
          - label files (.txt)                -> raw_dir/Labels/
        Target sub-dirs are wiped first (idempotent).
        '''
        images_dst = os.path.join(raw_dir, "Images")
        labels_dst = os.path.join(raw_dir, "Labels")

        for dst in (images_dst, labels_dst):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            os.makedirs(dst)

        IMAGE_EXTS = (".jpg", ".jpeg", ".png")
        img_count = lbl_count = 0

        for root, _, files in os.walk(dataset_path):
            for fname in files:
                src = os.path.join(root, fname)
                if fname.lower().endswith(IMAGE_EXTS):
                    shutil.copy(src, os.path.join(images_dst, fname))
                    img_count += 1
                elif fname.lower().endswith(".txt"):
                    shutil.copy(src, os.path.join(labels_dst, fname))
                    lbl_count += 1

        logger.info(f"Flattened: {img_count} images, {lbl_count} labels")
        if img_count == 0 or lbl_count == 0:
            raise FileNotFoundError(
                "No images or labels found. "
                "Check Kaggle credentials and dataset slug."
            )

    def _handle_zip(self, dataset_path: str) -> str:
        '''If kagglehub returned a .zip path, extract it first.'''
        if dataset_path.endswith(".zip"):
            extract_dir = dataset_path.replace(".zip", "")
            if not os.path.exists(extract_dir):
                logger.info(f"Extracting zip -> {extract_dir}")
                with zipfile.ZipFile(dataset_path, "r") as zf:
                    zf.extractall(extract_dir)
            return extract_dir
        return dataset_path

    def run(self) -> str:
        '''
        Execute full ingestion pipeline.
        Returns the path to the populated raw directory.
        '''
        try:
            raw_dir = self._create_raw_dir()
            logger.info("Downloading dataset from Kaggle ...")
            dataset_path = kagglehub.dataset_download(self.dataset_name)
            logger.info(f"Kaggle cache path: {dataset_path}")
            dataset_path = self._handle_zip(dataset_path)
            self._flatten_dataset(dataset_path, raw_dir)
            logger.info(f"Data ingestion complete. Raw data at: {raw_dir}")
            return raw_dir
        except Exception as e:
            logger.error(f"Data ingestion failed: {e}")
            raise CustomException("Data ingestion pipeline failed", e)


if __name__ == "__main__":
    DataIngestion().run()
