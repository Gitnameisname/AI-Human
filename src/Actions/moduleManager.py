from MindMap.LogManager import LogManager
from src.Systems.ActionCore import ActionCore
from src.tools.Chatbot.BasicModel.BasicModel import BasicModel
from src.tools.Chatbot.ChatbotUtils.SystemContexts import module_manager_system_context, function_manager_system_context
from src.tools.Chatbot.ChatbotUtils.Conversation.promptExtension import MODULE_PATH, FUNCTION_NAME

def module_retrival(user_msg, logManager: LogManager, chatbot: BasicModel, actionCore: ActionCore):
    logManager.log_info(f"(Module Manager) Module Retrieval")
    system_context = module_manager_system_context()
    module_name = chatbot.chat(user_msg=user_msg, system_context=system_context, prompt_extention=MODULE_PATH)
    
    functions = actionCore.listup_functions(module_name)
    system_context = function_manager_system_context(functions)
    function_name = chatbot.chat(user_msg=user_msg, system_context=system_context, prompt_extention=FUNCTION_NAME)
    logManager.log_info(f"(Module Manager) Function Name: {function_name}")
    function_result = actionCore.execute_function(module_name, function_name)
    logManager.log_info(f"(Module Manager) Function Result: {function_result}")

    return function_result