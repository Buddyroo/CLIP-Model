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

def process_all_videos(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        all_videos = json.load(infile)

    vectors_dict = {}

    for video_id, video_data in all_videos.items():
        transcription = video_data.get('subtitles', None)
        if transcription:
            result, vector = process_only_text_data(video_id, transcription)
            if result and vector:
                vectors_dict[video_id] = vector[0]  # Предполагается, что vector возвращает список с одним элементом

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(vectors_dict, outfile, ensure_ascii=False, indent=4)

    total_processing_time = sum(video['processing_time'] for video in all_videos.values())
    average_processing_time = total_processing_time / len(all_videos)
    print(f"Total processing time: {total_processing_time:.2f} seconds")
    print(f"Average processing time: {average_processing_time:.2f} seconds")

if __name__ == "__main__":
    input_file = 'subtitles_new_2.json'
    output_file = 'subtitles_vectors_2.json'
    process_all_videos(input_file, output_file)

