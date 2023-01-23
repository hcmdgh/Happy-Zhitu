import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('..')

import core 

import json 
import csv 
from tqdm.auto import tqdm 
import traceback 
from concurrent.futures import ThreadPoolExecutor, as_completed 
from typing import Optional, Any 

NUM_THREADS = 20 


def run_thread(scholar_id_list: list[int],
               thread_id: int) -> dict[int, int]:
    scholar_paper_cnt_map = dict()
            
    for i, scholar_id in enumerate(tqdm(scholar_id_list)):
        if i % NUM_THREADS != thread_id:
            continue 
        
        try:
            paper_id_set = core.query_scholar_paper_id(scholar_id=scholar_id)
        except Exception:
            traceback.print_exc()
        else:
            scholar_paper_cnt_map[scholar_id] = len(paper_id_set)
            
    return scholar_paper_cnt_map


def main():
    scholar_id_set = set() 
    
    with open('./input/scholar_id.txt', 'r', encoding='utf-8') as fp: 
        for line in fp:
            scholar_id = int(line)
            scholar_id_set.add(scholar_id)
            
    scholar_id_list = list(scholar_id_set)
    
    scholar_paper_cnt_map = dict()
    
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        thread_list = [] 
        
        for i in range(NUM_THREADS):
            thread = executor.submit(
                run_thread, 
                scholar_id_list = scholar_id_list, 
                thread_id = i,
            )
            thread_list.append(thread)
        
        for thread in as_completed(thread_list):
            scholar_paper_cnt_map.update(thread.result()) 
            
    with open('./output/scholar_paper_cnt_map.csv', 'w', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=['scholar_id', 'paper_cnt'])
        writer.writeheader()
        
        for scholar_id, paper_cnt in scholar_paper_cnt_map.items():
            writer.writerow(
                dict(
                    scholar_id = scholar_id,
                    paper_cnt = paper_cnt, 
                )
            )


if __name__ == '__main__':
    main() 
