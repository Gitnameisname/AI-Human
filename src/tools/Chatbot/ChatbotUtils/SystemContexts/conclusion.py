import json
from src.constants import PERSONADB_DIR

def conclusion_system_context(user_msg: str, thougths: list):
    with open(f'{PERSONADB_DIR}/conclusion.json', 'r', encoding='utf-8') as f:
        persona = json.load(f)

    persona['user_message'] = user_msg
    persona['thoughts_process'] = thougths

    system_context = f"""
{persona}
"""
    return system_context