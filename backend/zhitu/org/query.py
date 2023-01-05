from ..client import * 
from ..util import * 

__all__ = [
    'query_org_id_by_name', 
]


def query_org_id_by_name(org_name: str) -> set[int]:
    org_name = org_name.strip() 
    
    org_id_set = janusgraph_client.query_vertex_by_prop(
        label = LABEL_ORG, 
        prop_name = PROP_ORG_NAME, 
        prop_val = org_name, 
    )
    
    return org_id_set 
