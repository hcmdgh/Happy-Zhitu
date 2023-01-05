from typing import Optional, Any 

__all__ = [
    'parse_str',
    'parse_int',
    'parse_float',
]


def parse_str(s: str) -> Optional[str]:
    s = s.strip() 
    
    if s: 
        return s 
    else:
        return None 
    
    
def parse_int(s: str) -> Optional[int]:
    s = s.strip() 
    
    if s: 
        return int(s)  
    else:
        return None 
    
    
def parse_float(s: str) -> Optional[float]:
    s = s.strip() 
    
    if s: 
        return float(s)  
    else:
        return None 
