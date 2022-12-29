__all__ = [
    'normalize_str', 
]


def normalize_str(s: str) -> str:
    out_str = str()  
    
    for ch in s:
        if ch.isalnum():
            out_str += ch.lower() 
        else:
            out_str += ' '
            
    out_str = ' '.join(out_str.split())  
    
    return out_str
