from .client import * 
import core

import requests 
from concurrent.futures import ThreadPoolExecutor
import traceback 
from typing import Optional, Any 

__all__ = [
    'sync_scholar', 
]

executor = ThreadPoolExecutor(max_workers=50)


def task(scholar_id: int):
    try:
        resp = requests.get(
            url = f"http://192.168.0.91:9003/academic-data-calculate/scholar-index/update-scholar?scholarId={scholar_id}", 
        )
        if resp.status_code != 200: 
            print(resp.text) 
        
        resp = requests.get(
            url = f"http://192.168.0.88:9004/academic-data-calculate/scholar-index/update-scholar?scholarId={scholar_id}", 
        )
        if resp.status_code != 200: 
            print(resp.text) 
            
        print(f"FZK scholar_id: {scholar_id}")
    except Exception:
        traceback.print_exc()


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
            scholar_name = None, 
            scholar_org = None, 
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
    
    if result.get('scholar_id'): 
        zhitu_scholar_id = int(result['scholar_id'])
        
        executor.submit(task, zhitu_scholar_id)

    return dict(
        error = result.get('error'), 
        google_scholar_id = google_scholar_id, 
        zhitu_scholar_id = result.get('scholar_id'), 
        scholar_name = result.get('scholar_name'), 
        scholar_org = result.get('scholar_org'), 
        exist = result.get('exist'), 
        create = result.get('create'), 
        update = result.get('update'), 
    )
