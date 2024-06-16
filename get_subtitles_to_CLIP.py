import json
import requests
import logging
import time

def process_only_text_data(video_id):
    url = "http://127.0.0.1:8000/encode"
    json_file_path = 'subtitles_new.json'

    with open(json_file_path, 'r', encoding='utf-8') as file:
        all_videos = json.load(file)

    keywords = all_videos.get(video_id, {}).get('keywords', [])
    text = ','.join(keywords)

    files = []  # Пустой список файлов
    data = {'texts': [text] if text else []}

    try:
        start_time = time.time()
        response = requests.post(url, files=files, data=data)
        end_time = time.time()

        processing_time = end_time - start_time

        if response.status_code == 200:
            vector = response.json().get('features', None)
            result = True
        else:
            log_message = f"Failed to get a proper response. Status code: {response.status_code}\nResponse: {response.text}"
            print(log_message)
            logging.error(log_message)
            vector = None
            result = False
    except Exception as e:
        log_message = f"Error during data processing: {str(e)}"
        print(log_message)
        logging.error(log_message)
        vector = None
        result = False

    return result, vector, processing_time

# Вызов функции для обработки данных для всех видео
json_file_path = 'subtitles_new.json'

with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

total_videos = 0
total_processing_time = 0.0
audio_vectors = {}

for video_id, video_data in data.items():
    keywords = video_data.get("keywords")
    if keywords:
        result, vector, processing_time = process_only_text_data(video_id)
        if result and vector is not None:
            audio_vectors[video_id] = vector
            total_videos += 1
            total_processing_time += processing_time
        print(f"Processed video_id {video_id}: {result}")

# Запись векторов в audio_vectors.json
with open('subtitles_vectors.json', 'w', encoding='utf-8') as file:
    json.dump(audio_vectors, file, ensure_ascii=False, indent=4)

# Вывод статистики
print(f"Total videos processed: {total_videos}")
print(f"Total processing time: {total_processing_time:.2f} seconds")
print(f"Average processing time per video: {total_processing_time/total_videos:.2f} seconds" if total_videos > 0 else "No videos processed")
