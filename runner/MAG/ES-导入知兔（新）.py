import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import core 

import json 
import lzma 
from tqdm.auto import tqdm 
from concurrent.futures import ThreadPoolExecutor, as_completed
import jojo_es 
import traceback
from typing import Any, Optional, Iterator  

BATCH_SIZE = 10000


def bulk_insert(es_client: jojo_es.ESClient, 
                index_name: str,
                path: str,
                num_rows: int):
    index = es_client.get_index(index_name, index_name)
    # index.delete_index()
    
    if path.endswith('.json'):
        fp = open(path, 'r', encoding='utf-8') 
    elif path.endswith('.xz'):
        fp = lzma.open(path, 'rt', encoding='utf-8') 
    else:
        raise AssertionError
    
    with fp:
        entry_batch = [] 
        
        for line in tqdm(fp, desc=index_name, total=num_rows):
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
    
    for index_name, path, num_rows in [
        ('mag_zhitu_paper', '/MAG/zhitu/wzm/es/es_paper.json', 3171_8738), 
        # ('mag_zhitu_scholar_max_index', '/MAG/zhitu/wzm/es/es_scholar_max_index.json.xz'), 
        # ('mag_zhitu_scholar_index', '/MAG/zhitu/wzm/es/es_scholar_index.json.xz'),
        # ('mag_zhitu_scholar_history_index', '/MAG/zhitu/wzm/es/es_scholar_history_index.json.xz'),
        # ('mag_zhitu_scholar_performance_index', '/MAG/zhitu/wzm/es/es_scholar_performance_index.json.xz'),
    ]:
        thread = pool.submit(
            bulk_insert, 
            es_client = es_client, 
            index_name = index_name, 
            path = path,
            num_rows = num_rows, 
        )
        
        thread_list.append(thread)

    for thread in as_completed(thread_list):
        thread.result()    
        
    
if __name__ == '__main__':
    main() 
