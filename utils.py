import json
def load_json_file(path):
    with open(path) as f:
        data = json.load(f)
        return data