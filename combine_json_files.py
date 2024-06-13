import json
import os

# Функция для загрузки JSON файла
def load_json(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)

# Имена файлов
vector_text_1_file = 'vectors_text_1.json'
vector_text_2_file = 'vectors_text_2.json'
vector_video_1_file = 'vectors_1.json'
vector_video_2_file = 'vectors_2.json'

# Загрузка всех JSON файлов
vector_text_1 = load_json(vector_text_1_file)
vector_text_2 = load_json(vector_text_2_file)
vector_video_1 = load_json(vector_video_1_file)
vector_video_2 = load_json(vector_video_2_file)

# Создание объединенного словаря
combined_data = {}

# Функция для объединения векторов
def combine_vectors(text_dict, video_dict):
    for key, value in text_dict.items():
        if key in video_dict:
            combined_data[key] = {
                'url': value['url'],
                'text_vector': value['vector'],
                'video_vector': video_dict[key]['vector']
            }

# Объединение данных из всех четырех словарей
combine_vectors(vector_text_1, vector_video_1)
combine_vectors(vector_text_1, vector_video_2)
combine_vectors(vector_text_2, vector_video_1)
combine_vectors(vector_text_2, vector_video_2)

# Сохранение объединенного словаря в новый JSON файл
output_file = 'combined_vectors.json'
with open(output_file, 'w') as f:
    json.dump(combined_data, f, indent=4)

print(f"Combined data has been saved to {output_file}")

# Подсчет количества ключей
key_count = len(combined_data)
print(f"The number of keys in {output_file} is {key_count}") #2000

