import json
from src.constants import PERSONADB_DIR

def answering_system_context(user_msg: str, conclusion: str):
    with open(f'{PERSONADB_DIR}/answering.json', 'r', encoding='utf-8') as f:
        persona = json.load(f)
    persona['conclusion'] = conclusion

    system_context = f"""
{persona}
"""
    return system_context