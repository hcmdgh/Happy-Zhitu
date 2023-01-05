from ..client import * 
from ..util import * 

__all__ = [
    'query_field_id_by_name', 
]


def query_field_id_by_name(field_name: str) -> set[int]:
    janusgraph_client = get_janusgraph_client()
    
    field_name = field_name.strip() 
    
    field_id_set: set[int] = set() 
    
    field_id_set.update(
        janusgraph_client.query_vertex_by_prop(
            label = LABEL_FIELD, 
            prop_name = PROP_FIELD_NAME, 
            prop_val = field_name, 
        )
    )
    
    field_id_set.update(
        janusgraph_client.query_vertex_by_prop(
            label = LABEL_FIELD, 
            prop_name = PROP_FIELD_NAME, 
            prop_val = field_name.capitalize(), 
        )
    )
    
    return field_id_set 
