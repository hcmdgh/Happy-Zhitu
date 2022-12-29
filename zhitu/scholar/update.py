from ..connection import * 
from .query import * 
from ..util import * 

from typing import Optional 

__all__ = [
    'add_scholar_title', 
    'update_scholar_title', 
]


def add_scholar_title(scholar_id: int,
                      title: Optional[str]):
    scholar_entry = query_scholar_by_id(scholar_id)
    assert scholar_entry 
    
    old_title = scholar_entry['title']
    new_title = merge_title(old_title, title)

    update_scholar_title(
        scholar_id = scholar_id, 
        title = new_title,
    )
    

def update_scholar_title(scholar_id: int,
                         title: Optional[str]):
    client = get_or_create_mysql_connection()
    table = client.get_table('dump', 'scholar_basic')
    
    table.update_by_id(
        id = scholar_id, 
        title = title, 
    )
