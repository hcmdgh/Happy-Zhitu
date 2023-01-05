from ..client import * 
from ..util import * 

from typing import Optional, Any 

__all__ = [
    'query_scholar_by_name_org', 
    'smart_query_scholar_by_name_org', 
    'query_scholar_by_id', 
    'query_scholar_paper', 
]


def query_scholar_by_name_org(scholar_name: str,
                              scholar_org: str) -> list[dict[str, Any]]:
    mysql_client = get_mysql_client()
    
    table = mysql_client.get_table('dump', 'scholar_basic')
    
    entry_list = table.query_X_eq_x_and_Y_eq_y(
        X = 'name', 
        x = scholar_name.strip(),
        Y = 'org_name', 
        y = scholar_org.strip(),          
    )
    
    return entry_list


def smart_query_scholar_by_name_org(scholar_name: str,
                                    scholar_org: str) -> list[dict[str, Any]]:
    raise NotImplementedError


def query_scholar_by_id(scholar_id: int) -> Optional[dict[str, Any]]:
    mysql_client = get_mysql_client()
    
    table = mysql_client.get_table('dump', 'scholar_basic')
    
    entry = table.query_by_id(id=scholar_id)
    
    return entry 


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
