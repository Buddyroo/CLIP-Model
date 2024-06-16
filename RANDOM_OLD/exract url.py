import json

# Загрузка данных из файла vectors_separated_frames_998-4000.json
with open('../vectors_separated_frames_998-4000.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Извлечение всех URL
urls = {key: value['url'] for key, value in data.items()}

# Сохранение URL в новый файл urls.json
with open('../urls.json', 'w', encoding='utf-8') as file:
    json.dump(urls, file, ensure_ascii=False, indent=4)

print("Все URL успешно сохранены в файл urls.json")
