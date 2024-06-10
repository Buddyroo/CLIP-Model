from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["video_index"]

# Создание коллекции для векторов
collection = db["vectors"]

# Создание индекса для поля vector (если требуется)
collection.create_index([("vector", "2dsphere")])