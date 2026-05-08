# settings.py
# Single source of truth for all environment variables and runtime settings.
# Reads from os.environ (populated by Colab Secrets in Phase 0).

import os


class Settings:
    """
    Centralised application settings.
    Every agent and utility imports from here — no scattered os.getenv calls.
    """

    # ── LLM ──────────────────────────────────────────────────────────────────
    # Using Groq llama-3.1-8b-instant: fast inference, generous free tier.
    GROQ_API_KEY:   str = os.environ.get("GROQ_API_KEY", "")
    LLM_MODEL:      str = "llama-3.1-8b-instant"   # versatile & within token limits
    LLM_MAX_TOKENS: int = 256                      # safe ceiling for Groq free tier
    LLM_TEMPERATURE: float = 0.3                    # slightly creative but stable

    # ── Databases ────────────────────────────────────────────────────────────
    MONGO_DB_URL:   str = os.environ.get("MONGO_DB_URL", "")
    CHROMA_DB_PATH: str = "all-utils/db"            # local ChromaDB for Mem0

    # ── MLflow ───────────────────────────────────────────────────────────────
    MLFLOW_TRACKING_URI:      str = os.environ.get("MLFLOW_TRACKING_URI", "./mlruns")
    MLFLOW_TRACKING_USERNAME: str = os.environ.get("MLFLOW_TRACKING_USERNAME", "")
    MLFLOW_TRACKING_PASSWORD: str = os.environ.get("MLFLOW_TRACKING_PASSWORD", "")
    MLFLOW_EXPERIMENT_NAME:   str = "Holiday_Management_Agent"

    # ── Agent behaviour ──────────────────────────────────────────────────────
    MAX_AGENT_ROUNDS: int = 6   # maximum back-and-forth turns per planning session


settings = Settings()   # single shared instance — import this, not Settings()