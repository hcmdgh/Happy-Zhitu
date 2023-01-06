from datetime import datetime

__all__ = [
    'get_now_datetime_str', 
]


def get_now_datetime_str() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
