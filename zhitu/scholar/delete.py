from ..connection import * 

__all__ = [
    'delete_scholar', 
]


def delete_scholar(scholar_id: int):
    client = get_or_create_mysql_connection()
    table = client.get_table('dump', 'scholar_basic')
    
    table.delete_by_id(scholar_id)
    
    client = get_or_create_janusgraph_connection()
    
    client.delete_vertex(scholar_id)
