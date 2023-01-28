import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import core 

import json 
from tqdm.auto import tqdm 
from concurrent.futures import ThreadPoolExecutor 
import jojo_es 
import traceback
from typing import Any, Optional, Iterator  

BATCH_SIZE = 1000 


def bulk_insert(es_client: jojo_es.ESClient, 
                index_name: str):
    index = es_client.get_index(f'mag_zhitu_{index_name}', f'mag_zhitu_{index_name}')
    index.delete_index()
    
    filename = f'/MAG/zhitu/wzm/es/es_{index_name}.json'
    
    with open(filename, 'r', encoding='utf-8') as fp:
        entry_batch = [] 
        
        for line in fp:
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
    
    for index_name in tqdm(['paper',
                            'scholar',
                            'scholar_history_index',
                            'scholar_performance_index',
                            'scholar_index',
                            'scholar_publish_index']):
        thread = pool.submit(bulk_insert, es_client, index_name)
        thread_list.append(thread)
        
    
if __name__ == '__main__':
    main() 
