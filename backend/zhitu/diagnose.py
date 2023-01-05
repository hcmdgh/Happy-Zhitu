from .client import * 
from .paper import * 

import io 
import traceback
from uuid import uuid4
from typing import Any, Optional 

__all__ = [
    'diagnose_all',
]


def diagnose_all() -> dict[str, Any]:
    try:
        SCHOLAR_ID = 14372606192
        
        table = mysql_client.get_table('dump', 'scholar_basic')
        
        scholar_entry_list = table.query_X_eq_x('name', '王德庆')
        scholar_id_set = { entry['id'] for entry in scholar_entry_list }
        assert SCHOLAR_ID in scholar_id_set
        
        random_str = str(uuid4())
        table.update_by_id(id=SCHOLAR_ID, avatar=random_str)
        scholar_entry = table.query_by_id(SCHOLAR_ID)
        assert scholar_entry['avatar'] == random_str 
        
        paper_entry_list = query_scholar_paper(scholar_id=SCHOLAR_ID, source='JanusGraph')
        assert len(paper_entry_list) >= 10 
        title_list = [ entry['paper_title'] for entry in paper_entry_list ]
        assert '基于支持向量的迭代修正质心文本分类算法' in ' '.join(title_list)
        
        paper_entry_list = query_scholar_paper(scholar_id=SCHOLAR_ID, source='ES')
        assert len(paper_entry_list) >= 10 
        title_list = [ entry['title'] for entry in paper_entry_list ]
        assert '基于支持向量的迭代修正质心文本分类算法' in ' '.join(title_list)
    except Exception:
        sio = io.StringIO()
        traceback.print_exc(file=sio)
        error_msg = sio.getvalue()
        
        return dict(
            error = dict(
                type = '未知错误', 
                detail = error_msg, 
            ), 
        )
    else:
        return dict(
            error = None, 
        )
