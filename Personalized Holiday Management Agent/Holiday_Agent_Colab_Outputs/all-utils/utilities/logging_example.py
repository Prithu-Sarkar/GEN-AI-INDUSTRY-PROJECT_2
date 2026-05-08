# logging_example.py
# Provides a reusable, dual-output logger for the Holiday Management Agent.
#
# Two handlers are attached to every logger instance:
#   • Console (INFO+) — coloured output in Colab / terminal
#   • File (DEBUG+)   — full trace written to utility_logging_example.log
#
# Usage:
#   from utilities.logging_example import get_app_logger
#   logger = get_app_logger("my_module")
#   logger.info("Agent started.")

import logging
import sys


def get_app_logger(name: str = __name__) -> logging.Logger:
    """
    Return a named logger with console + file handlers.
    Calling this multiple times with the same name is safe — handlers
    are only added once (guard via `logger.handlers`).
    """
    logger = logging.getLogger(name)
    if logger.handlers:        # already configured — return as-is
        return logger

    logger.setLevel(logging.DEBUG)   # capture everything at the root level

    # ── Console handler: INFO and above ──────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))

    # ── File handler: DEBUG and above (full audit trail) ─────────────────────
    file_handler = logging.FileHandler(
        "utility_logging_example.log", encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    ))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.propagate = False  # prevent double-logging via root logger
    return logger


def run_logging_demo() -> None:
    """Demonstrates all log levels including exception capture."""
    logger = get_app_logger("utility_logger")

    logger.debug("Debugging values: %s", {"step": 1, "status": "starting"})
    logger.info("Holiday Agent logging demo started.")
    logger.warning("Token budget is approaching 80%% — consider truncating context.")

    try:
        value = 10 / 0   # simulate a runtime error in an agent step
    except ZeroDivisionError:
        logger.exception("Division error — would be an API/timeout failure in production.")

    logger.info("Logging demo finished.")