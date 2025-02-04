from MindMap.LogManager import LogManager
from src.tools.Chatbot.BasicModel.BasicModel import BasicModel
from src.tools.Chatbot.ChatbotUtils.SystemContexts import conclusion_system_context

def make_conclusion(user_msg: str, memory: list, logManager: LogManager, chatbot: BasicModel):
    logManager.log_info(f"(Conclusion) Memory: {memory}")
    system_context = conclusion_system_context(user_msg, thougths=memory)

    conclusion = chatbot.chat(user_msg="Conclusion: ", system_context=system_context)
    logManager.log_info(f"(Conclusion) conclusion: {conclusion}")

    return conclusion