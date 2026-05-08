# utils.py
# General-purpose helpers shared across the holiday_management package.

import time
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def format_markdown_itinerary(raw_text: str, destination: str, days: int) -> str:
    """
    Wrap raw agent output in a consistent Markdown header.

    Parameters
    ----------
    raw_text    : The text produced by the final writing agent.
    destination : Name of the destination city/region.
    days        : Number of trip days.

    Returns
    -------
    str : Formatted Markdown string ready for display or export.
    """
    header = f"# 🌍 {days}-Day Travel Guide: {destination}\n\n"
    return header + raw_text


def timer(func):
    """
    Decorator that logs the wall-clock time of any function call.
    Useful for measuring LLM API latency.
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info("[TIMER] %s completed in %.2fs", func.__name__, elapsed)
        return result
    return wrapper


def safe_dict_get(d: Dict[str, Any], *keys, default=None) -> Any:
    """
    Safely traverse a nested dict with a list of keys.
    Returns `default` if any key is missing (avoids KeyError chains).
    """
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, default)
    return d