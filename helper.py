import json
import os


def convert_keys_to_int(d):
    return {int(k) if k.isdigit() else k: v for k, v in d.items()}


def load_json(filename: str):
    if os.path.exists(filename):
        with open(filename, mode='r', encoding="utf-8") as f:
            return json.load(f, object_hook=convert_keys_to_int)
    else:
        return {}


def save_json(data, filename: str):
    with open(filename, mode='w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
