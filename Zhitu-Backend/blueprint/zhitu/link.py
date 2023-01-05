import zhitu 

from flask import Blueprint, request 
import time 
from typing import Any, Optional 

bp = Blueprint('zhitu/link', __name__, url_prefix='/zhitu/link')


@bp.route('/link-scholar-and-paper', methods=['POST'])
def link_scholar_and_paper() -> dict[str, Any]:
    start_time = time.time()
    
    scholar_id = int(request.json['scholar_id']) 
    paper_id = int(request.json['paper_id']) 
    
    zhitu.link_scholar_and_paper(
        scholar_id = scholar_id, 
        paper_id = paper_id, 
    )
    
    return dict(
        error = None, 
        time = time.time() - start_time, 
    ) 
