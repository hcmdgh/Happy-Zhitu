import google_scholar
import core 

from flask import Blueprint, request 
import time 
from typing import Any, Optional 

bp = Blueprint('google-scholar/scholar', __name__, url_prefix='/google-scholar/scholar')


@bp.route('/sync-scholar', methods=['POST'])
def sync_scholar() -> dict[str, Any]:
    start_time = time.time()
    
    google_scholar_id = request.json['google_scholar_id'] 
    
    result = google_scholar.sync_scholar(google_scholar_id=google_scholar_id)
    
    result['time'] = time.time() - start_time 
    
    return result 
