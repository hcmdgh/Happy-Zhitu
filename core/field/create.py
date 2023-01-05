from .query import * 
from ..client import * 
from ..util import * 

from typing import Optional, Any 

__all__ = [
    'create_field', 
]


def create_field(field_name: str, 
                 field_level: int,
                 check_exist: bool = True) -> dict[str, Any]:
    janusgraph_client = get_janusgraph_client()
    
    field_name = field_name.strip() 
                 
    if check_exist:
        exist_field_ids = query_field_id_by_name(field_name=field_name)

        if exist_field_ids:
            return dict(
                error = None, 
                field_id = exist_field_ids.pop(), 
                exist = True, 
                create = False, 
            )
        
    field_id = janusgraph_client.create_vertex(
        v_label = LABEL_FIELD, 
        prop_dict = {
            PROP_FIELD_NAME: field_name, 
            PROP_FIELD_LEVEL: field_level, 
        },
    )
    
    return dict(
        error = None, 
        field_id = field_id, 
        exist = False, 
        create = True, 
    )
