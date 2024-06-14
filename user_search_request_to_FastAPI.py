import json
import time
import os
import logging
import numpy as np
from upload_only_TEXT_vector import process_only_text_data
from faiss_module import FaissIndex  # Импортируем класс FaissIndex
from upload_search_request_to_CLIP import process_search_request

# Настройка логирования
logging.basicConfig(filename='processing.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Путь к файлам для записи и загрузки индексов
video_index_file_path = 'video_index.faiss'
text_index_file_path = 'text_index.faiss'
user_search_file_path = 'user_search.json'
faiss_statistics_file_path = 'FAISS_statistics.json'
all_videos_file_path = 'video_description/all_videos.json'
vectors_file_path = 'vectors_separated_frames_1.json'

# Загрузка комбинированных векторов из файла
def load_combined_vectors(file_path=vectors_file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            combined_vectors = json.load(f)
            logging.debug(f"Combined vectors loaded: {combined_vectors}")
        except json.JSONDecodeError as e:
            logging.error(f"Error loading JSON file {file_path}: {str(e)}")
            raise
    video_vectors = [np.array(vector) for v in combined_vectors.values() for vector in v.get('vectors', [])]
    text_vectors = [np.array(v['text_vector'][0]) for v in combined_vectors.values() if v.get('text_vector')]
    logging.debug(f"Video vectors: {video_vectors}")
    logging.debug(f"Text vectors: {text_vectors}")
    return combined_vectors, video_vectors, text_vectors

try:
    combined_vectors, video_vectors, text_vectors = load_combined_vectors()
    logging.info("Successfully loaded combined vectors.")
except Exception as e:
    logging.error(f"Failed to load combined vectors: {str(e)}")
    raise

# Размерность векторов
d = len(video_vectors[0])
logging.info(f"Vector dimension: {d}")

# Создание или загрузка Faiss индексов
video_index = FaissIndex(d, index_type='FlatL2')
text_index = FaissIndex(d, index_type='FlatL2')

if os.path.exists(video_index_file_path) and os.path.exists(text_index_file_path):
    # Загрузка индексов из файлов
    video_index.load_index(video_index_file_path)
    text_index.load_index(text_index_file_path)
    logging.info("Loaded existing Faiss indices.")
else:
    # Добавление векторов и сохранение индексов
    video_index.add_vectors(np.vstack(video_vectors).astype('float32'))
    text_index.add_vectors(np.vstack(text_vectors).astype('float32'))
    video_index.save_index(video_index_file_path)
    text_index.save_index(text_index_file_path)
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
        # Преобразование search_query в список
        success, vector = process_search_request([search_query])
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
        text_distances, text_indices = text_index.search_vectors(query_vector, k)
        faiss_search_time = time.time() - start_faiss_time

        logging.info(f"FAISS search time: {faiss_search_time:.2f} seconds.")
        logging.debug(f"Video distances: {video_distances}, Video indices: {video_indices}")
        logging.debug(f"Text distances: {text_distances}, Text indices: {text_indices}")

        video_results = []
        text_results = []

        for i in range(k):
            best_video_match = list(combined_vectors.values())[video_indices[0][i]]
            best_text_match = list(combined_vectors.values())[text_indices[0][i]]

            video_description = all_videos.get(list(combined_vectors.keys())[video_indices[0][i]], {}).get('description', '')
            text_description = all_videos.get(list(combined_vectors.keys())[text_indices[0][i]], {}).get('description', '')

            video_results.append({
                "url": best_video_match['url'],
                "description": video_description,
                "type": 'video',
                "video_distance": float(video_distances[0][i]),
                "text_distance": float(text_distances[0][i])
            })

            text_results.append({
                "url": best_text_match['url'],
                "description": text_description,
                "type": 'text',
                "video_distance": float(video_distances[0][i]),
                "text_distance": float(text_distances[0][i])
            })

        user_search_data[search_query] = clip_processing_time
        faiss_statistics[search_query] = {
            "video_results": video_results,
            "text_results": text_results,
            "clip_processing_time": clip_processing_time,
            "faiss_search_time": faiss_search_time
        }

        formatted_video_results = "\n".join([f"{i+1}. Video Distance: {result['video_distance']:.2f}, Text Distance: {result['text_distance']:.2f}\nDescription: {result['description']}\nURL: {result['url']}" for i, result in enumerate(video_results)])
        formatted_text_results = "\n".join([f"{i+1}. Video Distance: {result['video_distance']:.2f}, Text Distance: {result['text_distance']:.2f}\nDescription: {result['description']}\nURL: {result['url']}" for i, result in enumerate(text_results)])

        log_message = (f"Successfully processed data for query '{search_query}'.\n"
                       f"Processing time: {clip_processing_time:.2f} seconds,\n"
                       f"FAISS search time: {faiss_search_time:.2f} seconds.\n"
                       f"Top 10 results by video distance:\n{formatted_video_results}\n\n"
                       f"Top 10 results by text distance:\n{formatted_text_results}")
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
