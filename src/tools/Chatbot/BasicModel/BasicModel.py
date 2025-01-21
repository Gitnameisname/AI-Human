from openai import OpenAI

from src.tools.Chatbot.ChatbotUtils.Connector.OpenAI import *
from src.tools.Chatbot.ChatbotUtils.Conversation.history import trim_conversation_history
from src.tools.Chatbot.BasicModel.selectTokenizer import selectTokenizer
from src.tools.file.json import *
from src.constants import AGENT_INFOFILE_PATH

class BasicModel:
    def __init__(self, model_name:str, max_tokens=1024):
        self.model_info = get_data_from_key(get_json_data(AGENT_INFOFILE_PATH), "model_name", model_name)

        self.client = OpenAI(
                        api_key=self.model_info['api_key']
        )

        self.max_tokens = max_tokens
        self.tokenizer = selectTokenizer(model_info=self.model_info)
        self.conversation_history = []

    def chat(self, user_msg, memory=None, system_context="", prompt_extention="", temperature: float = 0.7, top_p: float = 0.7):

        if memory:
            trimed_conversation_history = trim_conversation_history(memory=memory, tokenizer=self.tokenizer, max_tokens=self.max_tokens)
            prompt = construct_prompt_with_context(user_msg, conversation_history=trimed_conversation_history, prompt_extension=prompt_extention)

        else:
            prompt = construct_prompt_with_context(user_msg,  prompt_extension=prompt_extention)
        
        # 언어 모델의 응답을 가져옵니다.
        agent_response = generate(client=self.client, model_name=self.model_info['model_name'], prompt=prompt, system_context=system_context, temperature=temperature, top_p=top_p)

        return agent_response
    
    def stream_chat(self, user_msg, memory=None, system_context="", prompt_extention="", temperature: float = 0.7, top_p: float = 0.7):

        if memory:
            trimed_conversation_history = trim_conversation_history(memory=memory, tokenizer=self.tokenizer, max_tokens=self.max_tokens)
            prompt = construct_prompt_with_context(user_msg, conversation_history=trimed_conversation_history, prompt_extension=prompt_extention)
        
        else:
            prompt = construct_prompt_with_context(user_msg, prompt_extension=prompt_extention)

        for agent_response, _ in generate_stream(client=self.client, model_name=self.model_info['model_name'], prompt=prompt, system_context=system_context, temperature=temperature, top_p=top_p):
                yield agent_response