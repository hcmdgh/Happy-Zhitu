import google_scholar 

from flask import Blueprint, request 
import time 
from typing import Any, Optional  

bp = Blueprint('google-scholar/paper', __name__, url_prefix='/google-scholar/paper')


@bp.route('/sync-paper', methods=['POST'])
def sync_paper() -> dict[str, Any]:
    start_time = time.time()
    
    google_paper_id = request.json['google_paper_id'] 
    
    result = google_scholar.sync_paper(google_paper_id=google_paper_id)
    
    result['time'] = time.time() - start_time 
    
    return result 
