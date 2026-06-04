
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """All app config. Override via env vars or .env file."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "AI Support Copilot"
    # Groq -- two models; instant for agent loop, versatile for fallback
    groq_api_key:         str   = ""
    groq_model_instant:   str   = "llama-3.1-8b-instant"
    groq_model_versatile: str   = "llama-3.3-70b-versatile"
    llm_temperature:      float = 0.2
    max_tokens_per_call:  int   = 1024   # keep within Groq free-tier limits
    tavily_api_key: str = ""
    embedding_model: str = "all-MiniLM-L6-v2"  # local, no API key needed
    # Paths
    base_dir:           Path = Path("/content/customer_support_agent")
    data_dir:           Path = Path("/content/customer_support_agent/data")
    db_path:            Path = Path("/content/customer_support_agent/data/support.db")
    faiss_rag_dir:      Path = Path("/content/customer_support_agent/data/faiss_rag")
    faiss_mem_dir:      Path = Path("/content/customer_support_agent/data/faiss_mem")
    knowledge_base_dir: Path = Path("/content/customer_support_agent/knowledge_base")
    outputs_dir:        Path = Path("/content/customer_support_agent/outputs")
    # RAG / memory tuning
    rag_chunk_size: int = 800; rag_chunk_overlap: int = 120
    rag_top_k: int = 4;       mem_top_k: int = 5

@lru_cache
def get_settings() -> Settings: return Settings()

def ensure_directories(s=None):
    cfg = s or get_settings()
    for p in (cfg.data_dir, cfg.faiss_rag_dir, cfg.faiss_mem_dir,
              cfg.knowledge_base_dir, cfg.outputs_dir):
        Path(p).mkdir(parents=True, exist_ok=True)
