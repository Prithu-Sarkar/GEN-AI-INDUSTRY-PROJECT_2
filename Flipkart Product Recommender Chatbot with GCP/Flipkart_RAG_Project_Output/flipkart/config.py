import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class Config:
    GROQ_API_KEY    = os.getenv("GROQ_API_KEY", "")
    HF_TOKEN        = os.getenv("HF_TOKEN", "")
    LLM_MODEL       = "llama-3.1-8b-instant"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    CHUNK_SIZE      = 500
    CHUNK_OVERLAP   = 50

    @classmethod
    def get_llm(cls):
        return ChatGroq(
            model=cls.LLM_MODEL,
            api_key=cls.GROQ_API_KEY,
            temperature=0,
        )
