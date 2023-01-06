from datetime import datetime

__all__ = [
    'now', 
]


def now() -> str:
    dt = datetime.now()
    s = dt.strftime('%Y/%m/%d %H:%M:%S')
    
    return s 
