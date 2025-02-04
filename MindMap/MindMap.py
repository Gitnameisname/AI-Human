import datetime

from MindMap.LogManager import LogManager
from MindMap.MindMapUtils.manageMemoryFile import *
from src.tools.file.json import *
from src.constants import *

class MindMap:
    def __init__(self, logManager: LogManager):
        self.logManager = logManager
        self.tdm_filepath = create_memory_file()
        self.identity = get_json_data(IDENTITYFILE_PATH)
        self.logManager.log_info(f"Identity Load: OK\nIdentity:\n{self.identity}")

        self.td_memory = load_memory(self.tdm_filepath)
        self.ti_memory = load_memory(R_TI_MEMORY_PATH)
        self.sago_process_memory = []
    
    def add_td_memory(self, category: str, speaker, contents):
        memory_entry = {
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "speaker": speaker,
            "contents": contents
        }

        self.td_memory.append(memory_entry)
        save_memory(self.tdm_filepath, self.td_memory, self.logManager)

    def add_ti_memory(self, entry_id, subject, tags, contents):
        new_entry = {
            "id": entry_id,
            "subject": subject,
            "tags": tags,
            "contents": contents
        }

        self.ti_memory.append(new_entry)
        save_memory(R_TI_MEMORY_PATH, self.ti_memory, self.logManager)

    def add_sago_process_memory(self, action:str, request: str, result: str):
        new_entry = {
            "action": action,
            "request": request,
            "result": result
        }
        self.sago_process_memory.append(new_entry)

    def add_instance_memory(self, memory: list, actor: str, action:str, request: str, result: str) -> list:
        new_entry = {
            "actor": actor,
            "action": action,
            "request": request,
            "result": result
        }

        memory.append(new_entry)
        return memory


    def initialize_sago_process_memory(self):
        self.sago_process_memory = []
