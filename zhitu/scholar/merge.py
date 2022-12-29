from ..connection import * 
from ..constant import * 
from .delete import * 

__all__ = [
    'merge_scholar', 
]


def merge_scholar(src_id: int,
                  target_id: int):
    client = get_or_create_janusgraph_connection()
    
    if not client.is_vertex_exist(src_id) or not client.is_vertex_exist(target_id):
        print(f"[ERROR] 学者id不存在：{src_id} {target_id}")
        return 
    
    publish_vids = client.query_vertex_neighbor(
        vid = src_id, 
        in_or_out = False,
    )

    for publish_vid in publish_vids:
        prop_dict = client.query_vertex_by_vid(
            vid = publish_vid, 
            with_vid_and_label = True,
        )
        v_label = prop_dict['v_label']
        
        if v_label == LABEL_PAPER:
            client.create_edge(
                src_vid = target_id,
                dest_vid = publish_vid, 
                edge_label = LABEL_HAS_PAPER, 
            )
        elif v_label == LABEL_PATENT:
            client.create_edge(
                src_vid = target_id,
                dest_vid = publish_vid, 
                edge_label = LABEL_HAS_PATENT, 
            )
        elif v_label == LABEL_PROJECT:
            client.create_edge(
                src_vid = target_id,
                dest_vid = publish_vid, 
                edge_label = LABEL_HAS_PROJECT, 
            )
        else:
            pass 
            
    delete_scholar(src_id)
