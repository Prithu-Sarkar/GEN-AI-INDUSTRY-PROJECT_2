"""
Configuration Management Module.

Uses environment variables (loaded from Colab Secrets or os.environ) to
provide validated settings to the rest of the application.

Usage:
    from src.shared.config import settings
    print(settings.groq_api_key)
"""

import os
from typing import Optional
from functools import lru_cache


class Settings:
    """
    Central settings object.
    Reads directly from os.environ (populated by Colab Secrets in Phase 0).

    Attributes:
        groq_api_key (str): Key for Groq LLM inference.
        groq_model (str): LLaMA Instant model identifier.
        firecrawl_api_key (str): Key for Firecrawl news scraping.
        azure_postgres_connection_string (Optional[str]): Optional DB URL.
        azure_blob_storage_connection_string (Optional[str]): Optional Blob URL.
    """

    def __init__(self):
        # --- LLM Configuration (Groq / LLaMA Instant) ---
        self.groq_api_key: str = os.environ.get('GROQ_API_KEY', '')
        # LiteLLM model string format: "groq/<model_name>"
        self.groq_model: str = 'groq/llama-3.3-70b-versatile'

        # --- Tool Configuration (Firecrawl) ---
        self.firecrawl_api_key: str = os.environ.get('FIRECRAWL_API_KEY', '')

        # --- Optional Azure Cloud Configuration ---
        self.azure_postgres_connection_string: Optional[str] = (
            os.environ.get('AZURE_POSTGRES_CONNECTION_STRING') or None
        )
        self.azure_blob_storage_connection_string: Optional[str] = (
            os.environ.get('AZURE_BLOB_STORAGE_CONNECTION_STRING') or None
        )

    def validate(self) -> bool:
        """Returns True if all required keys are present."""
        missing = []
        if not self.groq_api_key:
            missing.append('GROQ_API_KEY')
        if not self.firecrawl_api_key:
            missing.append('FIRECRAWL_API_KEY')
        if missing:
            print(f'[Config] Missing required keys: {missing}')
            return False
        return True


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached Settings singleton.
    Using lru_cache ensures environment is read only once per runtime.
    """
    return Settings()


# Module-level singleton for easy import
settings = get_settings()