from jojo_es import * 
from pprint import pprint 
import json 
from typing import Any, Optional 

__all__ = [
    'tag_by_title', 
]

CLIENT = ESClient(
    host = '124.205.141.242', 
    port = 10000, 
    username = 'elastic', 
    password = '6GYZTyH6D3fR4Y', 
)

PAPER_INDEX = CLIENT.get_index('mag_paper')
PAPER_FIELD_INDEX = CLIENT.get_index('mag_paper_field')

FIELD_MAP: dict[int, dict[str, Any]] = dict()

with open('/MAG/zhitu/field_map_L012_enriched.json', 'r', encoding='utf-8') as fp:
    for line in fp:
        entry = json.loads(line)
        FIELD_MAP[entry['field_magid']] = entry  


def tag_by_title(title: str) -> list[dict[str, Any]]:
    entry_list = PAPER_INDEX.query_X_eq_x(
        X = 'paper_title.text',
        x = title.strip(),
        limit = 1,
    )
    assert len(entry_list) >= 1 
    
    paper_magid = int(entry_list[0]['id']) 
    
    entry_list = PAPER_FIELD_INDEX.query_X_eq_x(
        X = 'paper_id',
        x = paper_magid,
    )
    
    field_id_set = { int(entry['field_id']) for entry in entry_list }
    
    result = [ FIELD_MAP[field_id] for field_id in field_id_set if field_id in FIELD_MAP ] 
    
    return result 
