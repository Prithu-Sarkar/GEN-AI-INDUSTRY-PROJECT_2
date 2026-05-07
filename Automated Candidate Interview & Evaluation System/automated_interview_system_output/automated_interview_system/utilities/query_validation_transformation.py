import re
from typing import Dict

ALLOWED_QUERY_PATTERN = re.compile(r"^[a-zA-Z0-9\s?@#\-_.,'\"()]+$")
STOP_WORDS = {"the", "is", "and", "or", "for", "a", "an", "to"}
SYNONYMS = {"buy": "purchase", "find": "search", "latest": "recent"}


def validate_query(query: str) -> bool:
    if not query or len(query.strip()) < 3:
        raise ValueError("Query must be at least 3 characters long.")
    if not ALLOWED_QUERY_PATTERN.match(query):
        raise ValueError("Query contains invalid characters.")
    return True


def transform_query(query: str) -> Dict[str, str]:
    normalized = re.sub(r"\s+", " ", query.strip().lower())
    tokens = [SYNONYMS.get(t, t) for t in normalized.split() if t not in STOP_WORDS]
    cleaned = " ".join(tokens)
    return {
        "original": query,
        "normalized": normalized,
        "cleaned": cleaned,
        "signature": cleaned.replace(" ", "_"),
    }


def handle_query(query: str) -> Dict[str, str]:
    validate_query(query)
    return transform_query(query)