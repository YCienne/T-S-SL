from google.cloud import translate_v2 as translate

translator = translate.Client()

def translate_text(text: str, target_lang: str) -> str:
    result = translate.translate(text, target_language=target_lang)
    return result["translatedText"]