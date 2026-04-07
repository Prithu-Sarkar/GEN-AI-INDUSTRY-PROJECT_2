import os
from src.utils.logger import get_logger

logger = get_logger(__name__)

GROQ_API_KEY   = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

logger.info("Config initialized")