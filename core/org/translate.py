from ..util import * 

import json 
from typing import Optional, Any 

__all__ = [
    'smart_translate_org_name',  
    'translate_org_name_to_zh',    
]

org_name_translation_map: dict[str, dict[str, Any]] = dict()


def init():
    if not org_name_translation_map:
        print("Loading affiliation_name_translation.json...")
        
        with open('/MAG/json/affiliation_name_translation.json', 'r', encoding='utf-8') as fp:
            for line in fp: 
                entry = json.loads(line)
                norm_org_name = normalize_str(entry['affiliation_name'], keep_space=False)
                norm_org_zh_name = normalize_str(entry['affiliation_zh_name'], keep_space=False)
                
                org_name_translation_map[norm_org_name] = entry  
                org_name_translation_map[norm_org_zh_name] = entry  

        assert org_name_translation_map
        
        print("Loading Completed!")
    

def smart_translate_org_name(org_name: str) -> set[str]:
    init()
    org_name = org_name.strip() 
    
    candidate_org_name_set = {
        org_name,
        *[ item.strip() for item in org_name.split(',') ],
    } 
    
    for item in list(candidate_org_name_set):
        candidate_org_name_set.add(
            normalize_str(item, keep_space=False)
        )
    
    for item in list(candidate_org_name_set):
        translation_entry = org_name_translation_map.get(item)
        
        if translation_entry:
            candidate_org_name_set.add(translation_entry['affiliation_name'])
            candidate_org_name_set.add(translation_entry['affiliation_zh_name'])
            candidate_org_name_set.add(normalize_str(translation_entry['affiliation_name'], keep_space=False))
            candidate_org_name_set.add(normalize_str(translation_entry['affiliation_zh_name'], keep_space=False))
            
    return candidate_org_name_set 


def translate_org_name_to_zh(org_name: str) -> str:
    init()
    
    org_name = org_name.strip() 
    
    norm_org_name = normalize_str(org_name, keep_space=False) 
    
    translation_entry = org_name_translation_map.get(norm_org_name)
        
    if translation_entry:
        return translation_entry['affiliation_zh_name'] 
    else:
        return org_name 
