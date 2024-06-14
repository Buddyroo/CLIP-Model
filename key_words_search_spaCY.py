import subprocess
import spacy

# Установка модели ru_core_news_sm через subprocess
subprocess.run(["python", "-m", "spacy", "download", "ru_core_news_sm"])

# Загрузка модели для русского языка
nlp = spacy.load("ru_core_news_sm")

def extract_keywords(text):
    # Обработка текста с использованием spaCy
    doc = nlp(text)
    # Извлечение ключевых слов
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return keywords

russian_text = "Сегодня я рано утром встала и пошла посушить волосы феном перед зеракалом, и там увидела отражение сломанного волоса. Используйте шампунь Шварцкопф."
keywords = extract_keywords(russian_text)
print(russian_text)
print(keywords)  # Вывод ключевых слов
