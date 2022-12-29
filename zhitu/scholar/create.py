from ..connection import * 
from .query import * 
from ..constant import * 

from typing import Optional, Any 

__all__ = [
    'create_scholar', 
]


def create_scholar(scholar_entry: dict[str, Any],
                   check_exist: bool = True) -> dict[str, Any]:
    try:
        assert 'id' not in scholar_entry 
        scholar_name = scholar_entry['name'] = scholar_entry['name'].strip() 
        scholar_org = scholar_entry['org_name'] = scholar_entry['org_name'].strip() 
    except Exception:
        print(f"[ERROR] 学者信息缺少姓名或机构：{scholar_entry}")
        
        return dict(
            error = '学者信息缺少姓名或机构', 
            exist = None, 
            scholar_id = None, 
        )    
    
    if check_exist:
        exist_scholar_list = query_scholar_by_name_org(
            scholar_name = scholar_name, 
            scholar_org = scholar_org, 
        )
        
        if exist_scholar_list:
            exist_scholar_id = exist_scholar_list[0]['id']
            
            print(f"[INFO] 学者已存在：{exist_scholar_id} {scholar_name} {scholar_org}")
            
            return dict(
                error = None, 
                exist = True, 
                scholar_id = exist_scholar_id, 
            )
        
    client = get_or_create_janusgraph_connection()
        
    scholar_id = client.create_vertex(
        v_label = LABEL_SCHOLAR,
        prop_dict = {
            PROP_NAME: scholar_name, 
            PROP_ORG: scholar_org,
        },
    )
    
    client = get_or_create_mysql_connection()
    table = client.get_table('dump', 'scholar_basic')

    scholar_entry['id'] = scholar_id
    
    table.insert_one(scholar_entry)
    
    return dict(
        error = None, 
        exist = False, 
        scholar_id = scholar_id, 
    )
