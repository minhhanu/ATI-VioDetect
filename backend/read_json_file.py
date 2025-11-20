import json

def read_json_file(file_path):
    """
    Đọc file JSON và trả về dict
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

