import json 
from datetime import datetime

from .query import * 
from ..client import * 
from ..util import * 
from ..jojo_es import * 

from typing import Any, Optional

__all__ = [
    'create_paper', 
    'create_or_update_paper', 
]

google_es_client = ESClient(
    host = '124.205.141.242',
    port = 9202, 
)
google_paper_index = google_es_client.get_index('publication_copy_attributes', 'doc')


def create_google_paper(*,
                        google_paper_id: Optional[str] = None, 
                        google_paper_entry: Optional[dict[str, Any]] = None,
                        scholar_id: int,
                        tag: bool = True) -> dict[str, Any]:
    if google_paper_id:
        google_paper_entry = google_paper_index.query_by_id(google_paper_id)
        
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



def create_paper(paper_entry: dict[str, Any]) -> dict[str, Any]:
    janusgraph_client = get_janusgraph_client()
    
    paper_title = paper_entry.get('paper_title') 
    
    if not paper_title:
        return dict(
            error = dict(
                type = '论文信息缺少标题', 
                detail = paper_entry, 
            ),
            paper_id = None, 
            exist = None, 
            create = False, 
            update = False,  
        )
        
    paper_title_lowercase = normalize_str(paper_title, keep_space=True)
    paper_entry['paper_title_lowercase'] = paper_title_lowercase 
    
    exist_paper_ids = query_paper_id_by_title(paper_title)
    
    if exist_paper_ids:
        paper_id = exist_paper_ids.pop() 
        
        return dict(
            error = None,
            paper_id = paper_id, 
            exist = True, 
            create = False, 
            update = False,  
        )
    else:
        paper_id = janusgraph_client.create_vertex(
            v_label = LABEL_PAPER,
            prop_dict = paper_entry,
        )
        
        return dict(
            error = None,
            paper_id = paper_id, 
            exist = False, 
            create = True, 
            update = True,  
        )


def create_or_update_paper(paper_entry: dict[str, Any]) -> dict[str, Any]:
    janusgraph_client = get_janusgraph_client()
    
    paper_title = paper_entry.get('paper_title') 
    
    if not paper_title:
        return dict(
            error = dict(
                type = '论文信息缺少标题', 
                detail = paper_entry, 
            ),
            paper_id = None, 
            exist = None, 
            create = False, 
            update = False,  
        )
        
    paper_title_lowercase = normalize_str(paper_title, keep_space=True)
    paper_entry['paper_title_lowercase'] = paper_title_lowercase 
    
    exist_paper_ids = query_paper_id_by_title(paper_title)
    
    if exist_paper_ids:
        paper_id = exist_paper_ids.pop() 
        
        janusgraph_client.update_vertex(
            vid = paper_id, 
            prop_dict = paper_entry, 
        )
        
        return dict(
            error = None,
            paper_id = paper_id, 
            exist = True, 
            create = False, 
            update = True,  
        )
    else:
        paper_id = janusgraph_client.create_vertex(
            v_label = LABEL_PAPER,
            prop_dict = paper_entry,
        )
        
        return dict(
            error = None,
            paper_id = paper_id, 
            exist = False, 
            create = True, 
            update = True,  
        )
