import os
import json
import datetime

from MindMap.LogManager import LogManager
from src.tools.file.json import *
from src.constants import *

def create_memory_file():
    tdm_filename = datetime.datetime.now().strftime("%Y%m%d") + ".json"
    tdm_filepath = os.path.join(R_TD_MEMORY_PATH, tdm_filename)

    if not os.path.exists(tdm_filepath):
        with open(tdm_filepath, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

    if not os.path.exists(R_TI_MEMORY_PATH):
        with open(R_TI_MEMORY_PATH, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

    return tdm_filepath

def load_identity(logManager: LogManager):
    try:
        with open(f'{PERSONADB_DIR}/identity.json', 'r', encoding='utf-8') as file:
            logManager.log_info(f"Identity Load: OK")
            identity = json.load(file)

        return identity
    
    except FileNotFoundError:
        logManager.log_error(f"Identity Load: Failed - File not found")
        return {}

def load_memory(memory_path):
    return get_json_data(memory_path)
    
def search_td_memory(date: str):
    """
    TD Memory 폴더에서, date에 해당하는 파일 이름을 찾아 읽고 내용을 반환합니다.
    Date 파일 이름 형식은 "YYYYMMDD.json" 입니다.
    만약 date 변수가 "YYYY-MM-DD"로 들어오면, YYYYMMDD로 변환하여 찾습니다.
    """
    date = date.replace("-", "")
    memory_path = os.path.join(R_TD_MEMORY_PATH, f"{date}.json")

    json_data = get_json_data(memory_path)

    return json_data
    
def get_new_tim_id(last_id):
    num = int(last_id[-4:]) + 1
    new_id = last_id[:-4] + str(num).zfill(4)
    return new_id

def save_memory(MEMORY_DIR, memory, logManager: LogManager):
    try:
        with open(MEMORY_DIR, "w", encoding="utf-8") as file:
            json.dump(memory, file, ensure_ascii=False, indent=4)

    except FileNotFoundError:
        logManager.log_error(f"Memory Save: Failed - File not found")