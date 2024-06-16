import torch
import torch.nn as nn

# Пример векторов
v1 = torch.tensor([1.0, 2.0, 3.0])
v2 = torch.tensor([4.0, 5.0, 6.0])

# Усреднение
v_combined_avg = (v1 + v2) / 2

# Суммирование
v_combined_sum = v1 + v2

# Конкатенация и линейная трансформация
v_concat = torch.cat((v1, v2), dim=0)
print("Конкатенация:", v_concat)
linear_layer = nn.Linear(6, 3)  # Пример: линейный слой, который переводит из размерности 6 в 3
v_combined_linear = linear_layer(v_concat)

print("Усреднение:", v_combined_avg)
print("Суммирование:", v_combined_sum)
print("Конкатенация с линейной трансформацией:", v_combined_linear)