import json
import numpy as np


# Загрузка комбинированных векторов
def load_combined_vectors(file_path='combined_vectors.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            combined_vectors = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Ошибка загрузки JSON файла {file_path}: {str(e)}")
            raise
    return combined_vectors


# Проверка векторов
def inspect_vectors(combined_vectors, num_samples=5):
    sample_keys = list(combined_vectors.keys())[:num_samples]
    for key in sample_keys:
        video_vector = combined_vectors[key].get('video_vector')
        text_vector = combined_vectors[key].get('text_vector')

        video_vector = np.array(video_vector[0]) if video_vector and video_vector[0] is not None else None
        text_vector = np.array(text_vector[0]) if text_vector and text_vector[0] is not None else None

        print(f"Ключ: {key}")
        print(f"Видео вектор: {video_vector}")
        print(f"Текстовый вектор: {text_vector}")
        print()


if __name__ == "__main__":
    combined_vectors = load_combined_vectors()
    inspect_vectors(combined_vectors)
