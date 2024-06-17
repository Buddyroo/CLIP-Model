import json
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import re

# Инициализация модели и токенизатора
model_name = 'Helsinki-NLP/opus-mt-ru-en'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Словарь исключений
exceptions = {
    "нарезкистримов": "stream_cuts",
    "холодное сердце": "frozen",
    "роблокс": "roblox",
    "глэмпинг": "glamping",
    "влог": "vlog",
    "лайфхаки": "lifehacks",
    "бьютирутина": "beauty_routine",
    "контент": "content",
    "пахлава": "baklava",
    "пахлавы": "baklava",
    "пахлаву": "baklava",
    "лукум": "locum",
    "анекдот": "joke",
}

# Фраза для исключения
exclude_phrase = "The present document is being issued without formal editing."


def translate(text, model, tokenizer):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    output_ids = model.generate(input_ids, max_new_tokens=100)
    en_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return en_text


def contains_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))


def translate_text(text):
    # Заменяем фразы из словаря исключений на их переводы
    for phrase, translation in exceptions.items():
        text = re.sub(rf'\b{re.escape(phrase)}\b', translation, text)

    words = text.split(', ')
    translated_words = []
    seen_words = set()

    for word in words:
        clean_word = word.strip()
        if contains_cyrillic(clean_word):
            translated_word = translate(clean_word, model, tokenizer)
            if translated_word != exclude_phrase and translated_word not in seen_words:
                translated_words.append(translated_word)
                seen_words.add(translated_word)
        else:
            if clean_word not in seen_words:
                translated_words.append(clean_word)
                seen_words.add(clean_word)

    # Объединяем уникальные переведенные слова, разделенные запятыми
    translated_text = ', '.join(translated_words)
    return translated_text


# Функция для перевода всех транскрипций из файла
def translate_transcriptions(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        transcriptions = json.load(f)

    translated_transcriptions = {}
    total_transcriptions = len(transcriptions)
    for i, (key, value) in enumerate(transcriptions.items(), 1):
        transcription = value.get('transcription', '')
        if transcription:
            translated_transcription = translate_text(transcription)
            value['transcription'] = translated_transcription
        translated_transcriptions[key] = value
        # Вывод прогресса
        print(f'Перевод {i} из {total_transcriptions} завершен.')

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translated_transcriptions, f, ensure_ascii=False, indent=4)


# Пример использования функции
translate_transcriptions('transcriptions_all.json', 'transcriptions_all_Translated.json')
