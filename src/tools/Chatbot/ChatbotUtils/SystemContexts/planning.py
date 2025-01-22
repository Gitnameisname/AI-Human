import json
from src.constants import PERSONADB_DIR

def planning_system_context():
    with open(f'{PERSONADB_DIR}/planning.json', 'r', encoding='utf-8') as f:
        persona = json.load(f)

    system_context = f"""
{persona}
"""
    return system_context