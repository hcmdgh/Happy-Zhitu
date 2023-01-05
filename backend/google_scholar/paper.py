from .client import * 
import core 

from datetime import datetime
from typing import Any, Optional 

__all__ = [
    'sync_paper', 
]


def sync_paper(google_paper_id: str) -> dict[str, Any]:
    paper_entry = google_paper_index.query_by_id(google_paper_id)

    if not paper_entry:
        return dict(
            error = dict(
                type = '谷歌论文id不存在', 
                detail = dict(
                    google_paper_id = google_paper_id, 
                ),
            ), 
            google_paper_id = google_paper_id, 
            zhitu_paper_id = None, 
            exist = None, 
            create = False, 
            update = False, 
        )
    
    paper_entry['abst'] = paper_entry.get('abstract') 
    paper_entry['paper_title'] = paper_entry.get('title') 
    
    try:
        paper_entry['date'] = datetime.strptime(paper_entry.get('pub_date'), '%Y-%m-%d')  

        if paper_entry['date'].year <= 1900:
            paper_entry['date'] = None 
    except Exception:
        paper_entry['date'] = None 
    
    try:
        paper_entry['year'] = int(paper_entry.get('pub_year'))  
        
        if paper_entry['year'] <= 1900: 
            paper_entry['year'] = None 
    except Exception:
        paper_entry['year'] = None 

    paper_result = core.create_paper(paper_entry)
    
    zhitu_paper_id = paper_result.get('paper_id')

    if zhitu_paper_id:
        field_name_set: set[str] = set() 
        
        if paper_entry.get('first_class_tag'): 
            field_name_set.add(paper_entry['first_class_tag']) 
            
        if paper_entry.get('second_class_tags'): 
            field_name_set.update(paper_entry['second_class_tags']) 
            
        field_id_set: set[int] = set() 
        
        for field_name in field_name_set: 
            field_id_set.update(
                core.query_field_id_by_name(field_name)
            )
            
        for field_id in field_id_set: 
            core.link_paper_and_field(
                paper_id = zhitu_paper_id, 
                field_id = field_id, 
            )
            
    return dict(
        error = paper_result.get('error'), 
        google_paper_id = google_paper_id, 
        zhitu_paper_id = paper_result.get('paper_id'), 
        exist = paper_result.get('exist'), 
        create = paper_result.get('create'), 
        update = paper_result.get('update'), 
    )
