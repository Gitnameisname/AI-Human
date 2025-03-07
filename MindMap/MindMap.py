import os
import datetime

from MindMap.LogManager import LogManager
from src.tools.file.json import *
from src.constants import *

class MindMap:
    def __init__(self, logManager: LogManager):
        self.logManager = logManager
        self.tdm_filepath = self.create_memory_file()
        self.identity = get_json_data(IDENTITYFILE_PATH)
        self.logManager.log_info(f"Identity Load: OK\nIdentity:\n{self.identity}")

        self.td_memory = self.load_memory(self.tdm_filepath)
        self.ti_memory = self.load_memory(R_TI_MEMORY_PATH)
        self.sago_process_memory = []

    def create_memory_file(self):
        tdm_filename = datetime.datetime.now().strftime("%Y%m%d") + ".json"
        tdm_filepath = os.path.join(R_TD_MEMORY_PATH, tdm_filename)

        if not os.path.exists(tdm_filepath):
            with open(tdm_filepath, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

        if not os.path.exists(R_TI_MEMORY_PATH):
            with open(R_TI_MEMORY_PATH, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

        return tdm_filepath
    
    def load_identity(self):
        try:
            with open(f'{PERSONADB_DIR}/identity.json', 'r', encoding='utf-8') as file:
                self.logManager.log_info(f"Identity Load: OK")
                identity = json.load(file)

            return identity
        
        except FileNotFoundError:
            self.logManager.log_error(f"Identity Load: Failed - File not found")
            return {}
    
    def load_memory(self, memory_path):
        try:
            with open(memory_path, "r", encoding="utf-8") as file:
                data = json.load(file) 
            return data
        
        except FileNotFoundError:
            self.logManager.log_error(f"Memory Load: Failed - File not found")
            return []
    
    def add_td_memory(self, category: str, speaker, contents):
        memory_entry = {
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "speaker": speaker,
            "contents": contents
        }

        self.td_memory.append(memory_entry)
        self.save_memory(self.tdm_filepath, self.td_memory)

    def add_ti_memory(self, entry_id, subject, tags, contents):
        new_entry = {
            "id": entry_id,
            "subject": subject,
            "tags": tags,
            "contents": contents
        }

        self.ti_memory.append(new_entry)
        self.save_memory(R_TI_MEMORY_PATH, self.ti_memory)

    def get_new_tim_id(self, last_id):
        num = int(last_id[-4:]) + 1
        new_id = last_id[:-4] + str(num).zfill(4)
        return new_id
    
    def save_memory(self, MEMORY_DIR, memory):
        try:
            with open(MEMORY_DIR, "w", encoding="utf-8") as file:
                json.dump(memory, file, ensure_ascii=False, indent=4)

        except FileNotFoundError:
            self.logManager.log_error(f"Memory Save: Failed - File not found")

    def add_instance_memory(self, memory: list, actor: str, action:str, request: str, result: str) -> list:
        new_entry = {
            "actor": actor,
            "action": action,
            "request": request,
            "result": result
        }

        memory.append(new_entry)
        return memory

    def add_sago_process_memory(self, action:str, request: str, result: str):
        new_entry = {
            "action": action,
            "request": request,
            "result": result
        }
        self.sago_process_memory.append(new_entry)

    def initialize_sago_process_memory(self):
        self.sago_process_memory = []
