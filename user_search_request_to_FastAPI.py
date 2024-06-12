import json
import time
import os
import logging
from upload_only_TEXT_vector import process_only_text_data

# Настройка логирования
logging.basicConfig(filename='processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Путь к файлу для записи времени обработки запросов пользователя
user_search_file_path = 'user_search.json'


def load_json(file_path):
    if not os.path.exists(file_path):
        # Создаем пустой файл с пустым словарем, если он не существует
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False)  # ensure_ascii=False для поддержки русского языка
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
        json.dump(data, file, indent=4, ensure_ascii=False)  # ensure_ascii=False для поддержки русского языка


def user_search_request():
    # Загрузка существующих данных
    user_search_data = load_json(user_search_file_path)

    # Ввод слова или фразы для поиска
    search_query = input("Введите слово или фразу для поиска: ")

    start_time = time.time()  # Засекаем время начала обработки

    # Обработка введенного текста
    success, vector = process_only_text_data(search_query)

    if success:
        processing_time = time.time() - start_time  # Вычисляем время обработки
        user_search_data[search_query] = processing_time
        log_message = f"Successfully processed data for query '{search_query}'. Processing time: {processing_time:.2f} seconds."
        print(log_message)
        logging.info(log_message)
    else:
        log_message = f"Failed to process data for query '{search_query}'."
        print(log_message)
        logging.warning(log_message)

    # Сохранение данных после обработки
    save_json(user_search_data, user_search_file_path)


if __name__ == "__main__":
    try:
        user_search_request()
    except Exception as e:
        log_message = f"An error occurred: {str(e)}"
        print(log_message)
        logging.error(log_message)
