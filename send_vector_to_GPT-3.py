import json
import openai

# Установка вашего API ключа OpenAI
openai.api_key = 'your_openai_api_key'

# Загрузка данных из файла
with open('vectors_1.json', 'r') as file:
    data = json.load(file)


# Функция для получения вектора по video_id
def get_vector_by_video_id(video_id, data):
    if video_id in data:
        return data[video_id]['vector'][0]  # Предполагается, что вектор внутри списка
    else:
        raise ValueError("Video ID not found")


# Функция для генерации текста на основе эмбеддинга
def generate_text_from_embedding(embedding):
    # Преобразуем эмбеддинг в строку, чтобы передать его в GPT-3
    embedding_str = ','.join(map(str, embedding))

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Опишите изображение с эмбеддингом: {embedding_str}"}
        ]
    )
    return response['choices'][0]['message']['content']


# Пример использования
video_id = "ef285e0241139fc611318ed33071"
vector = get_vector_by_video_id(video_id, data)
text_description = generate_text_from_embedding(vector)
print(text_description)
