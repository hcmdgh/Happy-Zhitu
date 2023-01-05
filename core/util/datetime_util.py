from datetime import datetime, date 

__all__ = [
    'get_now_date_str',
    'get_now_datetime_str',
]


def get_now_date_str() -> str: 
    now = datetime.now()
    return now.strftime('%Y/%m/%d') 


def get_now_datetime_str() -> str: 
    now = datetime.now()
    return now.strftime('%Y/%m/%d %H:%M:%S')
