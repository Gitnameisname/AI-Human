import os
import json
import subprocess

from MindMap.LogManager import LogManager
from MindMap.MindMap import MindMap
from ActionCore.ActionCore import ActionCore
from src.tools.Chatbot.OpenAI.chatGPT import chatGPT
from src.tools.Chatbot.ChatbotUtils.SystemContexts import math_solving_problem_system_context, math_system_context
from src.tools.Chatbot.ChatbotUtils.Conversation import JSON_PROMPT_EXTENSION, unwrap_codeblock
from src.constants import CODING_PLAYGROUND

class Math:
    def __init__(self, logManager: LogManager, mindMap: MindMap):
        self.logManager = logManager
        self.mindMap = mindMap
        self.actionCore = ActionCore(logManager)
        self.chatbot = chatGPT(model_name="gpt-4o-mini", max_tokens=2048)
        self.logManager.log_info(f"(Math) Load: OK")

        # 단계별 수학 연산 결과를 저장하는 리스트입니다.
        self.mathMemory = []

    # 가장 상위에서 실행되는 함수입니다.
    # 외부에서는 이 함수를 불러, 수학 문제를 풀도록 합니다.
    def solver(self, problems: str):
        """
        수학 문제를 풀 때 실행되는 가장 상위 함수입니다.
        외부에서는 이 함수를 불러 수학 문제를 풀도록 합니다.

        Args:
            problems (str): 수학 문제

        Returns:
            self.mathMemory (list): 수학 문제의 풀이 단계와 결과
        """
        # self.mathMemory = self.mindMap.add_instance_memory(memory = self.mathMemory, actor='User', action='request', request=problems, result='')
        solving_steps = self.generate_solving_steps(problems)
        
        for step in solving_steps:
            self.logManager.log_info(f"(Math) Step: {step}")
            self.logManager.log_info(f"(Math) mathMemory:\n{self.mathMemory}")
            code_info = self.generate_script(step)
            result = self.execute_script(code_info)
            self.mathMemory = self.mindMap.add_instance_memory(memory = self.mathMemory, actor='mathematician', action='solve a math problem', request=step, result=result)

        return self.mathMemory

    def generate_solving_steps(self, problems: str):
        """
        수학 문제를 풀기 위해 수학 문제의 풀이 단계를 생성합니다.

        Args:
            problems (str): 수학 문제

        Returns:
            solving_steps (list): 수학 문제의 풀이 단계
        """
        self.logManager.log_info(f"(Math) Generate Codes")
        system_context = math_solving_problem_system_context()
        solving_steps = self.chatbot.chat(user_msg=problems, system_context=system_context)
        self.logManager.log_info(f"(Math) Solving Steps:\n{solving_steps}")
        solving_steps = unwrap_codeblock(solving_steps)
        self.logManager.log_info(f"(Math) Unwrapped Solving Steps:\n{solving_steps}")
        try:
            solving_steps = json.loads(solving_steps.replace("'", "\""))
            self.logManager.log_info(f"(Math) Coding Jobs:\n{solving_steps}")
        except Exception as e:
            self.logManager.log_error(f"(Math) List Error:\n{solving_steps}")
            raise ValueError(f"(Math) Generate Jobs: Invalid Jobs\nType of solving_steps: {type(solving_steps)}\nsolving_steps: {solving_steps}")

        if type(solving_steps) is not list:
            raise ValueError(f"(Math) Generate Jobs: Invalid Jobs\nType of solving_steps: {type(solving_steps)}\nsolving_steps: {solving_steps}")
        
        return solving_steps

    def generate_script(self, step):
        """
        수학 문제 풀이 단계를 실행 가능한 스크립트로 변환합니다.

        Args:
            step (str): 수학 문제의 풀이 단계에 대한 설명

        Returns:
            code_info (dict): 스크립트 정보
        """
        self.logManager.log_info(f"(Math) Generate Script")
        self.logManager.log_info(f"(Math) Step: {step}")
        descriptions = json.dumps({
            "solution_record": self.mathMemory,
            "present_step": step
        }, indent=4)
        code_info = self.chatbot.chat(user_msg=descriptions, system_context=math_system_context(), prompt_extention=JSON_PROMPT_EXTENSION)

        # code_info에서 코드 블록이 있다면 제거하고, JSON 형식으로 변환합니다.
        code_info = unwrap_codeblock(code_info)

        try:
            code_info = json.loads(code_info)
            if type(code_info) is list:
                code_info = code_info[0]
            self.logManager.log_info(f"(Math) Code Info:\n{code_info}")
        except Exception as e:
            self.logManager.log_error(f"(Math) Generate Script: Invalid Script\ntype: {type(code_info)}\ncode_info: {code_info}")
            raise ValueError(f"(Math) Generate Script: Invalid Script")

        # 스크립트를 파일로 저장합니다.
        with open(f"{CODING_PLAYGROUND}/{code_info['file_name']}", "w", encoding="utf-8") as f:
            f.write(code_info['script'])

        self.logManager.log_info(f"(Math) Generate Script: OK")

        return code_info

    def execute_script(self, code_info):
        script_path = f"{CODING_PLAYGROUND}/{code_info['file_name']}"
        try:            
            if os.name == 'posix':
                exec_list = ["python3", script_path]
            elif os.name == 'nt':
                exec_list = ["python", script_path]
            else:
                raise EnvironmentError("Unsupported operating system")
            
            result = subprocess.run(exec_list, capture_output=True, text=True)

            if result.returncode == 0:
                self.logManager.log_info(f"(Math) execute_script: OK")
                self.logManager.log_info(f"(Math) execution results: {result.stdout}")
                return result.stdout.strip()
            else:
                self.logManager.log_error(f"(Math) execute_script: {result.stderr}")
                return result.stderr
                   
        except Exception as e:
            self.logManager.log_error(f"(Math) execute_script - 스크립트 실행 중 오류가 발생하였습니다:\n{e}")
            raise

        finally:
            if os.path.exists(script_path):
                os.remove(script_path)
