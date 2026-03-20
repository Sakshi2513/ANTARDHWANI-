import re

def clean_text(text):
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Keep English + Hindi
    text = re.sub(r"[^a-zA-Z\u0900-\u097F\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def detect_language(text):
    if re.search(r'[\u0900-\u097F]', text):
        return "hindi"
    return "english"