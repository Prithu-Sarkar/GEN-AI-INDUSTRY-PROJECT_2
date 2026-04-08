import asyncio
import os
import sys

sys.path.insert(0, "src")

from team.analyzer_gpt import getDataAnalyzerTeam
from agents.Code_Executor_agent import getLocalCodeExecutor
from config.constants import WORK_DIR
from utils.logger import get_logger

from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

logger = get_logger(__name__)

# ── LLM Selection ──────────────────────────────────────────────────────────
# Set USE_GROQ = True  → Groq llama-3.3-70b-versatile (free, fast)
# Set USE_GROQ = False → OpenAI gpt-4o
USE_GROQ = True

if USE_GROQ:
    from config.groq_model_client import get_groq_model_client
    model_client = get_groq_model_client()
    print("Using LLM: Groq llama-3.3-70b-versatile")
else:
    from config.openai_model_client import get_openai_model_client
    model_client = get_openai_model_client()
    print("Using LLM: OpenAI gpt-4o")


async def main():
    os.makedirs(WORK_DIR, exist_ok=True)
    code_executor = getLocalCodeExecutor()
    team = getDataAnalyzerTeam(code_executor, model_client)

    task = (
        "Can you give me a graph of survived vs died from data.csv "
        "and save it as output.png?"
    )
    logger.info("Pipeline started | task: %s", task)

    async for message in team.run_stream(task=task):
        print("=" * 50)
        if isinstance(message, TextMessage):
            print(f"{message.source}: {message.content}")
        elif isinstance(message, TaskResult):
            print(f"Stop Reason: {message.stop_reason}")

    logger.info("Pipeline complete")


if __name__ == "__main__":
    asyncio.run(main())