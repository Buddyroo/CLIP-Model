import json
import numpy as np

def check_vector_dimensions(vectors):
    expected_length = len(vectors[0])
    for i, vector in enumerate(vectors):
        if len(vector) != expected_length:
            return i, len(vector), expected_length
    return None

def check_json_vectors(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    for key, value in data.items():
        if 'vectors' in value:
            result = check_vector_dimensions(value['vectors'])
            if result is not None:
                i, vector_length, expected_length = result
                print(f"Error: Vectors have different dimensions for key {key} at index {i}. "
                      f"Found length {vector_length}, expected length {expected_length}")

if __name__ == "__main__":
    input_file = '/DONE_normalized_vectors_2.json'
    check_json_vectors(input_file)
