import core 

from flask import Blueprint, request 
import time 
from typing import Any, Optional 

bp = Blueprint('zhitu/field', __name__, url_prefix='/zhitu/field')


@bp.route('/query-field-id-by-name', methods=['GET'])
def query_field_id_by_name() -> dict[str, Any]:
    start_time = time.time()
    
    field_name = request.json['field_name'].strip() 
    
    field_id_set = core.query_field_id_by_name(field_name)
    
    return dict(
        error = None, 
        field_id_list = list(field_id_set), 
        time = time.time() - start_time, 
    ) 


@bp.route('/create-field', methods=['POST'])
def create_field() -> dict[str, Any]:
    start_time = time.time()
    
    field_name = request.json['field_name'].strip() 
    field_level = int(request.json['field_level']) 
    
    result = core.create_field(
        field_name = field_name, 
        field_level = field_level,
    )
    
    return dict(
        error = result.get('error'), 
        field_id = result.get('field_id'), 
        exist = result.get('exist'), 
        create = result.get('create'), 
        time = time.time() - start_time, 
    ) 
