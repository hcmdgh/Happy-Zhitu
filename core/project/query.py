from ..util import * 
from ..client import * 

from typing import Any, Optional, Literal 

__all__ = [
    'query_scholar_project',
    'query_project_id_by_title', 
    'query_project_by_title', 
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


def query_project_id_by_title(title: str,
                              source: str = 'JanusGraph') -> set[int]:
    janusgraph_client = get_janusgraph_client()

    title = title.strip() 
    
    if source == 'JanusGraph': 
        project_id_set: set[int] = set()

        project_id_set.update(
            janusgraph_client.query_vertex_by_prop(
                label = LABEL_PROJECT, 
                prop_name = PROP_PROJECT_TITLE, 
                prop_val = title, 
            )
        )
        
        return project_id_set
    
    else:
        raise AssertionError


def query_project_by_title(title: str,
                           source: str = 'JanusGraph') -> list[dict[str, Any]]:
    janusgraph_client = get_janusgraph_client()
    es_client = get_es_client()
    
    title = title.strip() 
                         
    if source == 'ES':
        index = es_client.get_index('project_v10', 'project_v10')

        paper_map: dict[str, dict[str, Any]] = dict() 

        for paper_entry in index.query_X_eq_x(X='title', x=title):
            paper_map[paper_entry['_id']] = paper_entry
            
        for paper_entry in index.query_X_eq_x(X='titleLowercase', x=normalize_str(title)):
            paper_map[paper_entry['_id']] = paper_entry

        return list(paper_map.values())
    
    elif source == 'JanusGraph':
        project_id_set = query_project_id_by_title(title)
        
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
