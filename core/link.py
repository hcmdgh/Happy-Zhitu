from .client import * 
from .util import * 

__all__ = [
    'link_scholar_and_paper', 
    'link_scholar_and_patent', 
    'link_scholar_and_project', 
    'link_paper_and_field', 
    'link_patent_and_field', 
    'link_project_and_field', 
]


def link_scholar_and_paper(scholar_id: int,
                           paper_id: int):
    janusgraph_client = get_janusgraph_client()
    
    janusgraph_client.create_edge(
        src_vid = scholar_id, 
        dest_vid = paper_id, 
        edge_label = LABEL_HAS_PAPER, 
    )


def link_scholar_and_patent(scholar_id: int,
                            patent_id: int):
    janusgraph_client = get_janusgraph_client()
    
    janusgraph_client.create_edge(
        src_vid = scholar_id, 
        dest_vid = patent_id, 
        edge_label = LABEL_HAS_PATENT, 
    )
    
    
def link_scholar_and_project(scholar_id: int,
                             project_id: int):
    janusgraph_client = get_janusgraph_client()
    
    janusgraph_client.create_edge(
        src_vid = scholar_id, 
        dest_vid = project_id, 
        edge_label = LABEL_HAS_PROJECT, 
    )


def link_paper_and_field(paper_id: int,
                         field_id: int):
    janusgraph_client = get_janusgraph_client()
    
    janusgraph_client.create_edge(
        src_vid = paper_id, 
        dest_vid = field_id, 
        edge_label = LABEL_HAS_PAPER_FIELD, 
    )


def link_patent_and_field(patent_id: int,
                          field_id: int):
    janusgraph_client = get_janusgraph_client()
    
    janusgraph_client.create_edge(
        src_vid = patent_id, 
        dest_vid = field_id, 
        edge_label = LABEL_HAS_PATENT_FIELD, 
    )


def link_project_and_field(project_id: int,
                           field_id: int):
    janusgraph_client = get_janusgraph_client()
    
    janusgraph_client.create_edge(
        src_vid = project_id, 
        dest_vid = field_id, 
        edge_label = LABEL_HAS_PROJECT_FIELD, 
    )
