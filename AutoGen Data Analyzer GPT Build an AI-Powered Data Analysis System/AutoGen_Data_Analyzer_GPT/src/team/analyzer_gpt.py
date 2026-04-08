from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.Data_analyzer_agent import getDataAnalyzerAgent
from agents.Code_Executor_agent import getCodeExecutorAgent
from config.constants import MAX_TURNS, TERMINATION_KW
from utils.logger import get_logger

logger = get_logger(__name__)

def getDataAnalyzerTeam(code_executor, model_client):
    """Build and return a RoundRobinGroupChat team.

    Turn order: Data_Analyzer_Agent → CodeExecutor → repeat
    Terminates when LLM outputs the TERMINATION_KW or MAX_TURNS reached.
    """
    data_analyzer_agent = getDataAnalyzerAgent(model_client)
    code_executor_agent = getCodeExecutorAgent(code_executor)

    termination = TextMentionTermination(TERMINATION_KW)

    team = RoundRobinGroupChat(
        participants=[data_analyzer_agent, code_executor_agent],
        max_turns=MAX_TURNS,
        termination_condition=termination,
    )
    logger.info("DataAnalyzerTeam built | max_turns=%d", MAX_TURNS)
    return team