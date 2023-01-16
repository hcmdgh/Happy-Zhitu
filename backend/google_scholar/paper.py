from .client import * 
from .scholar import * 
import core 

import json 
import requests 
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional 

executor = ThreadPoolExecutor(max_workers=50)


def task(scholar_id: int):
    resp = requests.get(
        url = f"http://192.168.0.91:9003/academic-data-calculate/scholar-index/update-scholar?scholarId={scholar_id}", 
    )
    assert resp.status_code == 200 
    
    resp = requests.get(
        url = f"http://192.168.0.88:9004/academic-data-calculate/scholar-index/update-scholar?scholarId={scholar_id}", 
    )
    assert resp.status_code == 200 
    

__all__ = [
    'sync_paper', 
]


def link_paper_and_field(zhitu_paper_id: int,
                         field_name_set: set[str]):
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
    paper_entry['n_citation'] = paper_entry.get('num_citations') 
    paper_entry['doc_type'] = paper_entry.get('pub_type')
    paper_entry['keywords'] = paper_entry.get('keyword')
    
    author_name_list = [] 
    
    if paper_entry.get('author'):
        for author_name in paper_entry['author']:
            author_name_list.append(dict(name=author_name)) 
    
    if author_name_list:
        paper_entry['authors'] = json.dumps(author_name_list, ensure_ascii=False).strip() 
    
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

    paper_result = core.create_or_update_paper(paper_entry)
    
    zhitu_paper_id = paper_result.get('paper_id')

    if zhitu_paper_id:
        field_name_set: set[str] = set() 
        
        if paper_entry.get('first_class_tag'): 
            field_name_set.add(paper_entry['first_class_tag']) 
            
        if paper_entry.get('second_class_tags'): 
            field_name_set.update(paper_entry['second_class_tags']) 
            
        link_paper_and_field(
            zhitu_paper_id = zhitu_paper_id, 
            field_name_set = field_name_set, 
        )
            
    google_scholar_id_list = paper_entry.get('author_id')
    if not google_scholar_id_list:
        google_scholar_id_list = [] 

    for google_scholar_id in google_scholar_id_list:
        if google_scholar_id:
            scholar_result = sync_scholar(google_scholar_id=google_scholar_id) 

            zhitu_scholar_id = scholar_result.get('zhitu_scholar_id')
            
            if zhitu_scholar_id and zhitu_paper_id:
                core.link_scholar_and_paper(
                    scholar_id = zhitu_scholar_id, 
                    paper_id = zhitu_paper_id, 
                )
                
                executor.submit(task, zhitu_scholar_id)
            
    return dict(
        error = paper_result.get('error'), 
        google_paper_id = google_paper_id, 
        zhitu_paper_id = paper_result.get('paper_id'), 
        exist = paper_result.get('exist'), 
        create = paper_result.get('create'), 
        update = paper_result.get('update'), 
    )
