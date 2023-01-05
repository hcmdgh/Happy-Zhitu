import json 

__all__ = [
    'smart_translate_org_name',     
]

org_name_map: dict[str, str] = dict()


def init():
    print("Loading affiliation_name_translation.json...")
    
    with open('/mnt/GengHao/MAG/zhitu/affiliation_name_translation.json', 'r', encoding='utf-8') as fp:
        for line in fp: 
            entry = json.loads(line)
            org_name = entry['affiliation_name']
            org_zh_name = entry['affiliation_zh_name']
            
            org_name_map[org_name] = org_zh_name 
            org_name_map[org_zh_name] = org_name 
    
    print("Loading Completed!")


init()


def smart_translate_org_name(org_name: str) -> set[str]:
    candidate_org_name_set: set[str] = set() 
    
    candidate_org_name_set.add(org_name.strip())
    candidate_org_name_set.update(
        _org_name.strip() for _org_name in org_name.split(',')
    )
    
    for _org_name in list(candidate_org_name_set):
        if org_name_map.get(_org_name):
            candidate_org_name_set.add(org_name_map[_org_name])
            
    return candidate_org_name_set 
