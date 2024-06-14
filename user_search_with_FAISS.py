import json
import time
import os
import logging
import numpy as np
from upload_search_request_to_CLIP import process_search_request
from faiss_module import FaissIndex  # Ваш класс FaissIndex

# Настройка логирования
logging.basicConfig(filename='processing.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Путь к файлам для записи и загрузки индексов
video_index_file_path = 'video_separated_frames_index.faiss'
vectors_file_path = 'vectors_separated_frames_1.json'
user_search_file_path = 'user_search.json'
faiss_statistics_file_path = 'FAISS_statistics.json'
all_videos_file_path = 'video_description/all_videos.json'

# Функция для загрузки векторов из JSON файла
def load_vectors(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            vectors_data = json.load(f)
            logging.debug(f"Vectors loaded: {vectors_data}")
        except json.JSONDecodeError as e:
            logging.error(f"Error loading JSON file {file_path}: {str(e)}")
            raise
    video_vectors = []
    video_ids = []
    for video_id, data in vectors_data.items():
        for vector in data['vectors']:
            video_vectors.append(np.array(vector, dtype='float32'))
            video_ids.append(video_id)
    logging.debug(f"Video vectors: {video_vectors}")
    return video_vectors, video_ids

try:
    video_vectors, video_ids = load_vectors(vectors_file_path)
    logging.info("Successfully loaded vectors.")
except Exception as e:
    logging.error(f"Failed to load vectors: {str(e)}")
    raise

# Размерность векторов
d = len(video_vectors[0])
logging.info(f"Vector dimension: {d}")

# Создание или загрузка Faiss индексов
video_index = FaissIndex(d, index_type='FlatL2')

if os.path.exists(video_index_file_path):
    # Загрузка индексов из файлов
    video_index.load_index(video_index_file_path)
    logging.info("Loaded existing Faiss indices.")
else:
    # Добавление векторов и сохранение индексов
    video_index.add_vectors(np.vstack(video_vectors))
    video_index.save_index(video_index_file_path)
    logging.info("Created and saved new Faiss indices.")

def load_json(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False)
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
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_all_videos(file_path=all_videos_file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            all_videos = json.load(f)
            logging.debug(f"All videos loaded: {all_videos}")
        except json.JSONDecodeError as e:
            logging.error(f"Error loading JSON file {file_path}: {str(e)}")
            raise
    return all_videos

def user_search_request():
    # Загрузка существующих данных
    user_search_data = load_json(user_search_file_path)
    faiss_statistics = load_json(faiss_statistics_file_path)
    all_videos = load_all_videos()

    # Ввод слова или фразу для поиска
    search_query = input("Введите слово или фразу для поиска: ")
    logging.debug(f"Search query: {search_query}")

    start_time = time.time()  # Засекаем время начала обработки
    try:
        # Обработка введенного текста
        success, vector = process_search_request(search_query)
        logging.debug(f"Processing result: success={success}, vector={vector}")
        if not success:
            raise ValueError("Failed to process text data.")

        clip_processing_time = time.time() - start_time  # Вычисляем время обработки
        logging.info(f"CLIP processing time: {clip_processing_time:.2f} seconds.")

        # Поиск по Faiss индексам
        query_vector = np.array(vector).astype('float32').reshape(1, -1)
        logging.debug(f"Query vector: {query_vector}")

        k = 15  # Количество ближайших соседей для поиска
        start_faiss_time = time.time()
        video_distances, video_indices = video_index.search_vectors(query_vector, k)
        faiss_search_time = time.time() - start_faiss_time

        logging.info(f"FAISS search time: {faiss_search_time:.2f} seconds.")
        logging.debug(f"Video distances: {video_distances}, Video indices: {video_indices}")

        video_results = []

        for i in range(k):
            video_index_id = video_indices[0][i]
            best_video_match_id = video_ids[video_index_id]
            video_url = all_videos.get(best_video_match_id, {}).get('url', '')
            video_results.append({
                "url": video_url,
                "video_distance": float(video_distances[0][i])
            })

        user_search_data[search_query] = clip_processing_time
        faiss_statistics[search_query] = {
            "video_results": video_results,
            "clip_processing_time": clip_processing_time,
            "faiss_search_time": faiss_search_time
        }

        formatted_video_results = "\n".join(
            [f"{i + 1}. Video Distance: {result['video_distance']:.2f}\nURL: {result['url']}" for i, result in
             enumerate(video_results)])

        log_message = (f"Successfully processed data for query '{search_query}'.\n"
                       f"Processing time: {clip_processing_time:.2f} seconds,\n"
                       f"FAISS search time: {faiss_search_time:.2f} seconds.\n"
                       f"Top 15 results by video distance:\n{formatted_video_results}")
        print(log_message)
        logging.info(log_message)
    except Exception as e:
        log_message = f"An error occurred: {str(e)}"
        print(log_message)
        logging.error(log_message)

    # Сохранение данных после обработки
    save_json(user_search_data, user_search_file_path)
    save_json(faiss_statistics, faiss_statistics_file_path)

if __name__ == "__main__":
    try:
        user_search_request()
    except Exception as e:
        log_message = f"An error occurred: {str(e)}"
        print(log_message)
        logging.error(log_message)
