import json
from src.constants import PERSONADB_DIR

def coding_system_context(request: str):
    with open(f'{PERSONADB_DIR}/coding.json', 'r', encoding='utf-8') as f:
        persona = json.load(f)

    persona['request'] = request

    system_context = f"""
{persona}
"""
    return system_context