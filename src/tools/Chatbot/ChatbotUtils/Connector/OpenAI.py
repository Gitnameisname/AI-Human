from openai import OpenAI

def construct_prompt_with_context(main_prompt, conversation_history=[], prompt_extension='', conclusion=""):
    """
    사용자 메시지와 시스템 컨텍스트를 사용하여 프롬프트를 생성합니다.
    """

    if not conversation_history:
        return main_prompt + f"\n{prompt_extension}"
    
    full_prompt = ''
    for user_msg, agent_response in conversation_history:
        full_prompt += f"User: {user_msg}\nModel: {agent_response}\n"
    
    full_prompt += f"{main_prompt}"

    if conclusion:
        full_prompt += f"\nConclusion: {conclusion}"
    
    return full_prompt + f"\n{prompt_extension}"

def generate(client: OpenAI, model_name, prompt, system_context="",
             max_tokens=4096, temperature=0.7, top_p=0.7):
    """
    OpenAI API를 사용하여 언어 모델의 응답을 생성합니다.
    """

    if system_context:
        message = [
            {"role": "system", "content": system_context},
            {"role": "user", "content": prompt}
        ]
    else:
        message = [{"role": "user", "content": prompt}]

    # OpenAI API를 사용하여 언어 모델의 응답을 생성합니다.
    completion = client.chat.completions.create(
        model=model_name,
        messages=message,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p
    )

    return completion.choices[0].message.content.strip()

def generate_stream(client: OpenAI, model_name, prompt, system_context="",
                    max_tokens=4096, temperature=0.7, top_p=0.7):
    """
    OpenAI API를 사용하여 언어 모델의 응답을 생성합니다.
    """

    if system_context:
        message = [
            {"role": "system", "content": system_context},
            {"role": "user", "content": prompt}
        ]
    else:
        message = [{"role": "user", "content": prompt}]

    # OpenAI API를 사용하여 언어 모델의 응답을 생성합니다.
    completion = client.chat.completions.create(
        model=model_name,
        messages=message,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True
    )

    partial_completion = ''

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            chunk_message = chunk.choices[0].delta.content
            partial_completion += chunk_message
            yield partial_completion, chunk_message