import re
from deep_translator import GoogleTranslator
from langdetect import detect

def detect_language(text: str) -> str:
        try:
            return detect(text)
        except:
            return "en"


def clean_response(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()



def translate_if_needed(text: str, target_lang: str = "en") -> str:
        src_lang = detect_language(text)
        if src_lang == target_lang:
            return text
        return GoogleTranslator(source=src_lang, target=target_lang).translate(text)
