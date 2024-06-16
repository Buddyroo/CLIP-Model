import json

def find_json_error(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
        json.loads(data)
        print("No errors found in the JSON file.")
    except json.JSONDecodeError as e:
        print(f"Error: {str(e)} at line {e.lineno}, column {e.colno}, char {e.pos}")
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            error_line = lines[e.lineno - 1] if e.lineno <= len(lines) else None
            if error_line:
                print(f"Error in line {e.lineno}: {error_line}")

# Замените 'vectors_separated_frames_1.json' на путь к вашему JSON-файлу
find_json_error('vectors_to_normalize_6.json')
