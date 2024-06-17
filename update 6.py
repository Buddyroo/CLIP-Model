import json

# Загружаем данные из файла с указанием кодировки UTF-8
with open('ADD_to_db/DONE_normalized_vectors_6.json', 'r', encoding='utf-8') as vectors_file:
    vectors_data = json.load(vectors_file)

missing_urls = []

# Проверяем, что для каждого video_id есть url
for video_id, data in vectors_data.items():
    if 'url' not in data:
        missing_urls.append(video_id)

if missing_urls:
    print(f"Следующие video_id не имеют url: {missing_urls}")
else:
    print("Все video_id имеют url.")

# Дополнительно можно сохранить результаты в файл
with open('missing_urls.txt', 'w', encoding='utf-8') as missing_file:
    for video_id in missing_urls:
        missing_file.write(f"{video_id}\n")

print("Проверка завершена.")
