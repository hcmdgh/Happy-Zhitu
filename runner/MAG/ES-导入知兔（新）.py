import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import core 

import json 
from tqdm.auto import tqdm 
from concurrent.futures import ThreadPoolExecutor, as_completed
import jojo_es 
import traceback
from typing import Any, Optional, Iterator  

BATCH_SIZE = 1000 


def bulk_insert(es_client: jojo_es.ESClient, 
                index_name: str,
                path: str):
    index = es_client.get_index(index_name, index_name)
    index.delete_index()
    
    with open(path, 'r', encoding='utf-8') as fp:
        entry_batch = [] 
        
        for line in tqdm(fp, desc=index_name, total=5590_0608):
            entry = json.loads(line)
            entry_batch.append(entry)
            
            if len(entry_batch) >= BATCH_SIZE:
                try:
                    index.bulk_insert(entry_batch)             
                except Exception:
                    traceback.print_exc()
                    
                entry_batch.clear()    
                
        if entry_batch:
            try:
                index.bulk_insert(entry_batch)             
            except Exception:
                traceback.print_exc()


def main():
    es_client = jojo_es.ESClient(host='192.168.0.90')
    pool = ThreadPoolExecutor(max_workers=10)
    thread_list = [] 
    
    for index_name, path in [
        ('mag_zhitu_scholar_history_index', '/MAG/zhitu/wzm/es/es_scholar_history_index_slim.json'), 
        ('mag_zhitu_scholar_performance_index', '/MAG/zhitu/wzm/es/es_scholar_performance_index_slim.json'),
        ('mag_zhitu_scholar_index', '/MAG/zhitu/wzm/es/es_scholar_index_slim.json'),
    ]:
        thread = pool.submit(
            bulk_insert, 
            es_client = es_client, 
            index_name = index_name, 
            path = path,
        )
        
        thread_list.append(thread)

    for thread in as_completed(thread_list):
        thread.result()    
        
    
if __name__ == '__main__':
    main() 
