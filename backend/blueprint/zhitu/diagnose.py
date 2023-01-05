import core 

from flask import Blueprint, request 
import time 
from typing import Any, Optional 

bp = Blueprint('zhitu/diagnose', __name__, url_prefix='/zhitu/diagnose')


@bp.route('/diagnose-all', methods=['GET'])
def diagnose_all() -> dict[str, Any]:
    start_time = time.time()
    
    result = core.diagnose_all() 
    
    result['time'] = time.time() - start_time 
    
    return result 
