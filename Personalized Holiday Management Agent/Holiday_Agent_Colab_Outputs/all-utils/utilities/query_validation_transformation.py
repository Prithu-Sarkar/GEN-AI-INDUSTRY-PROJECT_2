# query_validation_transformation.py
# Cleans and normalizes raw user queries before they reach the LLM.
#
# Pipeline:
#   1. validate_query()   — reject short / malformed queries immediately
#   2. transform_query()  — lowercase, collapsed whitespace, strip stop-words,
#                           expand synonyms, and produce a cache-friendly
#                           signature string.

import re
from typing import Dict


# Only alphanumeric + a safe set of punctuation is permitted.
# This blocks SQL injection, HTML tags, and unusual Unicode.
ALLOWED_QUERY_PATTERN = re.compile(r"""^[a-zA-Z0-9\s?@#\-_.,'"()]+$""")

# Common English stop-words that add noise to keyword searches.
STOP_WORDS = {"the", "is", "and", "or", "for", "a", "an", "to", "i", "want"}

# Synonym map: map user vocabulary → canonical vocabulary.
# Extend this dict to cover your domain (e.g. travel-specific terms).
SYNONYMS = {
    "buy":    "purchase",
    "find":   "search",
    "latest": "recent",
    "trip":   "travel",
    "holiday": "vacation",
    "book":   "reserve",
    "cheap":  "budget",
}


def validate_query(query: str) -> bool:
    """Raises ValueError if the query is too short or contains illegal chars."""
    if not query or len(query.strip()) < 3:
        raise ValueError("Query must be at least 3 characters long.")
    if not ALLOWED_QUERY_PATTERN.match(query):
        raise ValueError("Query contains invalid characters.")
    return True


def transform_query(query: str) -> Dict[str, str]:
    """
    Returns a dict with four representations of the query:
      original  — raw input from the user
      normalized — lowercase, collapsed whitespace
      cleaned   — stop-words removed, synonyms applied
      signature — cleaned query joined with underscores (cache key)
    """
    # Step 1: lowercase and collapse extra whitespace
    normalized = query.strip().lower()
    normalized = re.sub(r"\s+", " ", normalized)

    # Step 2: tokenise, remove stop-words, apply synonym map
    tokens = normalized.split()
    tokens = [SYNONYMS.get(token, token) for token in tokens
              if token not in STOP_WORDS]
    cleaned_query = " ".join(tokens)

    # Step 3: produce a deterministic cache/signature key
    query_signature = cleaned_query.replace(" ", "_")

    return {
        "original":   query,
        "normalized": normalized,
        "cleaned":    cleaned_query,
        "signature":  query_signature,
    }


def handle_query(query: str) -> Dict[str, str]:
    """Full pipeline: validate then transform."""
    validate_query(query)
    return transform_query(query)