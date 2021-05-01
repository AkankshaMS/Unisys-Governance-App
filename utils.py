import json
import os
def load_json_file(path):
    with open(path) as f:
        data = json.load(f)
        return data

def isLinux():
    return os.name=="posix"