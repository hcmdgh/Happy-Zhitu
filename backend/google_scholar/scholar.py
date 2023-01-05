from .client import * 
import core

from typing import Optional, Any 

__all__ = [
    'sync_scholar', 
]


def sync_scholar(google_scholar_id: str) -> dict[str, Any]:
    scholar_entry = google_author_index.query_by_id(google_scholar_id)

    if not scholar_entry:
        return dict(
            error = dict(
                type = '谷歌学者id不存在', 
                detail = dict(
                    google_scholar_id = google_scholar_id, 
                ),
            ), 
            google_scholar_id = google_scholar_id, 
            zhitu_scholar_id = None, 
            exist = None,
            create = False,
            update = False,  
        )
    
    converted_scholar_entry = dict(
        name = scholar_entry.get('name'),
        org_name = scholar_entry.get('affiliation'), 
        email = scholar_entry.get('email'),
        phone = scholar_entry.get('tel'),
    ) 

    result = core.create_scholar(converted_scholar_entry)

    return dict(
        error = result.get('error'), 
        google_scholar_id = google_scholar_id, 
        zhitu_scholar_id = result.get('scholar_id'), 
        exist = result.get('exist'), 
        create = result.get('create'), 
        update = result.get('update'), 
    )
