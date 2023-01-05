import core

from flask import Blueprint, request 
import time 
from typing import Any, Optional 

bp = Blueprint('zhitu/scholar', __name__, url_prefix='/zhitu/scholar')


@bp.route('/query-scholar-paper', methods=['GET'])
def query_scholar_paper() -> dict[str, Any]:
    start_time = time.time()
    
    scholar_id = int(request.json['scholar_id']) 
    source = request.json['source'].strip() 
    
    paper_list = core.query_scholar_paper(
        scholar_id = scholar_id, 
        source = source, 
    )
    
    return dict(
        error = None, 
        paper_list = paper_list, 
        time = time.time() - start_time, 
    ) 
