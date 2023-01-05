from .query import * 
from ..util import * 
from ..client import * 

from typing import Optional, Any 

__all__ = [
    'add_scholar_title', 
    'update_scholar_title', 
]


def add_scholar_title(scholar_id: int,
                      title: Optional[str]) -> dict[str, Any]:
    scholar_entry = query_scholar_by_id(scholar_id)
    
    if not scholar_entry:
        return dict(
            error = dict(
                type = '学者id不存在', 
                detail = dict(
                    scholar_id = scholar_id, 
                ),
            )
        )
    
    old_title = scholar_entry['title']
    new_title = merge_title(old_title, title)

    return update_scholar_title(
        scholar_id = scholar_id, 
        title = new_title,
    )
    

def update_scholar_title(scholar_id: int,
                         title: Optional[str]) -> dict[str, Any]:
    mysql_client = get_mysql_client()
    
    table = mysql_client.get_table('dump', 'scholar_basic')
    
    if not table.query_by_id(scholar_id):
        return dict(
            error = dict(
                type = '学者id不存在', 
                detail = dict(
                    scholar_id = scholar_id, 
                ),
            )
        )
    
    table.update_by_id(
        id = scholar_id, 
        title = title, 
    )

    return dict(
        error = None, 
    )
