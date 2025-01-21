from src.tools.Chatbot.BasicModel.BasicModel import BasicModel

from openai import OpenAI

class MistralNemo(BasicModel):
    def __init__(self, model_name="mistral-nemo", max_tokens=1024):
        super.__init__(model_name, max_tokens)

        self.client = OpenAI(
                        base_url = self.model_info['base_url'],
                        api_key="EMPTY"
        )