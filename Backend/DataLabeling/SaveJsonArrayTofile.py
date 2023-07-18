import json

def save_json_array_to_file(data, file_path):
    with open(file_path, 'w+') as file:
        json.dump(data, file)
