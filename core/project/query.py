from ..util import * 
from ..client import * 

from typing import Any, Optional, Literal 

__all__ = [
    'query_scholar_project'
] 


def query_scholar_project(scholar_id: int,
                          source: str = 'ES') -> list[dict[str, Any]]:
    janusgraph_client = get_janusgraph_client()
    es_client = get_es_client()
    
    if source == 'ES':
        index = es_client.get_index('project_v10', 'project_v10')

        project_list = index.query_X_eq_x(
            X = 'scholars.scholarId', 
            x = scholar_id, 
        ) 
        
        return project_list
    
    elif source == 'JanusGraph':
        project_id_set = janusgraph_client.query_vertex_neighbor(
            vid = scholar_id, 
            in_or_out = False, 
            v_label = LABEL_PROJECT, 
        )
        
        project_list = [
            janusgraph_client.query_vertex_by_vid(
                vid = project_id, 
                with_vid_and_label = True, 
            )
            for project_id in project_id_set 
        ]
        
        return project_list 
        
    else:
        raise AssertionError 
