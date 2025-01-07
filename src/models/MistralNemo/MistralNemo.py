from transformers import AutoTokenizer
from openai import OpenAI

from src.utils.chatutils import *
from src.constants import MISTRALNEMO_TOKENIZER_DIR, MISTRALNEMO_URL


class MistralNemo:
    def __init__(self, max_tokens=1024):
        self.client = OpenAI(
                        base_url = MISTRALNEMO_URL,
                        api_key="EMPTY"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(MISTRALNEMO_TOKENIZER_DIR)
        self.max_tokens = max_tokens
        self.conversation_history = []

    def chat(self, user_msg, system_context=""):
        # 대화 이력과 새 사용자 메시지를 사용하여 프롬프트를 생성합니다.
        messages = construct_prompt_with_context(user_msg, system_context, self.conversation_history)
        
        # 언어 모델의 응답을 가져옵니다.
        completion = generate(client=self.client, messages=messages)

        # 언어 모델의 응답에서 텍스트를 추출합니다.
        agent_response = completion.choices[0].message.content

        # 이 대화를 대화 이력에 저장합니다.
        self.conversation_history.append((user_msg, agent_response))

        # Check and maintain the conversation history within the token limit
        self._trim_conversation_history()

        return agent_response
    
    def stream_chat(self, user_msg, system_context=""):

        # 대화 이력과 새 사용자 메시지를 사용하여 프롬프트를 생성합니다.
        messages = construct_prompt_with_context(user_msg, system_context, self.conversation_history)

        agent_response = ""
        for chunk in generate_stream(client=self.client, messages=messages, stream=True):
            if chunk is not None:
                agent_response += chunk
                yield agent_response
                

        # 이 대화를 대화 이력에 저장합니다.
        self.conversation_history.append((user_msg, agent_response))

        # Check and maintain the conversation history within the token limit
        self._trim_conversation_history()

    def _trim_conversation_history(self):
        """
        대화 이력을 유지하기 위해 토큰 수를 지정한 제한 값 이하로 줄입니다.
        """

        # 대화 이력을 하나의 문자열로 연결합니다.
        history_string = ''.join(user + agent for user, agent in self.conversation_history)
        
        # 대화 이력의 토큰 수를 계산합니다.
        history_tokens = len(self.tokenizer.encode(history_string))

        # 대화 이력이 최대 토큰 제한을 초과하는 경우, 가장 오래된 항목을 제거합니다.
        while history_tokens > self.max_tokens:
            # 항상 뽑아낼 항목이 하나 이상 있는지 확인합니다.
            if self.conversation_history:
                # 가장 오래된 대화 튜플을 제거합니다.
                self.conversation_history.pop(0)
                # 대화 이력 문자열과 해당 토큰을 다시 계산합니다.
                history_string = ''.join(user + agent for user, agent in self.conversation_history)
                history_tokens = len(self.tokenizer.encode(history_string))
            else:
                # 대화 이력이 비어 있으면 루프를 종료합니다.
                break

    def reset(self):
        """
        대화 이력을 재설정합니다.

        이 방법은 기존 대화 이력을 지우고 대화를 다시 시작합니다.
        """
        # 대화 이력을 비웁니다.
        self.conversation_history = []