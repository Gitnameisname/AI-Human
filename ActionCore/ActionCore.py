import json
import importlib

from MindMap.LogManager import LogManager
from src.constants import MODULEDB_DIR

class ActionCore:
    def __init__(self, logManager: LogManager):
        self.logManager = logManager
        self.logManager.log_info(f"(ActionCore) Load: OK")
        with open(f"{MODULEDB_DIR}", "r", encoding="utf-8") as f:
            self.modules = json.load(f)

    def listup_functions(self, module_name: str):
        module = importlib.import_module(module_name)

        functions = {
            name: obj.__doc__.replace("  ", "") for name, obj in vars(module).items() if callable(obj) and not name.startswith("__")
        }

        return functions
    
    def execute_function(self, module_name: str, function_info: dict):
        try:
            module = importlib.import_module(module_name)
            function_name = function_info.get("function_name")
            args = function_info.get("args", [])
            kwargs = function_info.get("kwargs", {})
            function = getattr(module, function_name)
            return function(*args, **kwargs)
        except Exception as e:
            self.logManager.log_error(f"(ActionCore) execute_function: {e}")
            raise