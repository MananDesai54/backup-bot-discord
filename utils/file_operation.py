import json


def read_from_file(path: str):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def write_to_file(path: str, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
