from MindMap.LogManager import LogManager
from src.tools.Chatbot.BasicModel.BasicModel import BasicModel
from src.tools.Chatbot.ChatbotUtils.SystemContexts import coding_system_context

def coding(request: str, logManager: LogManager, chatbot: BasicModel):
    system_context = coding_system_context(request=request)
    codes = chatbot.chat(user_msg="Codes: ", system_context=system_context)
    logManager.log_info(f"(Coding) Codes:\n{codes}")

    return codes