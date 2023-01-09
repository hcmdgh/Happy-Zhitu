import json 
from typing import Optional, Any 

__all__ = [
    'json_dump', 
]


def jsonify(obj: Any) -> Any: 
    if obj is None or isinstance(obj, (int, float, bool, str, tuple)):
        return obj 
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = jsonify(v)
        return obj 
    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = jsonify(v)
        return obj 
    else:
        return str(obj) 


def json_dump(obj: Any,
              indent: Optional[int] = None) -> str:
    obj = jsonify(obj)
    
    json_str = json.dumps(obj, indent=indent, ensure_ascii=False).strip() 
    
    return json_str 
