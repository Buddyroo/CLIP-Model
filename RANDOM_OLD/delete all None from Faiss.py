import json
import numpy as np


def remove_invalid_vectors(file_path='combined_vectors.json', output_path='cleaned_combined_vectors.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            combined_vectors = json.load(f)
            print("Combined vectors loaded successfully.")
        except json.JSONDecodeError as e:
            print(f"Error loading JSON file {file_path}: {str(e)}")
            return

    valid_combined_vectors = {}
    for key, value in combined_vectors.items():
        video_vector = value.get('video_vector')
        text_vector = value.get('text_vector')
        if video_vector and text_vector and video_vector[0] is not None and text_vector[0] is not None:
            valid_combined_vectors[key] = value

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(valid_combined_vectors, f, ensure_ascii=False, indent=4)
    print(f"Cleaned combined vectors saved to {output_path}.")

    return valid_combined_vectors


if __name__ == "__main__":
    cleaned_vectors = remove_invalid_vectors()
    print(f"Total valid vectors: {len(cleaned_vectors)}")
