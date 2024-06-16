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

def process_videos(input_file, output_file, start=1, count=2000):
    with open(input_file, 'r', encoding='utf-8') as infile:
        all_videos = json.load(infile)

    video_ids = list(all_videos.keys())[start:start+count]
    vectors_dict = {}
    total_processing_time = 0
    processed_count = 0

    for video_id in video_ids:
        description = all_videos.get(video_id, {}).get('description', None)
        if description:
            result, vector = process_only_text_data(video_id, description)
            if result and vector:
                vectors_dict[video_id] = vector[0]  # Предполагается, что vector возвращает список с одним элементом
                processed_count += 1
                total_processing_time += all_videos[video_id].get('processing_time', 0)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(vectors_dict, outfile, ensure_ascii=False, indent=4)

    average_processing_time = total_processing_time / processed_count if processed_count > 0 else 0
    print(f"Processed {processed_count} videos")
    print(f"Total processing time: {total_processing_time:.2f} seconds")
    print(f"Average processing time: {average_processing_time:.2f} seconds")

if __name__ == "__main__":
    input_file = 'all_videos.json'
    output_file = 'video_vectors.json'
    process_videos(input_file, output_file, start=1, count=2000)
