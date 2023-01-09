from .query import * 
from ..util import * 
from ..client import * 

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
        return dict(
            error = dict(
                type = '学者信息缺少姓名或机构', 
                detail = scholar_entry, 
            ), 
            scholar_id = None, 
            exist = None,
            create = False,
            update = False,  
        )    
    
    if check_exist:
        exist_scholar_ids = smart_query_scholar_id_by_name_org(
            scholar_name = scholar_name, 
            scholar_org = scholar_org, 
        )
        
        if exist_scholar_ids:
            exist_scholar_id = exist_scholar_ids.pop()
            
            return dict(
                error = None, 
                scholar_id = exist_scholar_id, 
                exist = True, 
                create = False, 
                update = False, 
            )
            
    janusgraph_client = get_janusgraph_client()
    mysql_client = get_mysql_client()
        
    scholar_id = janusgraph_client.create_vertex(
        v_label = LABEL_SCHOLAR,
        prop_dict = {
            PROP_NAME: scholar_name, 
            PROP_ORG: scholar_org,
        },
    )
    
    table = mysql_client.get_table('dump', 'scholar_basic')

    scholar_entry['id'] = scholar_id
    
    table.insert_one(scholar_entry)
    
    return dict(
        error = None, 
        scholar_id = scholar_id, 
        exist = False, 
        create = True, 
        update = True, 
    )
