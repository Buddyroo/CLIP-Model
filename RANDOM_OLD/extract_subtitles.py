import json
import os
import subprocess
import requests


def download_video(url, output_path):
    response = requests.get(url, stream=True)
    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    return output_path


def extract_subtitles(video_path, subtitles_path):
    try:
        result = subprocess.run([
            'ffmpeg', '-i', video_path, '-map', '0:s:0', subtitles_path
        ], check=True, capture_output=True, text=True)
        print(f"FFmpeg output: {result.stdout}")

        if os.path.exists(subtitles_path):
            with open(subtitles_path, 'r', encoding='utf-8') as file:
                subtitles = file.read()
            os.remove(subtitles_path)
            return subtitles
        else:
            return None
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при извлечении субтитров: {e.stderr}")
        return None


def process_video(url, output_file='video_description/subtitles.json'):
    video_id = os.path.basename(url).split('.')[0]
    video_path = f"{video_id}.mp4"
    subtitles_path = f"{video_id}.srt"

    # Загружаем существующие субтитры, если файл уже существует
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as file:
            subtitles_dict = json.load(file)
    else:
        subtitles_dict = {}

    # Проверяем, существуют ли субтитры для этого видео
    if url in subtitles_dict:
        print(f"Субтитры для {url} уже существуют.")
        return

    print(f"Загрузка видео из {url}")
    download_video(url, video_path)

    print(f"Извлечение субтитров из {video_path}")
    subtitles = extract_subtitles(video_path, subtitles_path)
    os.remove(video_path)

    if subtitles:
        subtitles_dict[url] = subtitles
    else:
        subtitles_dict[url] = "Субтитры недоступны или отсутствуют"

    # Сохраняем словарь субтитров в файл
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(subtitles_dict, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # Пример использования функции process_video
    video_url = "https://cdn-st.rutubelist.ru/media/db/ab/c910dec14495b48479fb6991f68b/fhd.mp4"
    process_video(video_url)
