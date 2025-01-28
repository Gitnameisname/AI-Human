from src.tools.Chatbot.BasicModel.BasicModel import BasicModel

class chatGPT(BasicModel):
    def __init__(self, model_name='gpt-4o-mini', max_tokens=2048):
        super().__init__(model_name, max_tokens)