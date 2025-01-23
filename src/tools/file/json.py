import json

def get_json_data(path):
    """
    path 경로에 있는 json 파일을 읽어서 dict 형태로 반환합니다.

    Args:
        path (str): json 파일 경로

    Returns:
        dict: json 파일을 읽은 dict 데이터
    """
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

def get_data_from_key(data: dict, key: str, key_value: str):
    """
    data에서 key가 key_value인 항목을 반환합니다.

    Args:
        data (dict): 데이터
        key (str): 키
        key_value (str): 키 값

    Returns:
        dict: key가 key_value인 항목
    """
    for item in data:
        if item[key] == key_value:
            return item