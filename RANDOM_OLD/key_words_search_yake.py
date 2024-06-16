import yake

def extract_keywords_yake(text):
    kw_extractor = yake.KeywordExtractor(lan="ru", n=1, dedupLim=0.9, top=10)
    keywords = kw_extractor.extract_keywords(text)
    return [keyword for keyword, score in keywords]

russian_text = "что он о тебе думает прямо сейчас слушай, думает, что ты знаешь, для него не посильная ноша как будто бы, да королева мечей чувствует то, что ты по характеру гораздо сильнее и то, что ему с тобой будет очень сложно но при этом есть желание и желание не совсем приличное проявляется боится и, честно говоря, сам проявляться не будет я бы на твоем месте вообще подумала нужен ли тебе такой партнер который слабее тебя но вывода делай сама."
keywords = extract_keywords_yake(russian_text)
print(keywords)  # Вывод ключевых слов