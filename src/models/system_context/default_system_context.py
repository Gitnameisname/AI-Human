def default_system_context(identity):
    system_context = f"""
I am a conversational AI Agent designed to assist my master with a variety of tasks and inquiries. Here is my identity:\n{identity}
"""
    return system_context