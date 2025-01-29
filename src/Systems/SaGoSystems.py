import json
from MindMap.LogManager import LogManager
from src.tools.Chatbot.OpenAI.chatGPT import chatGPT
from MindMap.MindMap import MindMap
from ActionCore.Actions import *
from src.tools.Chatbot.ChatbotUtils.SystemContexts import planning_system_context
from src.tools.Chatbot.ChatbotUtils.Conversation import JSON_PROMPT_EXTENSION, unwrap_codeblock

class SaGoSystems:
    def __init__(self, logManager: LogManager, mindMap: MindMap):
        self.logManager = logManager
        self.mindMap = mindMap
        self.actionCore = ActionCore(logManager)
        self.coder = Coder(logManager=self.logManager, mindMap=self.mindMap)
        self.math = Math(logManager=self.logManager, mindMap=self.mindMap)
        self.chatbot = chatGPT(model_name="gpt-4o-mini", max_tokens=2048)
        self.logManager.log_info(f"(SaGoSystems) Load: OK")

    def SaGoProcess(self, user_msg, plan):
        self.logManager.log_info(f"(SaGoSystems) SaGoProcess")

        self.mindMap.initialize_sago_process_memory()
        # self.mindMap.add_sago_process_memory(action='listening', request=user_msg, result="")

        for action in plan:
            if action['action'] == 'use_module':
                response = use_module(user_msg, self.logManager, self.chatbot, self.actionCore)
                self.mindMap.add_sago_process_memory(action='use_module', request=action['description'], result=response)
            
            elif action['action'] == 'make_conclusion':
                conclusion = make_conclusion(self.mindMap.sago_process_memory, self.logManager, self.chatbot)
                self.logManager.log_info(f"(SaGoSystems) SaGoProcess: Conclusion\nconclusion: {conclusion}")
                self.mindMap.initialize_sago_process_memory()
                self.mindMap.add_td_memory(category="Thought", speaker="Model", contents=conclusion)

                return conclusion
            
            elif action['action'] == 'coding':
                self.coder.execute_codes(requests=action['description'])

            elif action['action'] == 'math':
                math_memory = self.math.solver(problems=user_msg)
                self.mindMap.sago_process_memory += math_memory

            else:
                self.logManager.log_error(f"(SaGoSystems) SaGoProcess: Invalid Action\naction: {action['action']}")
                raise ValueError(f"(SaGoSystems) SaGoProcess: Invalid Action\naction: {action['action']}")

    def planning(self, user_msg):
        self.logManager.log_info(f"(SaGoSystems) Planning")
        system_context = planning_system_context()
        agent_response = self.chatbot.chat(user_msg=user_msg, system_context=system_context, prompt_extention=JSON_PROMPT_EXTENSION)
        agent_response = unwrap_codeblock(agent_response)
        try:
            plan = json.loads(agent_response)
        except json.JSONDecodeError:
            self.logManager.log_error(f"(SaGoSystems) Planning: JSON Decode Error\nresponse: {agent_response}")
            raise ValueError(f"(SaGoSystems) Planning: JSON Decode Error\nresponse: {agent_response}")
        plan = self.check_plan(plan)

        return plan
    
    def check_plan(self, plan: list):
        self.logManager.log_info(f"(SaGoSystems) Check Plan")
        self.logManager.log_info(f"(SaGoSystems) Plan before:\n{plan}")
        if len(plan) == 0:
            self.logManager.log_error(f"(SaGoSystems) Check Plan: Empty Plan")
            plan.append({'action': 'answering', 'description': '사용자의 질문에 대해 답변합니다.'})

        elif len(plan) == 1:
            if plan[-1]['action'] == 'answering':
                self.logManager.log_info(f"(SaGoSystems) Check Plan: Answering")
            else:
                self.logManager.log_info(f"(SaGoSystems) Check Plan: Not Answering")
                plan.append({'action': 'answering', 'description': '사용자의 질문에 대해 답변합니다.'})
        else:
            if plan[-1]['action'] != 'answering' and plan[-2]['action'] == 'make_conclusion':
                plan.append({'action': 'answering', 'description': '사용자의 질문에 대해 답변합니다.'})
            elif plan[-1]['action'] != 'answering' and plan[-2]['action'] != 'make_conclusion':
                plan.append({'action': 'make_conclusion', 'description': '주어진 정보를 바탕으로 결론을 도출합니다.'})
                plan.append({'action': 'answering', 'description': '사용자의 질문에 대해 답변합니다.'})
            elif plan[-1]['action'] == 'answering' and plan[-2]['action'] != 'make_conclusion':
                plan.insert(-1, {'action': 'make_conclusion', 'description': '주어진 정보를 바탕으로 결론을 도출합니다.'})

        # 마지막으로 한번 더 확인
        if plan[-1]['action'] != 'answering':
            self.logManager.log_error(f"(SaGoSystems) Check Plan: Invalid Plan\nplan: {plan}")
            raise ValueError(f"(SaGoSystems) Check Plan: Invalid Plan\nplan: {plan}")

        self.logManager.log_info(f"(SaGoSystems) Plan after:\n{plan}")
        return plan
