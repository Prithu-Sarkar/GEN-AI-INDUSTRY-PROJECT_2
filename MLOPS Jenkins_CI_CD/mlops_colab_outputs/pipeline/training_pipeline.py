from src.data_processing import DataProcessing
from src.model_training import ModelTraining

if __name__ == "__main__":
    # Step 1 – Process raw data
    processor = DataProcessing("artifacts/raw/data.csv", "artifacts/processed")
    processor.run()

    # Step 2 – Train and evaluate model
    trainer = ModelTraining("artifacts/processed/", "artifacts/models/")
    trainer.run()