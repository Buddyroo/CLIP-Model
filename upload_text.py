import requests

url = "http://127.0.0.1:8000/encode"

data = {
    "texts": ["Привет, мир!", "Губная помада"]
}

response = requests.post(url, json=data)

# Печать ответа от сервера
print(response.json())