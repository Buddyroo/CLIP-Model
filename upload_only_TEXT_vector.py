import json
import requests
import logging

def process_only_text_data(video_id):
    url = "http://127.0.0.1:8000/encode"
    json_file_path = 'video_description/all_videos.json'

    with open(json_file_path, 'r', encoding='utf-8') as file:
        all_videos = json.load(file)

    text = all_videos.get(video_id, {}).get('description', None)

    files = []  # Пустой список файлов
    data = {'texts': [text] if text else []}

    try:
        response = requests.post(url, files=files, data=data)
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

    return result, vector

 #Вызов функции для обработки данных
#print(process_only_text_data('402f3e0144a2aba9f539439d21af'))
