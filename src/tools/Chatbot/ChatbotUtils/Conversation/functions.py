import re

def unwrap_codeblock(text: str) -> str:
    """
    Unwrap code block and code type from text.
    """
    cleaned_text = re.sub(r'```[a-zA-Z]*\n(.*?)```', r"\1", text, flags=re.DOTALL)

    return cleaned_text.strip()

def unwrap_double_quote(text: str) -> str:
    """
    Unwrap double quote from text.
    """
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    return text