import os
import requests
from PIL import Image
from io import BytesIO

# URL вашего FastAPI приложения
url = "http://127.0.0.1:8000/encode"

# Директория, куда были сохранены кадры
frames_dir = "frames"

# Создаем список файлов для отправки
files = []
for filename in os.listdir(frames_dir):
    if filename.endswith(('.jpg')):
        image_path = os.path.join(frames_dir, filename)
        with open(image_path, 'rb') as img_file:
            files.append(('images', (filename, img_file.read(), 'image/jpeg')))

# Отправка POST-запроса с изображениями
response = requests.post(url, files=files)

# Проверяем, что ответ сервера успешен и пытаемся прочитать JSON
if response.status_code == 200:
    try:
        print(response.json())
    except ValueError:
        print("Response is not in JSON format.")
else:
    print(f"Failed to get a proper response. Status code: {response.status_code}")
    print("Response:", response.text)
