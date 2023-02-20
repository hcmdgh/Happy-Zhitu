from .query import * 
from ..client import * 
from ..util import * 

from typing import Any, Optional

__all__ = [
    'create_or_update_project', 
]


def create_or_update_project(project_entry: dict[str, Any]) -> dict[str, Any]:
    janusgraph_client = get_janusgraph_client()
    
    project_title = project_entry.get('project_title') 
    
    if not project_title:
        return dict(
            error = dict(
                type = '项目信息缺少标题', 
                detail = project_entry, 
            ),
            project_id = None, 
            exist = None, 
            create = False, 
            update = False,  
        )
        
    exist_project_ids = query_project_id_by_title(project_title)
    
    if exist_project_ids:
        project_id = exist_project_ids.pop() 
        
        janusgraph_client.update_vertex(
            vid = project_id, 
            prop_dict = project_entry, 
        )
        
        return dict(
            error = None,
            project_id = project_id, 
            exist = True, 
            create = False, 
            update = True,  
        )
    else:
        project_id = janusgraph_client.create_vertex(
            v_label = LABEL_PROJECT,
            prop_dict = project_entry,
        )
        
        return dict(
            error = None,
            project_id = project_id, 
            exist = False, 
            create = True, 
            update = True,  
        )
