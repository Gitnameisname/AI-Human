from src.utils import *
from src.constants import *

class MindMap:
    def __init__(self, logManager):
        self.logManager = logManager
        self.identity = get_json_data(IDENTITYFILE_PATH)
        self.logManager.log_info(f"Identity Load: OK\nIdentity:\n{self.identity}")

        self.td_memory = self.load_memory

    def load_identity():
        return get_json_data(IDENTITYFILE_PATH)
    
    def load_memory(path):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file) 

        return data
    
    def create_td_memory():
        return []
    
    def add_td_memory(speaker, content):
        memory_entry = {
            "time": get_current_time(),
            "speaker": speaker,
            "content": content
        }