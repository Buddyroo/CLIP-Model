import torch

# Загрузка модели
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Выполнение детектирования
img = 'data/images/zidane.jpg'  # или путь к вашему изображению
results = model(img)

# Отображение результатов
results.show()

# Сохранение результатов
results.save('results/')
