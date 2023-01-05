import zhitu 

from flask import Blueprint, request 
import time 
from typing import Any, Optional 

bp = Blueprint('zhitu/org', __name__, url_prefix='/zhitu/org')


@bp.route('/query-org-id-by-name', methods=['GET'])
def query_org_id_by_name() -> dict[str, Any]:
    start_time = time.time()
    
    org_name = request.json['org_name'].strip() 
    
    org_id_set = zhitu.query_org_id_by_name(org_name)
    
    return dict(
        error = None, 
        org_id_list = list(org_id_set), 
        time = time.time() - start_time, 
    ) 


@bp.route('/create-org', methods=['POST'])
def create_org() -> dict[str, Any]:
    start_time = time.time()
    
    org_name = request.json['org_name'].strip() 
    
    result = zhitu.create_org(org_name=org_name)
    
    return dict(
        error = result.get('error'), 
        org_id = result.get('org_id'), 
        exist = result.get('exist'), 
        create = result.get('create'), 
        time = time.time() - start_time, 
    ) 
