from autogen_agentchat.agents import AssistantAgent
from agents.prompts.DataAnalyzerAgentPrompt import DATA_ANALYZER_MSG
from utils.logger import get_logger

logger = get_logger(__name__)

def getDataAnalyzerAgent(model_client):
    data_analyzer_agent = AssistantAgent(
        name="Data_Analyzer_Agent",
        description="An agent which helps with solving Data Analysis tasks and writes Python code.",
        model_client=model_client,
        system_message=DATA_ANALYZER_MSG,
    )
    logger.info("DataAnalyzerAgent initialized")
    return data_analyzer_agent