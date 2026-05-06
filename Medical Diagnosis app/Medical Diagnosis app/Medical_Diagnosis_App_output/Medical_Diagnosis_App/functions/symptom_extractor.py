import re

# Extended symptom vocabulary for richer extraction
SYMPTOM_PATTERNS = [
    r"headache", r"fever", r"nausea", r"fatigue", r"pain",
    r"cough", r"chills", r"vomiting", r"diarrhea", r"dizziness",
    r"shortness of breath", r"sore throat", r"runny nose",
    r"chest pain", r"back pain", r"muscle ache", r"joint pain",
    r"rash", r"swelling", r"insomnia", r"anxiety", r"depression",
    r"loss of appetite", r"weight loss", r"weight gain",
    r"palpitations", r"blurred vision", r"tinnitus",
    r"numbness", r"tingling", r"weakness"
]

def extract_symptoms(text: str) -> list:
    """
    Parse natural language text and return a deduplicated list of
    recognised medical symptoms.

    Args:
        text: Free-text symptom description from the patient.

    Returns:
        List of unique symptom strings found in the text.
    """
    text_lower = text.lower()
    found = set()
    for pattern in SYMPTOM_PATTERNS:
        if re.search(r"\b" + pattern + r"\b", text_lower):
            found.add(pattern)
    return sorted(found)