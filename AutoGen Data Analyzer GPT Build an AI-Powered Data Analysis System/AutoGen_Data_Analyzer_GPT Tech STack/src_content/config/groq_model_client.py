import os
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constants import GROQ_MODEL, TEMPERATURE

def get_groq_model_client():
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY not set in environment variables.")

    client = OpenAIChatCompletionClient(
        model=GROQ_MODEL,
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        model_capabilities={
            "vision": False,
            "function_calling": True,
            "json_output": True,
        },
    )
    return client