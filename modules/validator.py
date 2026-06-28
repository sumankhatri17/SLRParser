def validate_grammar_text(text: str):
    if not text or not text.strip():
        raise ValueError("Grammar cannot be empty.")
        
    lines = text.strip().split('\n')
    for line in lines:
        if line.strip() and '->' not in line:
            raise ValueError(f"Invalid syntax in line: '{line}'. Productions must contain '->'.")