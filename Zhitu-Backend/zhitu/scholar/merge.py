from .delete import * 
from ..util import * 
from ..client import * 

from typing import Optional, Any 

__all__ = [
    'merge_scholar', 
]


def merge_scholar(src_id: int,
                  target_id: int) -> dict[str, Any]:
    if not janusgraph_client.is_vertex_exist(src_id) or not janusgraph_client.is_vertex_exist(target_id):
        return dict(
            error = dict(
                type = '学者id不存在', 
                detail = dict(
                    src_id = src_id, 
                    target_id = target_id, 
                ),
            ),
        )
    
    publish_vids = janusgraph_client.query_vertex_neighbor(
        vid = src_id, 
        in_or_out = False,
    )

    for publish_vid in publish_vids:
        prop_dict = janusgraph_client.query_vertex_by_vid(
            vid = publish_vid, 
            with_vid_and_label = True,
        )
        v_label = prop_dict['v_label']
        
        if v_label == LABEL_PAPER:
            janusgraph_client.create_edge(
                src_vid = target_id,
                dest_vid = publish_vid, 
                edge_label = LABEL_HAS_PAPER, 
            )
        elif v_label == LABEL_PATENT:
            janusgraph_client.create_edge(
                src_vid = target_id,
                dest_vid = publish_vid, 
                edge_label = LABEL_HAS_PATENT, 
            )
        elif v_label == LABEL_PROJECT:
            janusgraph_client.create_edge(
                src_vid = target_id,
                dest_vid = publish_vid, 
                edge_label = LABEL_HAS_PROJECT, 
            )
        else:
            pass 
            
    delete_scholar(src_id)

    return dict(
        error = None, 
    )
