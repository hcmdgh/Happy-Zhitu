from typing import Optional 

__all__ = [
    'normalize_str', 
]


def normalize_str(s: str,
                  keep_space: bool) -> str: 
    out = str()
    
    for ch in s: 
        if ch.isalnum(): 
            out += ch.lower() 
        else:
            out += ' '

    if keep_space:        
        out = ' '.join(out.split()) 
    else:
        out = ''.join(out.split()) 
    
    return out 
