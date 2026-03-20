# app/services/language_service.py

from deep_translator import GoogleTranslator

# Initialize translators once for efficiency
english_translator = GoogleTranslator(source='auto', target='en')
hindi_translator = GoogleTranslator(source='auto', target='hi')


def translate_to_english(text: str) -> str:
    """
    Translate input text to English.
    """
    try:
        return english_translator.translate(text)
    except Exception as e:
        print(f"[Translation Error] Could not translate to English: {e}")
        return text  # fallback to original text


def translate_to_hindi(text: str) -> str:
    """
    Translate input text to Hindi.
    """
    try:
        return hindi_translator.translate(text)
    except Exception as e:
        print(f"[Translation Error] Could not translate to Hindi: {e}")
        return text  # fallback to original text