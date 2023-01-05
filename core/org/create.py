from .query import * 
from ..client import * 
from ..util import * 

from typing import Optional, Any 

__all__ = [
    'create_org', 
]


def create_org(org_name: str, 
               check_exist: bool = True) -> dict[str, Any]:
    janusgraph_client = get_janusgraph_client()
    
    org_name = org_name.strip() 
                 
    if check_exist:
        exist_org_ids = query_org_id_by_name(org_name=org_name)

        if exist_org_ids:
            return dict(
                error = None, 
                org_id = exist_org_ids.pop(), 
                exist = True, 
                create = False, 
            )
        
    org_id = janusgraph_client.create_vertex(
        v_label = LABEL_ORG, 
        prop_dict = {
            PROP_ORG_NAME: org_name, 
        },
    )
    
    return dict(
        error = None, 
        org_id = org_id, 
        exist = False, 
        create = True, 
    )
