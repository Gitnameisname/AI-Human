import json
from src.constants import PERSONADB_DIR

def math_solving_problem_system_context():
    with open(f'{PERSONADB_DIR}/math_solving_plan.json', 'r', encoding='utf-8') as f:
        persona = json.load(f)

    system_context = f"""
{persona}
"""
    return system_context

def math_system_context():
    with open(f'{PERSONADB_DIR}/math_solving.json', 'r', encoding='utf-8') as f:
        persona = json.load(f)
    system_context = f"""
{persona}
"""
    return system_context