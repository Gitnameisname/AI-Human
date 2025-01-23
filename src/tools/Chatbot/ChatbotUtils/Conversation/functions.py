

def unwrap_codeblock(text: str) -> str:
    """
    Unwrap code block from text.
    """
    if text.startswith("```") and text.endswith("```"):
        return text[3:-3]
    return text