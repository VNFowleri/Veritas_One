import re

def basic_deidentify(text: str) -> str:
    """
    Removes PHI (Protected Health Information) from text using regex.
    """
    text = re.sub(r"\(\d{3}\)\s*\d{3}-\d{4}", "[PHONE]", text)
    text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", "[EMAIL]", text)
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]", text)
    text = re.sub(r"\b(?:19|20)\d{2}-\d{2}-\d{2}\b", "[DATE]", text)  # YYYY-MM-DD
    return text