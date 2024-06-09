import pandas as pd
import json
import os

# Создаем папку для JSON, если она не существует
if not os.path.exists('video_description'):
    os.makedirs('video_description')

# Загрузка данных из CSV
data = pd.read_csv('db_links/yappy_hackaton_2024_400k.csv', header=None, skiprows=2, encoding='utf-8')

# Замена NaN значений на None в описаниях
data[1] = data[1].apply(lambda x: None if pd.isna(x) else x)

# Словарь для хранения данных
video_data = {}

# Обработка каждой строки данных
for index, row in data.iterrows():
    url = row[0]  # первый столбец - ссылка
    description = row[1]  # второй столбец - описание, теперь с None вместо NaN

    # Извлечение уникального идентификатора из URL
    unique_id = url.split('/')[-2]

    # Сохранение URL и описания в словарь
    video_data[unique_id] = {
        'url': url,
        'description': description
    }

# Сохранение словаря в JSON файл
with open('video_description/all_videos.json', 'w', encoding='utf-8') as f:
    json.dump(video_data, f, ensure_ascii=False)

print("Сохранение описаний и ссылок для всех видео завершено.")
