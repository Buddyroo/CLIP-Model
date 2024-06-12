import json
import time
import os
import logging
import requests
from upload_only_TEXT_vector import process_only_text_data

# Настройка логирования
logging.basicConfig(filename='processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Изменение названий файлов векторов
vectors_file_paths = [f"vectors_text_{i+1}.json" for i in range(40)]
statistics_file_path = 'statistics_text.json'

def load_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            content = file.read().strip()
            if content:
                return json.loads(content)
            else:
                return {}
        except json.JSONDecodeError as e:
            logging.error(f"Error loading JSON file {file_path}: {str(e)}")
            return {}

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def load_last_state():
    vectors = [load_json(path) for path in vectors_file_paths]
    statistics_text = load_json(statistics_file_path)
    return vectors, statistics_text


def main_handle_text():
    vectors, statistics_text = load_last_state()
    json_file_path = 'video_description/all_videos.json'

    with open(json_file_path, 'r', encoding='utf-8') as file:
        try:
            content = file.read().strip()
            if content:
                all_videos = json.loads(content)
            else:
                logging.error(f"JSON file {json_file_path} is empty.")
                return
        except json.JSONDecodeError as e:
            logging.error(f"Error loading JSON file {json_file_path}: {str(e)}")
            return

    video_ids = list(all_videos.keys())[:40000]

    for i, video_id in enumerate(video_ids):
        vector_index = i // 1000  # Разделение видео по файлам каждые 1000 видео
        if any(video_id in v for v in vectors[vector_index]):
            continue  # Skip already processed videos

        start_time = time.time()  # Засекаем время начала обработки

        success, vector = process_only_text_data(video_id)
        if success is not None:
            vectors[vector_index][video_id] = {
                "url": all_videos[video_id]['url'],
                "vector": vector
            }
            log_message = f"Successfully processed data for {video_id}."
            print(log_message)
            logging.info(log_message)
        else:
            log_message = f"Data for {video_id} was not processed."
            print(log_message)
            logging.warning(log_message)

        processing_time = time.time() - start_time  # Вычисляем время обработки

        # Записываем время обработки в статистику
        statistics_text[video_id] = {
            "text_processing_time": processing_time
        }

        # Сохранение данных после обработки каждого видео
        save_json(vectors[vector_index], vectors_file_paths[vector_index])
        save_json(statistics_text, statistics_file_path)

if __name__ == "__main__":
    try:
        main_handle_text()
    except Exception as e:
        log_message = f"An error occurred: {str(e)}"
        print(log_message)
        logging.error(log_message)


if __name__ == "__main__":
    try:
        main_handle_text()
    except Exception as e:
        log_message = f"An error occurred: {str(e)}"
        print(log_message)
        logging.error(log_message)
