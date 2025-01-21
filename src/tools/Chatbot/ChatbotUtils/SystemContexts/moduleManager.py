import json
from src.constants import PERSONADB_DIR, MODULEDB_DIR

def module_manager_system_context():
    with open(f"{MODULEDB_DIR}", "r", encoding="utf-8") as f:
        modules = json.load(f)

    with open(f"{PERSONADB_DIR}/module_manager.json", "r", encoding="utf-8") as f:
        persona = json.load(f)

    persona['modules'] = modules['modules']
    system_context = f"""
{persona}
"""
    return system_context

def function_manager_system_context(function_list: list):

    with open(f"{PERSONADB_DIR}/function_manager.json", "r", encoding="utf-8") as f:
        persona = json.load(f)

    persona['functions'] = function_list
    system_context = f"""
{persona}
"""
    return system_context