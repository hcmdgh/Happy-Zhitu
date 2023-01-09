from ..util import * 
from ..client import * 

from typing import Any, Optional, Literal 

__all__ = [
    'query_scholar_patent'
] 


def query_scholar_patent(scholar_id: int,
                         source: str = 'ES') -> list[dict[str, Any]]:
    janusgraph_client = get_janusgraph_client()
    es_client = get_es_client()
    
    if source == 'ES':
        index = es_client.get_index('patent_v10', 'patent_v10')

        patent_list = index.query_X_eq_x(
            X = 'scholars.scholarId', 
            x = scholar_id, 
        ) 
        
        return patent_list
    
    elif source == 'JanusGraph':
        patent_id_set = janusgraph_client.query_vertex_neighbor(
            vid = scholar_id, 
            in_or_out = False, 
            v_label = LABEL_PATENT, 
        )
        
        patent_list = [
            janusgraph_client.query_vertex_by_vid(
                vid = patent_id, 
                with_vid_and_label = True, 
            )
            for patent_id in patent_id_set 
        ]
        
        return patent_list 
        
    else:
        raise AssertionError 
