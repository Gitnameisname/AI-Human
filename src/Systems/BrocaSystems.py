from src.tools.Chatbot.OpenAI.gpt_4o_mini import gpt_4o_mini
from src.tools.Chatbot.ChatbotUtils.SystemContexts import *

from MindMap.MindMap import MindMap
from src.Systems.SaGoSystems import SaGoSystems

class BrocaSystems:
    def __init__(self, logManager):
        self.logManager = logManager
        self.mindMap = MindMap(self.logManager)
        self.logManager.log_info(f"MindMap Load: OK")
        self.chatbot = gpt_4o_mini()
        self.logManager.log_info(f"MistralNemo Load: OK")
        self.saGoSystems = SaGoSystems(self.logManager, self.mindMap)
        self.logManager.log_info(f"SaGoSystems Load: OK")

    def chat(self, user_msg):
        self.logManager.log_info(f"User: {user_msg}")
        system_context = default_system_context(self.mindMap.identity)
        agent_response = self.chatbot.chat(user_msg=user_msg, system_context=system_context)
        self.logManager.log_info(f"Model: {agent_response}")

        return agent_response
    
    def stream_chat(self, user_msg):
        self.logManager.log_info(f"User: {user_msg}")

        plan = self.saGoSystems.planning(user_msg)
        conclusion = ""
        if len(plan) > 1:
            conclusion = self.saGoSystems.SaGoProcess(user_msg=user_msg, plan=plan[:-1])

        system_context = answering_system_context(user_msg=user_msg, conclusion=conclusion)

        for agent_response in self.chatbot.stream_chat(user_msg=user_msg, memory=self.mindMap.td_memory, system_context=system_context):
            yield agent_response

        self.mindMap.add_td_memory(category="answering", speaker="User", contents=user_msg)
        self.mindMap.add_td_memory(category="answering", speaker="Model", contents=agent_response)