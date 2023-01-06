import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import core 

import json 
from tqdm.auto import tqdm 
from typing import Any, Optional 
from datetime import datetime


def main():
    org_map: dict[str, dict[str, Any]] = dict()
    
    with open('/MAG/zhitu/mag_zhitu_org_map.json', 'r', encoding='utf-8') as fp: 
        for line in fp:
            org_entry = json.loads(line)
            org_name = org_entry['org_name']
            org_map[org_name] = org_entry 
    
    scholar_map: dict[int, dict[str, Any]] = dict()
    
    with open('/MAG/zhitu/wzm/paper_author_field.json', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp):
            paper_entry = json.loads(line)
            scholar_list = paper_entry.get('scholar_list') 
            
            if scholar_list:
                for scholar_entry in scholar_list:
                    scholar_id = int(scholar_entry['scholar_id']) 
                    scholar_name = scholar_entry['scholar_name'].strip() 
                    scholar_org = scholar_entry['scholar_org'].strip()
                    
                    if scholar_id not in scholar_map:
                        scholar_map[scholar_id] = dict(
                            _id = scholar_id,
                            createTime = core.get_now_datetime_str('-'),
                            updateTime = core.get_now_datetime_str('-'),
                            scholarId = scholar_id, 
                            enName = scholar_name, 
                            name = scholar_name, 
                            orgId = org_map[scholar_org]['zhitu_zh_org_id'],
                            orgName = org_map[scholar_org]['org_zh_name'],
                            awardValue = 30, 
                            basicIndex = 40,
                        ) 
                        
    with open('/MAG/zhitu/wzm/es_scholar.json', 'w', encoding='utf-8') as fp:
        for scholar_entry in tqdm(scholar_map.values()):
            json_str = json.dumps(scholar_entry, ensure_ascii=False).strip() 
            print(json_str, file=fp)
    
    
if __name__ == '__main__':
    main() 
