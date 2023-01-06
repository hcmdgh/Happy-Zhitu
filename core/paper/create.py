from .query import * 
from ..client import * 
from ..util import * 

from typing import Any, Optional

__all__ = [
    'create_paper', 
]


def create_paper(paper_entry: dict[str, Any]) -> dict[str, Any]:
    janusgraph_client = get_janusgraph_client()
    
    paper_title = paper_entry.get('paper_title') 
    
    if not paper_title:
        return dict(
            error = dict(
                type = '论文信息缺少标题', 
                detail = paper_entry, 
            ),
            paper_id = None, 
            exist = None, 
            create = False, 
            update = False,  
        )
        
    paper_title_lowercase = normalize_str(paper_title, keep_space=True)
    paper_entry['paper_title_lowercase'] = paper_title_lowercase 
    
    exist_paper_ids = query_paper_id_by_title(paper_title)
    
    if exist_paper_ids:
        paper_id = exist_paper_ids.pop() 
        
        return dict(
            error = None,
            paper_id = paper_id, 
            exist = True, 
            create = False, 
            update = False,  
        )
    else:
        paper_id = janusgraph_client.create_vertex(
            v_label = LABEL_PAPER,
            prop_dict = paper_entry,
        )
        
        return dict(
            error = None,
            paper_id = paper_id, 
            exist = False, 
            create = True, 
            update = True,  
        )
