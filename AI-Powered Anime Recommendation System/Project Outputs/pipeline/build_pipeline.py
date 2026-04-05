from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)


def build_pipeline(
    original_csv: str = "data/anime_with_synopsis.csv",
    processed_csv: str = "data/anime_updated.csv",
    persist_dir: str = "chroma_db"
):
    """Runs the full data ingestion + vector store build pipeline."""
    try:
        logger.info("Starting data loading and processing...")
        loader = AnimeDataLoader(original_csv, processed_csv)
        processed_path = loader.load_and_process()
        logger.info(f"Processed CSV saved to: {processed_path}")

        logger.info("Building ChromaDB vector store...")
        builder = VectorStoreBuilder(processed_path, persist_dir=persist_dir)
        builder.build_and_save_vectorstore()
        logger.info("Vector store built and persisted.")

    except Exception as e:
        logger.error(f"Build pipeline failed: {e}")
        raise CustomException("Build pipeline error", e)


if __name__ == "__main__":
    build_pipeline()
