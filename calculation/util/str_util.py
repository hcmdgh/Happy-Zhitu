from typing import Optional 

__all__ = [
    'normalize_str', 
]


def normalize_str(s: str) -> str: 
    out = str()
    
    for ch in s: 
        if ch.isalnum(): 
            out += ch.lower() 
        else:
            out += ' '
            
    out = ' '.join(out.split()) 
    
    return out 
