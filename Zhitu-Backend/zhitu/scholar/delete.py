from ..client import * 

from typing import Any, Optional 

__all__ = [
    'delete_scholar', 
]


def delete_scholar(scholar_id: int) -> dict[str, Any]:
    table = mysql_client.get_table('dump', 'scholar_basic')
    table.delete_by_id(scholar_id)
    
    janusgraph_client.delete_vertex(scholar_id)

    return dict(
        error = None, 
    )
