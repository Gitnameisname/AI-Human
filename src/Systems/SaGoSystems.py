import json
from MindMap.LogManager import LogManager
from src.tools.Chatbot.OpenAI.gpt_4o_mini import gpt_4o_mini
from MindMap.MindMap import MindMap
from src.Actions import *
from src.tools.Chatbot.ChatbotUtils.SystemContexts import planning_system_context
from src.tools.Chatbot.ChatbotUtils.Conversation.promptExtension import JSON_PROMPT_EXTENSION

class SaGoSystems:
    def __init__(self, logManager: LogManager, mindMap: MindMap):
        self.logManager = logManager
        self.mindMap = mindMap
        self.actionCore = ActionCore(logManager)
        self.chatbot = gpt_4o_mini()
        self.logManager.log_info(f"(SaGoSystems) Load: OK")

    def planning(self, user_msg):
        self.logManager.log_info(f"(SaGoSystems) Planning")
        system_context = planning_system_context()
        agent_response = self.chatbot.chat(user_msg=user_msg, system_context=system_context, prompt_extention=JSON_PROMPT_EXTENSION)

        plan = json.loads(agent_response)
        self.logManager.log_info(f"Plan:\n{plan}")

        return plan

    def SaGoProcess(self, user_msg):
        self.logManager.log_info(f"(SaGoSystems) SaGoProcess")
        plan = self.planning(user_msg)

        self.mindMap.initialize_instance_memory()
        self.mindMap.add_instance_memory(speaker='User', contents=user_msg)

        for action in plan:
            if action['action'] == 'module_retrieval':
                response = module_retrival(user_msg, self.logManager, self.chatbot, self.actionCore)
                self.mindMap.add_instance_memory(speaker='Agent', contents=response)
            
            elif action['action'] == 'answering':



        return agent_response
