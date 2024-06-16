import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Загрузка стоп-слов
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Пример субтитров
subtitles = "_ | Of | | | i): -— ее ий > pov: you found the perfect skirt for this outfit 9 NY \\ —4 | у и hi _ ы [ i a к\" у Ve о И « ) \\ \\ | | | | } | wa | ром: you found the perfect skitt for this outfit U | | \\ >), \\ ~~ 4 у 4 № > = Se \\ piece Е г (2) = и / Py ey ‘eae > | МАМ. 7 и |"

# Функция для очистки текста
def clean_text(text):
    # Удаление специальных символов и чисел
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Приведение к нижнему регистру
    text = text.lower()
    # Токенизация
    words = word_tokenize(text)
    # Удаление стоп-слов и коротких слов (например, из одного символа)
    words = [word for word in words if word not in stop_words and len(word) > 1]
    return words

# Применение функции очистки к субтитрам
cleaned_words = clean_text(subtitles)

print("Ключевые слова:", cleaned_words)
