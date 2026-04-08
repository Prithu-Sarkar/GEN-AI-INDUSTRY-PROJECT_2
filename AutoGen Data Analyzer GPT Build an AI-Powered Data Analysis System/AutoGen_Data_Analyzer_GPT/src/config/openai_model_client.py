import os
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constants import OPENAI_MODEL, TEMPERATURE

def get_openai_model_client():
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not set in environment variables.")

    client = OpenAIChatCompletionClient(
        model=OPENAI_MODEL,
        api_key=api_key,
    )
    return client