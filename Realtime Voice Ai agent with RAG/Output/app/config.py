from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    MONGO_URL: str
    DB_NAME: str = "live_db"
    GROQ_API_KEY: str
    DEEPGRAM_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    ELEVENLABS_VOICE_ID: str = "pNInz6obpgDQGcFmaJgB"
    # llama-3.1-8b-instant: fast, 131k ctx, free tier friendly
    # llama-3.3-70b-versatile: higher quality, fits token limits, also free
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    # Free local HuggingFace embeddings - no API key needed
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSIONS: int = 384
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150
    VECTOR_INDEX_NAME: str = "vector_index"
    DOCUMENT_CHUNKS_COLLECTION: str = "document_chunks"
    TENANT_ID: str = "mvp_tenant"
    USER_ID: str = "mvp_user"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
