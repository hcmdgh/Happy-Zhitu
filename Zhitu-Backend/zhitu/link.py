from .client import * 
from .util import * 

__all__ = [
    'link_scholar_and_paper', 
    'link_paper_and_field', 
]


def link_scholar_and_paper(scholar_id: int,
                           paper_id: int):
    janusgraph_client.create_edge(
        src_vid = scholar_id, 
        dest_vid = paper_id, 
        edge_label = LABEL_HAS_PAPER, 
    )


def link_paper_and_field(paper_id: int,
                         field_id: int):
    janusgraph_client.create_edge(
        src_vid = paper_id, 
        dest_vid = field_id, 
        edge_label = LABEL_HAS_PAPER_FIELD, 
    )
