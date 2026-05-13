
import logging
import sys


def get_app_logger(name: str = __name__) -> logging.Logger:
    """Return a named logger with console (INFO) and file (DEBUG) handlers."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # avoid duplicate handlers on re-import

    logger.setLevel(logging.DEBUG)

    # Console handler — shows INFO and above in stdout.
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # File handler — captures DEBUG and above for traceability.
    fh = logging.FileHandler("storyforge_agent/outputs/storyforge.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))

    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.propagate = False
    return logger


def run_logging_demo() -> None:
    """Exercise every log level to verify handler wiring."""
    logger = get_app_logger("utility_logger")
    logger.debug("Debug payload: %s", {"step": 1, "status": "starting"})
    logger.info("Application example started.")
    logger.warning("Example warning from logging utility.")
    try:
        _ = 10 / 0
    except ZeroDivisionError:
        logger.exception("Caught ZeroDivisionError in logging demo.")
    logger.info("Logging demo finished.")
