import json
from MindMap.LogManager import LogManager
from ActionCore.ActionCore import ActionCore
from src.tools.Chatbot.BasicModel.BasicModel import BasicModel
from src.tools.Chatbot.ChatbotUtils.SystemContexts import module_manager_system_context, function_manager_system_context
from src.tools.Chatbot.ChatbotUtils.Conversation.promptExtension import MODULE_PATH, JSON_PROMPT_EXTENSION

def use_module(user_msg, logManager: LogManager, chatbot: BasicModel, actionCore: ActionCore):
    logManager.log_info(f"(Module Manager) Module Retrieval")
    system_context = module_manager_system_context()
    module_name = chatbot.chat(user_msg=user_msg, system_context=system_context, prompt_extention=MODULE_PATH)

    if module_name == "None":
        return None
    
    functions = actionCore.listup_functions(module_name)
    system_context = function_manager_system_context(functions)
    function_info = chatbot.chat(user_msg=user_msg, system_context=system_context, prompt_extention=JSON_PROMPT_EXTENSION)
    function_info = json.loads(function_info)
    logManager.log_info(f"(Module Manager) Function Info: {function_info}")
    function_result = actionCore.execute_function(module_name, function_info)
    logManager.log_info(f"(Module Manager) Function Result: {function_result}")

    return function_result