from datetime import datetime, date 

__all__ = [
    'get_now_date_str',
    'get_now_datetime_str',
]


def get_now_date_str(format: str) -> str: 
    now = datetime.now()
    
    if format == '/':
        return now.strftime('%Y/%m/%d') 
    elif format == '-':
        return now.strftime('%Y-%m-%d')
    else:
        raise AssertionError  


def get_now_datetime_str(format: str) -> str: 
    now = datetime.now()
    
    if format == '/':
        return now.strftime('%Y/%m/%d %H:%M:%S') 
    elif format == '-':
        return now.strftime('%Y-%m-%d %H:%M:%S')
    else:
        raise AssertionError 
    