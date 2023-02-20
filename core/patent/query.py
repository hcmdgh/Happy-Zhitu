from ..util import * 
from ..client import * 

from typing import Any, Optional, Literal 

__all__ = [
    'query_scholar_patent',
    'query_patent_id_by_title', 
    'query_patent_by_title', 
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
    
    
def query_patent_id_by_title(title: str,
                             source: str = 'JanusGraph') -> set[int]:
    janusgraph_client = get_janusgraph_client()

    title = title.strip() 
    
    if source == 'JanusGraph': 
        patent_id_set: set[int] = set()

        patent_id_set.update(
            janusgraph_client.query_vertex_by_prop(
                label = LABEL_PATENT, 
                prop_name = PROP_PATENT_TITLE, 
                prop_val = title, 
            )
        )
        
        return patent_id_set
    
    else:
        raise AssertionError


def query_patent_by_title(title: str,
                          source: str = 'JanusGraph') -> list[dict[str, Any]]:
    janusgraph_client = get_janusgraph_client()
    es_client = get_es_client()
    
    title = title.strip() 
                         
    if source == 'ES':
        index = es_client.get_index('patent_v10', 'patent_v10')

        paper_map: dict[str, dict[str, Any]] = dict() 

        for paper_entry in index.query_X_eq_x(X='title', x=title):
            paper_map[paper_entry['_id']] = paper_entry
            
        for paper_entry in index.query_X_eq_x(X='titleLowercase', x=normalize_str(title)):
            paper_map[paper_entry['_id']] = paper_entry

        return list(paper_map.values())
    
    elif source == 'JanusGraph':
        patent_id_set = query_patent_id_by_title(title)
        
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
