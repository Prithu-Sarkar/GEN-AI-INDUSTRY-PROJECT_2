"""Configuration module."""

import os

from dataclasses import (
    dataclass,
    asdict
)

from typing import (
    Dict,
    Any
)


@dataclass
class SystemConfig:

    vector_db_path: str = "vector_db"

    mongo_db_url: str = ""

    groq_api_key: str = ""

    model_name: str = "llama-3.1-8b-instant"

    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    chunk_size: int = 1000

    chunk_overlap: int = 200

    similarity_k: int = 4

    temperature: float = 0.7

    max_tokens: int = 512


    @classmethod
    def from_env(cls):

        return cls(

            vector_db_path=os.getenv(
                "VECTOR_DB_PATH",
                "vector_db"
            ),

            mongo_db_url=os.getenv(
                "MONGO_DB_URL",
                ""
            ),

            groq_api_key=os.getenv(
                "GROQ_API_KEY",
                ""
            )
        )


    def safe_dict(self) -> Dict[str, Any]:

        d = asdict(self)

        for k in (
            "groq_api_key",
            "mongo_db_url"
        ):

            if d[k]:
                d[k] = d[k][:8] + "***"

        return d