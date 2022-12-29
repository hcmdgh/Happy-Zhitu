from ..connection import * 
from ..util import * 
from ..constant import * 

from typing import Any, Optional, Literal  

__all__ = [
    'query_paper_by_title', 
    'query_scholar_paper', 
]


def query_paper_by_title(title: str,
                         source: str = 'ES') -> list[dict[str, Any]]:
    title = title.strip() 
                         
    if source == 'ES':
        client = get_or_create_es_connection() 
        index = client.get_index('paper_v10', 'paper_v10')

        paper_map: dict[str, dict[str, Any]] = dict() 

        for paper_entry in index.query_X_eq_x(X='title', x=title):
            paper_map[paper_entry['_id']] = paper_entry
            
        for paper_entry in index.query_X_eq_x(X='titleLowercase', x=normalize_str(title)):
            paper_map[paper_entry['_id']] = paper_entry

        return list(paper_map.values())
    
    elif source == 'JanusGraph':
        client = get_or_create_janusgraph_connection()

        paper_id_set: set[int] = set()

        paper_id_set.update(
            client.query_vertex_by_prop(
                label = LABEL_PAPER, 
                prop_name = PROP_TITLE_LOWERCASE, 
                prop_val = title, 
            )
        )
        
        paper_id_set.update(
            client.query_vertex_by_prop(
                label = LABEL_PAPER, 
                prop_name = PROP_TITLE_LOWERCASE, 
                prop_val = normalize_str(title), 
            )
        )
        
        paper_list = [
            client.query_vertex_by_vid(
                vid = paper_id, 
                with_vid_and_label = True, 
            )
            for paper_id in paper_id_set 
        ]
        
        return paper_list 
    
    else:
        raise AssertionError 


def query_scholar_paper(scholar_id: int,
                        source: str = 'ES') -> list[dict[str, Any]]:
    if source == 'ES':
        client = get_or_create_es_connection() 
        index = client.get_index('paper_v10', 'paper_v10')

        paper_list = index.query_X_eq_x(
            X = 'scholars.scholarId', 
            x = scholar_id, 
        ) 
        
        return paper_list
    
    elif source == 'JanusGraph':
        client = get_or_create_janusgraph_connection()

        paper_id_set = client.query_vertex_neighbor(
            vid = scholar_id, 
            in_or_out = False, 
            v_label = LABEL_PAPER, 
        )
        
        paper_list = [
            client.query_vertex_by_vid(
                vid = paper_id, 
                with_vid_and_label = True, 
            )
            for paper_id in paper_id_set 
        ]
        
        return paper_list 
        
    else:
        raise AssertionError 
