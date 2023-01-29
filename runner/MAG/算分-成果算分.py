import json 
from dataclasses import dataclass 
from tqdm.auto import tqdm 
import numpy as np 
from typing import Any, Optional 


@dataclass 
class Org:
    ztid: int 
    name: str
    zh_name: str 
    

@dataclass 
class Scholar:
    ztid: int 
    name: str 
    org: Org 
    paper_list: list['Paper']
    
    
@dataclass 
class Field:
    ztid: int 
    name: str
    zh_name: str 
    level: int  
    
    
@dataclass
class Paper:
    ztid: int 
    title: str 
    field_list: list[Field]
    year: int 
    citation_count: int 
    score: float 
    
    
@dataclass 
class ScholarField:
    scholar: Scholar 
    field: Field 
    history_score: float 
    recent_score: float 
    overall_score: float 
    
    
def compute_paper_score(citation_count: int) -> float:
    # citation_count: 0 -> score: 60
    # citation_count: 10 -> score: 80
    # citation_count: 20 -> score: 90
    # citation_count: 30 -> score: 95
    score = 60 + 40 * ( 1 - (2**0.1) ** (-citation_count) ) 
    
    return score 
    
    
def main():
    field_map: dict[int, Field] = dict() 
    org_map: dict[str, Org] = dict() 
    paper_map: dict[int, Paper] = dict() 
    scholar_map: dict[int, Scholar] = dict() 
    
    with open('/MAG/zhitu/field_map_L012_enriched.json', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp):
            entry = json.loads(line)
            field_id = int(entry['field_zhituid']) 
            field_map[field_id] = Field(
                ztid = field_id, 
                name = entry['field_name'].strip(),
                zh_name = entry['field_zh_name'].strip(),
                level = int(entry['field_level']) + 1, 
            )
            
    with open('/MAG/zhitu/mag_zhitu_org_map.json', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp):
            entry = json.loads(line)
            org_id = int(entry['zhitu_zh_org_id']) 
            org_name = entry['org_name'].strip()
            org_zh_name = entry['org_zh_name'].strip()
            
            org_map[org_name] = Org(
                ztid = org_id, 
                name = org_name, 
                zh_name = org_zh_name, 
            )
            
    with open('/MAG/zhitu/wzm/paper_author_field.json', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp, total=None):
            entry = json.loads(line)
            
            field_id_set = { int(field['field_id']) for field in entry['field_list'] }
            field_list = [ field_map[field_id] for field_id in field_id_set if field_id in field_map ]

            paper = Paper(
                ztid = int(entry['id']),
                title = entry['title'].strip(), 
                field_list = field_list, 
                year = int(entry['raw_data']['year']),
                citation_count = int(entry['raw_data']['citationCount']),
                score = compute_paper_score(int(entry['raw_data']['citationCount'])), 
            )
            paper_map[paper.ztid] = paper 

            for scholar in entry['scholar_list']:
                scholar_id = int(scholar['scholar_id'])
                scholar_name = scholar['scholar_name'].strip() 
                scholar_org = scholar['scholar_org'].strip() 

                if scholar_id not in scholar_map:
                    scholar_map[scholar_id] = Scholar(
                        ztid = scholar_id, 
                        name = scholar_name, 
                        org = org_map[scholar_org], 
                        paper_list = [paper], 
                    )
                else:
                    scholar_map[scholar_id].paper_list.append(paper)


if __name__ == '__main__':
    main() 
