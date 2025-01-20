def trim_conversation_history(memory, tokenizer, max_tokens):

    if memory is not []:
        conversation_history = convert_memory_to_char(memory)
    else:
        conversation_history = []


    history_string = ''.join(user + agent for user, agent in conversation_history)

    history_tokens = len(tokenizer.encode(history_string))

    while history_tokens > max_tokens:
        if conversation_history:
            conversation_history.pop(0)
            history_string = ''.join(user + agent for user, agent in conversation_history)
            history_tokens = len(tokenizer.encode(history_string))
        else:
            break

    return conversation_history

def convert_memory_to_char(memory):
    conversation_history = []
    checker = False
    user_msg = ''
    agent_msg = ''
    for entry in memory:
        if entry['speaker'].lower() == 'user':
            checker = True
            user_msg = entry['contents']

        if checker and entry['speaker'].lower() == 'agent':
            checker = False
            agent_msg = entry['contents']
            conversation_history.append((user_msg, agent_msg))

    return conversation_history
            
