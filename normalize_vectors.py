import json
import numpy as np
import torch

def normalize_vector(vector):
    tensor = torch.tensor(vector)
    norm = torch.norm(tensor)
    normalized_tensor = tensor / norm if norm > 0 else tensor
    return normalized_tensor.tolist()

def normalize_features(features):
    return [normalize_vector(feature) for feature in features]

def check_vector_dimensions(vectors):
    expected_length = len(vectors[0])
    for i, vector in enumerate(vectors):
        if len(vector) != expected_length:
            return i, len(vector), expected_length
    return None

def normalize_json_vectors(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    for key, value in data.items():
        if 'vectors' in value:
            value['vectors'] = normalize_features(value['vectors'])
            # Проверка размеров векторов после нормализации
            result = check_vector_dimensions(value['vectors'])
            if result is not None:
                i, vector_length, expected_length = result
                print(f"Error: Vectors have different dimensions for key {key} at index {i}. "
                      f"Found length {vector_length}, expected length {expected_length}")
                return

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    input_file = 'vectors_to_normalize_7.json'
    output_file = 'ADD_to_db/DONE_normalized_vectors_6.json'
    normalize_json_vectors(input_file, output_file)
    print(f"Normalized vectors saved to {output_file}")
