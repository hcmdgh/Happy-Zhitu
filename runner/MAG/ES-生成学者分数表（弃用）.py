import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import core 

import json 
from tqdm.auto import tqdm 
import numpy as np 
from typing import Any, Optional 


def compute_score(history_score: float, 
                  recent_score: float) -> float:
    return history_score * 0.4 + recent_score * 0.6 


def main():
    scholar_map: dict[int, dict[str, Any]] = dict() 

    with open('/MAG/zhitu/wzm/es_scholar.json', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp, total=960_9974):
            entry = json.loads(line)
            scholar_id = int(entry['scholarId'])
            scholar_map[scholar_id] = entry 
    
    field_scholar_map: dict[int, dict[int, dict[str, Any]]] = dict() 
    
    with open('/MAG/zhitu/wzm/es_scholar_performance_index.json', 'r', encoding='utf-8') as fp_recent:
        with open('/MAG/zhitu/wzm/es_scholar_history_index.json', 'r', encoding='utf-8') as fp_history:
            for line_recent, line_history in tqdm(zip(fp_recent, fp_history), total=None):  
                recent_entry = json.loads(line_recent)
                history_entry = json.loads(line_history)
                scholar_id = int(recent_entry['scholarId']) 
                field_id = int(recent_entry['fieldId']) 
                assert scholar_id == int(history_entry['scholarId']) 
                assert field_id == int(history_entry['fieldId'])
                recent_score = float(recent_entry['performanceIndexScore']) 
                history_score = float(recent_entry['historyIndexScore']) 

                if field_id not in field_scholar_map:
                    field_scholar_map[field_id] = dict()
                
                field_scholar_map[field_id][scholar_id] = dict(
                    scholar_id = scholar_id, 
                    recent_score = recent_score, 
                    history_score = history_score, 
                    score = compute_score(history_score=history_score, recent_score=recent_score), 
                )
                
    sorted_field_scholar_map: dict[int, list[dict[str, Any]]] = dict()

    for field_id in field_scholar_map: 
        sorted_field_scholar_map[field_id] = sorted(
            field_scholar_map[field_id].values(), 
            key = lambda x: -x['score'],
        )
                 
    

if __name__ == '__main__':
    main() 
