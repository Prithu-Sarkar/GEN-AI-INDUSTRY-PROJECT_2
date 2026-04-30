"""
Configuration Management Module.
Reads all secrets from os.environ (populated by Colab Secrets in Phase 0).
Rate-limit strategy: model chosen for max quality at free-tier TPM limits;
max_tokens caps each response to conserve per-minute token budget.
"""
import os
from typing import Optional
from functools import lru_cache


class Settings:
    """Central settings object. Read-once, cached via lru_cache."""

    def __init__(self):
        # --- LLM: Groq LLaMA 3.3 70B Versatile ---
        # Best quality model available on Groq free tier.
        # LiteLLM model string format: groq/<model_name>
        self.groq_api_key: str  = os.environ.get("GROQ_API_KEY", "")
        self.groq_model: str    = "groq/llama-3.3-70b-versatile"

        # max_tokens: caps each LLM response to conserve TPM budget.
        # 1024 tokens is enough for a structured agent reasoning step.
        self.max_tokens: int    = 1024

        # temperature: low for deterministic financial analysis
        self.temperature: float = 0.1

        # --- Tools ---
        self.firecrawl_api_key: str = os.environ.get("FIRECRAWL_API_KEY", "")

        # --- Optional Azure cloud ---
        self.azure_postgres_connection_string: Optional[str] = (
            os.environ.get("AZURE_POSTGRES_CONNECTION_STRING") or None
        )
        self.azure_blob_storage_connection_string: Optional[str] = (
            os.environ.get("AZURE_BLOB_STORAGE_CONNECTION_STRING") or None
        )

    def validate(self) -> bool:
        """Returns True if all required keys are present."""
        missing = [k for k in ["GROQ_API_KEY", "FIRECRAWL_API_KEY"]
                   if not os.environ.get(k)]
        if missing:
            print(f"[Config] Missing required keys: {missing}")
            return False
        return True


@lru_cache()
def get_settings() -> Settings:
    """Returns a cached Settings singleton (env read once per runtime)."""
    return Settings()


settings = get_settings()