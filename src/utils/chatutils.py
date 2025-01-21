def generate_stream(client, messages, temperature=0.3, top_p=0.7, max_length=4096, conversation_history=[], stream=False):
    """
    Generates a response to the given prompt using a specified language model pipeline.

    This function takes a prompt and passes it to a language model pipeline, such as LLaMA, 
    to generate a text response. The function is designed to allow customization of the 
    generation process through various parameters and keyword arguments.

    Parameters:
    - prompt (str): The input text prompt to generate a response for.
    - max_length (int): The maximum length of the generated response. Default is 1024 tokens.
    - pipe (callable): The language model pipeline function used for generation. Default is llama_pipe.
    - **kwargs: Additional keyword arguments that are passed to the pipeline function.

    Returns:
    - str: The generated text response from the model, trimmed of leading and trailing whitespace.

    Example usage:
    ```
    prompt_text = "Explain the theory of relativity."
    response = generate(prompt_text, max_length=512, pipe=my_custom_pipeline, temperature=0.7)
    print(response)
    ```
    """

    completion = client.chat.completions.create(
            model="nv-mistralai/mistral-nemo-12b-instruct",
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_length,
            stream=stream
    )
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            if content.endswith("</s>"):
                content = content[:-4]
            else:
                content = content + " "
            yield content

def generate(client, messages, temperature=0.3, top_p=0.7, max_length=4096, conversation_history=[], stream=False):
    """
    Generates a response to the given prompt using a specified language model pipeline.

    This function takes a prompt and passes it to a language model pipeline, such as LLaMA, 
    to generate a text response. The function is designed to allow customization of the 
    generation process through various parameters and keyword arguments.

    Parameters:
    - prompt (str): The input text prompt to generate a response for.
    - max_length (int): The maximum length of the generated response. Default is 1024 tokens.
    - pipe (callable): The language model pipeline function used for generation. Default is llama_pipe.
    - **kwargs: Additional keyword arguments that are passed to the pipeline function.

    Returns:
    - str: The generated text response from the model, trimmed of leading and trailing whitespace.

    Example usage:
    ```
    prompt_text = "Explain the theory of relativity."
    response = generate(prompt_text, max_length=512, pipe=my_custom_pipeline, temperature=0.7)
    print(response)
    ```
    """
    completion = client.chat.completions.create(
            model="nv-mistralai/mistral-nemo-12b-instruct",
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_length
    )
    return completion


def construct_prompt_with_context(main_prompt, system_context="", conversation_history=[]):
    """
    언어 모델을 위해 완전히 구조화된 프롬프트를 구성합니다. 시스템 컨텍스트 및 대화 예시가 선택적으로 포함됩니다.

    이 함수는 언어 모델에서 응답을 생성하기 위해 직접 사용할 수 있는 프롬프트를 컴파일합니다.
    시스템 컨텍스트 메시지를 선택적으로 시작하여, 이전 상호작용으로 대화 예시를 추가하고, 주요 사용자 프롬프트로 끝나는 구조화된 형식을 생성합니다.
    시스템 컨텍스트나 대화 예시가 제공되지 않으면 주요 프롬프트만 반환합니다.

    매개변수들:
    - main_prompt (str): 언어 모델이 응답할 핵심 질문 또는 문장입니다.
    - system_context (str, 선택적): 시나리오나 환경에 대한 추가 컨텍스트나 정보입니다. 기본값은 빈 문자열입니다.
    - conversation_history (튜플의 리스트, 선택적): 컨텍스트로 제공된 이전 교환으로, 각 튜플은 사용자 메시지와 해당 에이전트 응답을 포함합니다. 기본값은 빈 리스트입니다.

    반환값:
    - str: 언어 모델 입력으로 준비된 완전한 프롬프트로 포맷된 문자열입니다. 시스템 컨텍스트나 예시가 제공되지 않으면 주요 프롬프트를 반환합니다.

    사용 예시:
    ```
    main_prompt = "I'm looking to improve my dialogue writing skills for my next short story. Any suggestions?"
    system_context = "User is an aspiring author seeking to enhance dialogue writing techniques."
    conversation_examples = [
        ("How can dialogue contribute to character development?", "Dialogue should reveal character traits and show personal growth over the story arc."),
        ("What are some common pitfalls in writing dialogue?", "Avoid exposition dumps in dialogue and make sure each character's voice is distinct.")
    ]

    full_prompt = construct_prompt_with_context(main_prompt, system_context, conversation_examples)
    print(full_prompt)
    ```
    """
    
    # 만약 시스템 컨텍스트도 없고, 대화 예시도 없다면 주요 프롬프트만 반환
    if not system_context and not conversation_history:
        message = [
            {
                "role": "user",
                "content": main_prompt
            }
        ]
        return message
    
    full_prompt = ""

    # 대화 이력이 주어진 경우, 이전 교환을 프롬프트에 추가
    for user_msg, agent_response in conversation_history:
        full_prompt += f"User: {user_msg}\nModel: {agent_response}\n\n"

    # 사용자 프롬프트를 마지막에 추가
    full_prompt += f"{main_prompt}\n"

    # 시스템 컨텍스트가 주어진 경우, 시스템 컨텍스트 메시지를 프롬프트에 추가
    if system_context:
        message = [
            {
                "role": "system",
                "content": system_context
            },
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    else:
        message = [
            {
                "role": "user",
                "content": full_prompt
            }
        ]

    return message