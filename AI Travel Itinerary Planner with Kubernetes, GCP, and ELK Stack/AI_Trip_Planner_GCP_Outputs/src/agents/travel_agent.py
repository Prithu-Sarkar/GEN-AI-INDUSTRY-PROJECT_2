import os
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from src.tools.tavily_tool import tavily_search_tool
from src.tools.serper_tool import google_serper_search_tool
from src.utils.logger import get_logger

logger = get_logger(__name__)

# ── LLM selection ──────────────────────────────────────────────────────────
# Primary: Groq (free, fast)  |  Fallback: OpenAI gpt-4o
USE_OPENAI = False  # Set True to switch to OpenAI gpt-4o

if USE_OPENAI:
    model = init_chat_model(
        model="openai:gpt-4o",
        temperature=0.3
    )
    logger.info("Using OpenAI gpt-4o")
else:
    model = init_chat_model(
        model="groq:llama-3.3-70b-versatile",
        temperature=0.3
    )
    logger.info("Using Groq llama-3.3-70b-versatile")

SYSTEM_PROMPT = '''
You are an expert AI travel planner.

Rules:
- Always use web search tools for real-world accuracy
- Create a detailed day-wise itinerary
- Include food suggestions, local tips, and travel advice

User Inputs:
City, Number of days, Interests, Travel style, Pace
'''.strip()

agent = create_react_agent(
    model=model,
    tools=[tavily_search_tool, google_serper_search_tool],
    prompt=SYSTEM_PROMPT
)

logger.info("Travel agent created")