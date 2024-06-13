import json
import requests
import logging

def process_search_request(query_text):
    url = "http://127.0.0.1:8000/encode"

    data = {'texts': [query_text]}
    files = []  # Пустой список файлов

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

# Вызов функции для обработки данных
#print(process_search_request('спорт'))