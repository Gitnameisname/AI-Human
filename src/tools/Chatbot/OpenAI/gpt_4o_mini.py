from src.tools.Chatbot.BasicModel.BasicModel import BasicModel

class gpt_4o_mini(BasicModel):
    def __init__(self, model_name='gpt-4o-mini', max_tokens=1024):
        super().__init__(model_name, max_tokens)