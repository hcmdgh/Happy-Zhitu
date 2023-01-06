from ..util import * 

import json 
from typing import Optional, Any 

__all__ = [
    'translate_field_name_to_zh',    
]

field_name_translation_map: dict[str, str] = dict()


def init():
    if not field_name_translation_map:
        print("Loading field_name_translation_L012.json...")
        
        with open('/MAG/json/field_name_translation_L012.json', 'r', encoding='utf-8') as fp:
            for line in fp: 
                entry = json.loads(line)
                norm_field_name = normalize_str(entry['field_name'], keep_space=False)
                field_zh_name = entry['field_zh_name'].strip() 
                
                field_name_translation_map[norm_field_name] = field_zh_name  

        assert field_name_translation_map
        
        print("Loading Completed!")
    

def translate_field_name_to_zh(field_name: str) -> str:
    init()
    
    field_name = field_name.strip() 
    
    norm_field_name = normalize_str(field_name, keep_space=False) 
    
    field_zh_name = field_name_translation_map.get(norm_field_name)
        
    if field_zh_name:
        return field_zh_name 
    else:
        return field_name 
