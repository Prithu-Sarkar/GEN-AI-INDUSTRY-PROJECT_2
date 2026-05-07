from typing import List
from loguru import logger
# LangChain >=1.2 imports
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import settings

class EmbeddingService:
    """
    FREE embedding service using sentence-transformers/all-MiniLM-L6-v2.
    No API key required. 384-dimensional vectors. Fast CPU inference.
    Drop-in replacement for GoogleGenerativeAIEmbeddings.
    """
    def __init__(self):
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            is_separator_regex=False,
        )
        logger.info("✅ EmbeddingService ready")

    def split_text(self, text: str) -> List[str]:
        if not text or not text.strip():
            return []
        return self.text_splitter.split_text(text)

    def embed_text(self, text: str) -> List[float]:
        if not text or not text.strip():
            raise ValueError("Cannot embed empty text")
        return self.embeddings.embed_query(text)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        valid = [t for t in texts if t and t.strip()]
        return self.embeddings.embed_documents(valid) if valid else []
