from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from config.constants import WORK_DIR, TIMEOUT_EXEC
from utils.logger import get_logger
import os

logger = get_logger(__name__)

def getLocalCodeExecutor():
    os.makedirs(WORK_DIR, exist_ok=True)
    executor = LocalCommandLineCodeExecutor(
        work_dir=WORK_DIR,
        timeout=TIMEOUT_EXEC,
    )
    logger.info(f"LocalCommandLineCodeExecutor ready | work_dir={WORK_DIR}")
    return executor

def getCodeExecutorAgent(code_executor):
    agent = CodeExecutorAgent(
        name="CodeExecutor",
        code_executor=code_executor,
    )
    logger.info("CodeExecutorAgent initialized")
    return agent