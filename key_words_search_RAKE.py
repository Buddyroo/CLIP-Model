import nltk
from rake_nltk import Rake

# Загрузка необходимых ресурсов NLTK
nltk.download('stopwords')
nltk.download('punkt')

# Инициализация RAKE с русскими стоп-словами
r = Rake(stopwords=nltk.corpus.stopwords.words('russian'))

# Текст на русском языке
russian_text = "Сегодня я рано утром встала и пошла посушить волосы феном перед зеракалом, и там увидела отражение сломанного волоса. Используйте шампунь Шварцкопф."

# Извлечение ключевых слов
r.extract_keywords_from_text(russian_text)

# Получение ключевых фраз, отсортированных по важности
keywords = r.get_ranked_phrases()

# Вывод ключевых слов
print(keywords)
