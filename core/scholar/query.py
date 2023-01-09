from ..client import * 
from ..util import * 
from ..org import * 

from typing import Optional, Any 

__all__ = [
    'query_scholar_by_name_org', 
    'smart_query_scholar_id_by_name_org', 
    'query_scholar_by_id', 
]


def query_scholar_by_name_org(scholar_name: str,
                              scholar_org: str) -> list[dict[str, Any]]:
    mysql_client = get_mysql_client()
    
    table = mysql_client.get_table('dump', 'scholar_basic')
    
    entry_list = table.query_X_eq_x_and_Y_eq_y(
        X = 'name', 
        x = scholar_name.strip(),
        Y = 'org_name', 
        y = scholar_org.strip(),          
    )
    
    return entry_list


def smart_query_scholar_id_by_name_org(scholar_name: str,
                                       scholar_org: str) -> set[int]:
    mysql_client = get_mysql_client()
    mongo_client = get_mongo_client()
    table = mysql_client.get_table('dump', 'scholar_basic')
    collection = mongo_client.get_collection('zhitu', 'scholar_name_pinyin_map')
    
    scholar_name = scholar_name.strip()
    scholar_org = scholar_org.strip()
                                    
    org_set = smart_translate_org_name(scholar_org)
    
    name_set = {
        scholar_name, 
        normalize_str(scholar_name, keep_space=False), 
        convert_name_to_pinyin_1(scholar_name),
        convert_name_to_pinyin_2(scholar_name),
    }
    
    scholar_id_set: set[int] = set() 
    
    scholar_id_set.update(
        int(entry['id']) 
        for entry in table.query_X_in_x_and_Y_in_y('name', name_set, 'org_name', org_set)
    )
    
    scholar_id_set.update(
        int(entry['id']) 
        for entry in collection.query_X_in_x_and_Y_in_y('name_pinyin_list', name_set, 'norm_org', org_set)
    )
    
    return scholar_id_set


def query_scholar_by_id(scholar_id: int) -> Optional[dict[str, Any]]:
    mysql_client = get_mysql_client()
    
    table = mysql_client.get_table('dump', 'scholar_basic')
    
    entry = table.query_by_id(id=scholar_id)
    
    return entry 
