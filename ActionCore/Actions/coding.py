import os
import json
import subprocess

from MindMap.LogManager import LogManager
from MindMap.MindMap import MindMap
from src.Actions import *
from src.Systems.ActionCore import ActionCore
from src.tools.Chatbot.OpenAI.chatGPT import chatGPT
from src.tools.Chatbot.ChatbotUtils.SystemContexts import coding_system_context
from src.tools.Chatbot.ChatbotUtils.Conversation import JSON_PROMPT_EXTENSION, unwrap_codeblock
from src.constants import CODING_PLAYGROUND

class Coder:
    def __init__(self, logManager: LogManager, mindMap: MindMap):
        self.logManager = logManager
        self.mindMap = mindMap
        self.actionCore = ActionCore(logManager)
        self.chatbot = chatGPT(model_name="gpt-4o-mini", max_tokens=2048)
        self.logManager.log_info(f"(Coder) Load: OK")

    def execute_codes(self, requests: str):
        jobs = self.generate_jobs(requests)
        for code in jobs:
            self.generate_script(code)
            result = self.execute_script(code)
            self.mindMap.add_sago_process_memory(action='coding', request=code['request'], result=result)

    def generate_jobs(self, request: str):
        self.logManager.log_info(f"(Coder) Generate Codes")
        system_context = coding_system_context(request=request)
        jobs = self.chatbot.chat(user_msg=request, system_context=system_context, prompt_extention=JSON_PROMPT_EXTENSION)
        jobs = unwrap_codeblock(jobs)
        try:
            jobs = json.loads(jobs)
            self.logManager.log_info(f"(Coder) Coding Jobs:\n{jobs}")
        except Exception as e:
            self.logManager.log_error(f"(Coder) JSON Error:\n{jobs}")
            raise ValueError(f"(Coder) Generate Jobs: Invalid Jobs\n{jobs}")

        if type(jobs) is not list:
            raise ValueError(f"(Coder) Generate Jobs: Invalid Jobs\n{jobs}")
        
        return jobs

    def generate_script(self, code):
        self.logManager.log_info(f"(Coder) Generate Script")
        with open(f"{CODING_PLAYGROUND}/{code['file_name']}", "w", encoding="utf-8") as f:
            f.write(code['script'])

        self.logManager.log_info(f"(Coder) Generate Script: OK")

    def execute_script(self, code):
        script_path = f"{CODING_PLAYGROUND}/{code['file_name']}"
        try:            
            if os.name == 'posix':
                exec_list = ["python3", script_path]
            elif os.name == 'nt':
                exec_list = ["python", script_path]
            else:
                raise EnvironmentError("Unsupported operating system")
            
            result = subprocess.run(exec_list, capture_output=True, text=True)

            if result.returncode == 0:
                self.logManager.log_info(f"(Coder) execute_script: OK")
                self.logManager.log_info(f"(Coder) execution results: {result.stdout}")
                return result.stdout.strip()
            else:
                self.logManager.log_error(f"(Coder) execute_script: {result.stderr}")
                return result.stderr
                   
        except Exception as e:
            self.logManager.log_error(f"(Coder) execute_script - 스크립트 실행 중 오류가 발생하였습니다:\n{e}")
            raise

        finally:
            if os.path.exists(script_path):
                os.remove(script_path)
