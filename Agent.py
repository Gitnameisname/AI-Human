from src.models.MistralNemo import MistralNemo

class ChatBot:
    def __init__(self, logManager, stream=True):
        self.logManager = logManager
        self.mistralNemo = MistralNemo()


    def chat(self, user_msg):
        self.logManager.log_info(f"User: {user_msg}")
        agent_response = self.mistralNemo.chat(user_msg)
        self.logManager.log_info(f"Model: {agent_response}")

        return agent_response
    
    def stream_chat(self, user_msg):
        self.logManager.log_info(f"User: {user_msg}")
        for agent_response in self.mistralNemo.stream_chat(user_msg):
            print(f"agent_response: {agent_response}")
            yield agent_response
        # self.logManager.log_info(f"Model: {agent_response}")