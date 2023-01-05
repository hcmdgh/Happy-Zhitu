import zhitu 

from flask import Blueprint, request 
import time 
from typing import Any, Optional 

bp = Blueprint('zhitu/paper', __name__, url_prefix='/zhitu/paper')


@bp.route('/query-paper-by-title', methods=['GET'])
def query_paper_by_title() -> dict[str, Any]:
    start_time = time.time()
    
    paper_title = request.json['paper_title'].strip() 
    source = request.json['source'].strip() 
    
    paper_list = zhitu.query_paper_by_title(
        title = paper_title, 
        source = source, 
    )
    
    return dict(
        error = None, 
        paper_list = paper_list, 
        time = time.time() - start_time, 
    ) 
