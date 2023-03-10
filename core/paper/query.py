from ..util import * 
from ..client import * 

from typing import Any, Optional, Literal  

__all__ = [
    'query_paper_id_by_title', 
    'query_paper_by_title', 
    'query_scholar_paper', 
    'query_scholar_paper_id', 
]


def query_paper_id_by_title(title: str,
                            source: str = 'JanusGraph') -> set[int]:
    janusgraph_client = get_janusgraph_client()
    es_client = get_es_client()

    title = title.strip() 
    
    if source == 'JanusGraph': 
        paper_id_set: set[int] = set()

        paper_id_set.update(
            janusgraph_client.query_vertex_by_prop(
                label = LABEL_PAPER, 
                prop_name = PROP_TITLE_LOWERCASE, 
                prop_val = title, 
            )
        )
        
        paper_id_set.update(
            janusgraph_client.query_vertex_by_prop(
                label = LABEL_PAPER, 
                prop_name = PROP_TITLE_LOWERCASE, 
                prop_val = normalize_str(title, keep_space=True), 
            )
        )
        
        return paper_id_set
    
    else:
        raise AssertionError


def query_paper_by_title(title: str,
                         source: str = 'ES') -> list[dict[str, Any]]:
    janusgraph_client = get_janusgraph_client()
    es_client = get_es_client()
    
    title = title.strip() 
                         
    if source == 'ES':
        index = es_client.get_index('paper_v10', 'paper_v10')

        paper_map: dict[str, dict[str, Any]] = dict() 

        for paper_entry in index.query_X_eq_x(X='title', x=title):
            paper_map[paper_entry['_id']] = paper_entry
            
        for paper_entry in index.query_X_eq_x(X='titleLowercase', x=normalize_str(title)):
            paper_map[paper_entry['_id']] = paper_entry

        return list(paper_map.values())
    
    elif source == 'JanusGraph':
        paper_id_set = query_paper_id_by_title(title)
        
        paper_list = [
            janusgraph_client.query_vertex_by_vid(
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
    janusgraph_client = get_janusgraph_client()
    es_client = get_es_client()
    
    if source == 'ES':
        index = es_client.get_index('paper_v10', 'paper_v10')

        paper_list = index.query_X_eq_x(
            X = 'scholars.scholarId', 
            x = scholar_id, 
        ) 
        
        return paper_list
    
    elif source == 'JanusGraph':
        paper_id_set = janusgraph_client.query_vertex_neighbor(
            vid = scholar_id, 
            in_or_out = False, 
            v_label = LABEL_PAPER, 
        )
        
        paper_list = [
            janusgraph_client.query_vertex_by_vid(
                vid = paper_id, 
                with_vid_and_label = True, 
            )
            for paper_id in paper_id_set 
        ]
        
        return paper_list 
        
    else:
        raise AssertionError 


def query_scholar_paper_id(scholar_id: int) -> set[int]:
    janusgraph_client = get_janusgraph_client()

    paper_id_set = janusgraph_client.query_vertex_neighbor(
        vid = scholar_id, 
        in_or_out = False, 
        v_label = LABEL_PAPER, 
    )
    
    return paper_id_set 
