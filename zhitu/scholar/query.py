from ..connection import * 

from typing import Optional, Any 

__all__ = [
    'query_scholar_by_name_org', 
    'query_scholar_by_id', 
]


def query_scholar_by_name_org(scholar_name: str,
                              scholar_org: str) -> list[dict[str, Any]]:
    client = get_or_create_mysql_connection()
    table = client.get_table('dump', 'scholar_basic')
    
    entry_list = table.query_X_eq_x_and_Y_eq_y(
        X = 'name', 
        x = scholar_name.strip(),
        Y = 'org_name', 
        y = scholar_org.strip(),          
    )
    
    return entry_list


def query_scholar_by_id(scholar_id: int) -> Optional[dict[str, Any]]:
    client = get_or_create_mysql_connection()
    table = client.get_table('dump', 'scholar_basic')
    
    entry = table.query_by_id(id=scholar_id)
    
    return entry 
