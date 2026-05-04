
import os
import logging
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Each run gets a unique log file (never overwrites previous runs)
LOG_FILE = os.path.join(
    LOGS_DIR,
    f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
)

logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)

# Stream to stdout so Colab output shows log lines in real-time
_console = logging.StreamHandler()
_console.setLevel(logging.INFO)
_console.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
)
logging.getLogger("").addHandler(_console)


def get_logger(name: str) -> logging.Logger:
    '''Return a named logger; all loggers inherit the root configuration.'''
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
