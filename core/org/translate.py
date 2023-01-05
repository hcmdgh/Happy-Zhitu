from ..util import * 

import json 

__all__ = [
    'smart_translate_org_name',     
]

org_name_map: dict[str, str] = dict()


def init():
    if not org_name_map:
        print("Loading affiliation_name_translation.json...")
        
        with open('/mnt/GengHao/MAG/zhitu/affiliation_name_translation.json', 'r', encoding='utf-8') as fp:
            for line in fp: 
                entry = json.loads(line)
                org_name = entry['affiliation_name']
                org_zh_name = entry['affiliation_zh_name']
                org_name = normalize_str(org_name, keep_space=False)
                org_zh_name = normalize_str(org_zh_name, keep_space=False)
                
                org_name_map[org_name] = org_zh_name 
                org_name_map[org_zh_name] = org_name 

        assert org_name_map 
        
        print("Loading Completed!")
    

def smart_translate_org_name(org_name: str) -> set[str]:
    init()
    
    candidate_org_name_set: set[str] = set() 
    
    org_name = org_name.strip() 
    candidate_org_name_set.add(org_name)
    candidate_org_name_set.update(
        _org_name.strip() for _org_name in org_name.split(',')
    )
    
    for _org_name in list(candidate_org_name_set):
        candidate_org_name_set.add(
            normalize_str(_org_name, keep_space=False)
        )
    
    for _org_name in list(candidate_org_name_set):
        if org_name_map.get(_org_name):
            candidate_org_name_set.add(org_name_map[_org_name])
            
    return candidate_org_name_set 
