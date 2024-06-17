import json
import os


def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            content = file.read().strip()
            if content:
                return json.loads(content)
            else:
                raise ValueError(f"File {file_path} is empty.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error loading JSON file {file_path}: {str(e)}")


def check_and_fix_vectors_dimension(json_data, expected_dim=None):
    for key, value in json_data.items():
        vectors = value.get("vectors", [])
        fixed_vectors = []
        for vector in vectors:
            if expected_dim is None:
                expected_dim = len(vector)
            if len(vector) == expected_dim:
                fixed_vectors.append(vector)
            else:
                print(
                    f"Removing vector of incorrect dimension {len(vector)} for key {key}. Expected dimension: {expected_dim}")
        value["vectors"] = fixed_vectors

    return json_data, expected_dim


def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def main(json_file_path, output_file_path):
    try:
        json_data = load_json(json_file_path)
        fixed_json_data, expected_dim = check_and_fix_vectors_dimension(json_data)
        save_json(fixed_json_data, output_file_path)
        print(
            f"All vectors have been checked. Consistent dimension: {expected_dim}. Fixed data saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    json_file_path = 'DONE_normalized_vectors_1.json'
    output_file_path = 'ADD_to_db/DONE_normalized_vectors_1.json'
    main(json_file_path, output_file_path)
