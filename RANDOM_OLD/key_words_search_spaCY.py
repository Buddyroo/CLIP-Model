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

russian_text = "что он о тебе думает прямо сейчас слушай, думает, что ты знаешь, для него не посильная ноша как будто бы, да королева мечей чувствует то, что ты по характеру гораздо сильнее и то, что ему с тобой будет очень сложно но при этом есть желание и желание не совсем приличное проявляется боится и, честно говоря, сам проявляться не будет я бы на твоем месте вообще подумала нужен ли тебе такой партнер который слабее тебя но вывода делай сама"
keywords = extract_keywords(russian_text)
print(russian_text)
print(keywords)  # Вывод ключевых слов
