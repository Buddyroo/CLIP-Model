import requests
import os

url = "http://127.0.0.1:8000/encode"
frames_dir = "frames"

# Сбор путей к файлам изображений в директории frames
image_paths = [os.path.join(frames_dir, filename) for filename in os.listdir(frames_dir) if filename.endswith(('.jpg'))]

# Отправка POST-запроса с путями к изображениям
response = requests.post(url, json={"image_paths": image_paths})

if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to get a proper response. Status code: {response.status_code}")
    print("Response:", response.text)
