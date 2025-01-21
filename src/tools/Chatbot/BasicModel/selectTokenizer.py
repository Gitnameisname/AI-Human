from transformers import AutoTokenizer
import tiktoken

def selectTokenizer(model_info):
    if model_info['model_name'] == 'mistral-nemo':
        return AutoTokenizer.from_pretrained(model_info['tokenizer'])
    
    else:
        return tiktoken.encoding_for_model(model_name=model_info['model_name'])

