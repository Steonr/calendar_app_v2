import json
from infra.config_loader import ConfigLoader


def get_json(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)