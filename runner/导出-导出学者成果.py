import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('..')

import core 

import json 
import lzma 
import traceback
from tqdm.auto import tqdm 
from typing import Optional, Any 

SCHOLAR_ID_PATH = './input/scholar_id.txt' 
OUTPUT_PATH = './output/scholar_publish.json'
USE_XZ = True  


def main():
    scholar_ids = set() 
    
    with open(SCHOLAR_ID_PATH, 'r', encoding='utf-8') as fp: 
        for line in fp:
            scholar_id = int(line)
            scholar_ids.add(scholar_id)
            
    if not USE_XZ:
        fp = open(OUTPUT_PATH, 'w', encoding='utf-8')
    else:
        fp = lzma.open(OUTPUT_PATH + '.xz', 'wt', encoding='utf-8')
        
    with fp: 
        for scholar_id in tqdm(scholar_ids):
            scholar_entry = core.query_scholar_by_id(scholar_id)
            
            if scholar_entry:
                try:
                    scholar_entry['paper_list'] = core.query_scholar_paper(scholar_id=scholar_id, source='JanusGraph')
                except Exception: 
                    traceback.print_exc()
                    scholar_entry['paper_list'] = [] 
                    
                try:
                    scholar_entry['patent_list'] = core.query_scholar_patent(scholar_id=scholar_id, source='JanusGraph')
                except Exception: 
                    traceback.print_exc()
                    scholar_entry['patent_list'] = []
                    
                try:
                    scholar_entry['project_list'] = core.query_scholar_project(scholar_id=scholar_id, source='JanusGraph')
                except Exception: 
                    traceback.print_exc()
                    scholar_entry['project_list'] = []

                json_str = core.json_dump(scholar_entry) 
                print(json_str, file=fp)  
            else:
                print(f"[ERROR] 学者id不存在：{scholar_id}")


if __name__ == '__main__':
    main() 
