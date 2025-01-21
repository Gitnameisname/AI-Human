import json

def get_json_data(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

def get_data_from_key(data, key: str, key_value: str):
    for item in data:
        if item[key] == key_value:
            return item