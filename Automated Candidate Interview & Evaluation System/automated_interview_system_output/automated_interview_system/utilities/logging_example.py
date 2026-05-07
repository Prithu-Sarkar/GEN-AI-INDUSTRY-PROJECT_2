import logging
import sys
from pathlib import Path


def get_app_logger(name: str = __name__, log_dir: str = "logs") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    Path(log_dir).mkdir(exist_ok=True)
    fh = logging.FileHandler(f"{log_dir}/utility_logging_example.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))

    logger.addHandler(console)
    logger.addHandler(fh)
    logger.propagate = False
    return logger


def run_logging_demo() -> None:
    logger = get_app_logger("utility_logger")
    logger.debug("Debugging values: %s", {"step": 1, "status": "starting"})
    logger.info("Application example started.")
    logger.warning("This is a warning example for the logging utility.")
    try:
        _ = 10 / 0
    except ZeroDivisionError:
        logger.exception("An exception occurred while dividing by zero.")
    logger.info("Logging demo finished.")