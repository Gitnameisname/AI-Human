from transformers import AutoTokenizer
import tiktoken

def selectTokenizer(model_info):
    if model_info['model_name'] == 'mistral-nemo':
        return AutoTokenizer.from_pretrained(model_info['tokenizer'])
    
    elif model_info['model_name'] in ['gpt-4o-mini', 'gpt-4o', 'o1', 'gpt-4o-mini']:
        return tiktoken.encoding_for_model(model_name='gpt-4o-mini')

