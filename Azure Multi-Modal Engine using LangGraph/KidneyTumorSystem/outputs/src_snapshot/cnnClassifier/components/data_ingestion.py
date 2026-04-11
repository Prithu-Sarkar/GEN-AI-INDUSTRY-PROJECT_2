import os, zipfile
import gdown
from pathlib import Path
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import DataIngestionConfig


class DataIngestion:
    """Downloads the kidney CT-scan dataset from Google Drive and extracts it."""

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self) -> None:
        """Fetch data from Google Drive using gdown."""
        try:
            dataset_url    = self.config.source_URL
            zip_path       = self.config.local_data_file
            os.makedirs("artifacts/data_ingestion", exist_ok=True)
            logger.info(f"Downloading data from {dataset_url}")
            file_id = dataset_url.split("/")[-2]
            prefix  = "https://drive.google.com/uc?/export=download&id="
            gdown.download(prefix + file_id, str(zip_path), quiet=False)
            logger.info(f"Download complete. Size: {get_size(zip_path)}")
        except Exception as e:
            raise e

    def extract_zip_file(self) -> None:
        """Extract the downloaded ZIP archive."""
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, "r") as zf:
            zf.extractall(unzip_path)
        logger.info(f"Data extracted to: {unzip_path}")
