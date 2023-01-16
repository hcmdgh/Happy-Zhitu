import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('..')

import core 

import json 
from tqdm.auto import tqdm 
from typing import Optional, Any 


def main():
    core.init_client()
    
    scholar_ids = set() 
    
    with open('./input/scholar_id.txt', 'r', encoding='utf-8') as fp: 
        for line in fp:
            scholar_id = int(line)
            scholar_ids.add(scholar_id)
            
    with open('./output/scholar_publish.json', 'w', encoding='utf-8') as fp: 
        for scholar_id in tqdm(scholar_ids):
            scholar_entry = core.query_scholar_by_id(scholar_id)
            
            if scholar_entry:
                scholar_entry['paper_list'] = core.query_scholar_paper(scholar_id=scholar_id, source='ES')
                scholar_entry['patent_list'] = core.query_scholar_patent(scholar_id=scholar_id, source='ES')
                scholar_entry['project_list'] = core.query_scholar_project(scholar_id=scholar_id, source='ES')

                json_str = core.json_dump(scholar_entry) 
                print(json_str, file=fp)  
            else:
                print(f"[ERROR] 学者id不存在：{scholar_id}")


if __name__ == '__main__':
    main() 
