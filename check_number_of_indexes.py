import faiss
import os
import logging

# Настройка логирования
logging.basicConfig(filename='index_count.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Путь к файлам индексов
video_index_file_path = 'video_index.faiss'
text_index_file_path = 'text_index.faiss'

def load_index(file_path):
    if os.path.exists(file_path):
        index = faiss.read_index(file_path)
        return index
    else:
        logging.error(f"Index file {file_path} does not exist.")
        return None

def count_vectors_in_index(index):
    if index is not None:
        return index.ntotal
    else:
        logging.error("Index is None.")
        return 0

if __name__ == "__main__":
    video_index = load_index(video_index_file_path)
    text_index = load_index(text_index_file_path)

    total_vectors_video = count_vectors_in_index(video_index)
    total_vectors_text = count_vectors_in_index(text_index)

    log_message = (f"Total vectors in video index: {total_vectors_video}\n"
                   f"Total vectors in text index: {total_vectors_text}")

    print(log_message)
    logging.info(log_message)
