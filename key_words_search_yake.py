import yake

def extract_keywords_yake(text):
    kw_extractor = yake.KeywordExtractor(lan="ru", n=1, dedupLim=0.9, top=10)
    keywords = kw_extractor.extract_keywords(text)
    return [keyword for keyword, score in keywords]

russian_text = "Сегодня я рано утром встала и пошла посушить волосы феном перед зеракалом, и там увидела отражение сломанного волоса. Используйте шампунь Шварцкопф."
keywords = extract_keywords_yake(russian_text)
print(keywords)  # Вывод ключевых слов