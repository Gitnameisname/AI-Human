from src.models.MistralNemo.MistralNemo import MistralNemo
from MindMap.MindMap import MindMap
from src.utils import *
from src.models.system_context import *
from src.constants import *

class ChatBot:
    def __init__(self, logManager):
        self.logManager = logManager
        self.mindMap = MindMap(logManager)
        self.logManager.log_info(f"MindMap Load: OK")
        self.mistralNemo = MistralNemo()
        self.logManager.log_info(f"MistralNemo Load: OK")


    def chat(self, user_msg):
        self.logManager.log_info(f"User: {user_msg}")
        agent_response = self.mistralNemo.chat(user_msg)
        self.logManager.log_info(f"Model: {agent_response}")

        return agent_response
    
    def stream_chat(self, user_msg):
        self.logManager.log_info(f"User: {user_msg}")
        system_context = default_system_context(self.mindMap.identity)
        for agent_response in self.mistralNemo.stream_chat(user_msg, system_context):
            print(f"agent_response: {agent_response}")
            yield agent_response
        # self.logManager.log_info(f"Model: {agent_response}")