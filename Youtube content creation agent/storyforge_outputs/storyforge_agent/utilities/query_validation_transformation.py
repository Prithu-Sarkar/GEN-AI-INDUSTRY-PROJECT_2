
import re
from typing import Dict

# Only alphanumerics, whitespace, and safe punctuation are allowed.
ALLOWED_QUERY_PATTERN = re.compile(r"^[a-zA-Z0-9\s?@#\-_.,'()]+$")

# Stop-words stripped during normalisation.
STOP_WORDS = {"the", "is", "and", "or", "for", "a", "an", "to"}

# Simple synonym map to reduce query variants.
SYNONYMS = {
    "buy": "purchase",
    "find": "search",
    "latest": "recent",
}


def validate_query(query: str) -> bool:
    """Raise ValueError for blank or unsafe queries."""
    if not query or len(query.strip()) < 3:
        raise ValueError("Query must be at least 3 characters long.")
    if not ALLOWED_QUERY_PATTERN.match(query):
        raise ValueError("Query contains invalid characters.")
    return True


def transform_query(query: str) -> Dict[str, str]:
    """Normalise, remove stop-words, apply synonyms, return structured dict."""
    normalized = query.strip().lower()
    normalized = re.sub(r"\s+", " ", normalized)
    tokens = normalized.split()
    tokens = [SYNONYMS.get(t, t) for t in tokens if t not in STOP_WORDS]
    cleaned = " ".join(tokens)
    return {
        "original": query,
        "normalized": normalized,
        "cleaned": cleaned,
        "signature": cleaned.replace(" ", "_"),
    }


def handle_query(query: str) -> Dict[str, str]:
    """Public entry-point: validate then transform a query."""
    validate_query(query)
    return transform_query(query)
