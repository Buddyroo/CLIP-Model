import json
import requests
import logging

def process_only_text_data(video_id, text):
    url = "http://127.0.0.1:8000/encode"

    files = []  # Пустой список файлов
    data = {'texts': text}  # Передача текста как строка

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            response_json = response.json()
            vector = response_json.get('text_features', None)
            result = True if vector else False
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

def process_first_n_videos(input_file, output_file, n=3):
    with open(input_file, 'r', encoding='utf-8') as infile:
        all_videos = json.load(infile)

    vectors_dict = {}
    total_processing_time = 0
    count = 0

    for video_id, video_data in all_videos.items():
        if count >= n:
            break
        keywords = video_data.get('subtitles', None)
        print(keywords)
        if keywords:
            text = ', '.join(keywords)
            print(text)
            result, vector = process_only_text_data(video_id, text)
            if result and vector:
                vectors_dict[video_id] = vector[0]  # Предполагается, что vector возвращает список с одним элементом
                total_processing_time += video_data['processing_time']
                count += 1

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(vectors_dict, outfile, ensure_ascii=False, indent=4)

    average_processing_time = total_processing_time / count if count > 0 else 0
    print(f"Processed {count} videos")
    print(f"Total processing time: {total_processing_time:.2f} seconds")
    print(f"Average processing time: {average_processing_time:.2f} seconds")

if __name__ == "__main__":
    input_file = 'subtitles_new_2.json'
    output_file = 'subtitles_vectors_2.json'
    process_first_n_videos(input_file, output_file, n=3)
