import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import core 

import json 
from tqdm.auto import tqdm 
from concurrent.futures import ThreadPoolExecutor 
import jojo_es 
from typing import Any, Optional, Iterator  

BATCH_SIZE = 1000 


def read_json_file(path: str) -> Iterator[dict[str, Any]]:
    with open(path, 'r', encoding='utf-8') as fp:
        for line in fp:
            entry = json.loads(line)
            yield entry 
            
            
def bulk_insert(es_client: jojo_es.ESClient, 
                index_name: str):
    index = es_client.get_index(f'mag_zhitu_{index_name}', f'mag_zhitu_{index_name}')
    index.delete_index()
    index.bulk_insert(
        read_json_file(f'/MAG/zhitu/wzm/es/es_{index_name}.json'),
        batch_size = BATCH_SIZE,
    )   


def main():
    es_client = jojo_es.ESClient(host='192.168.0.90')
    pool = ThreadPoolExecutor(max_workers=10)
    
    for index_name in tqdm(['paper',
                            'scholar',
                            'scholar_history_index',
                            'scholar_performance_index',
                            'scholar_index',
                            'scholar_publish_index']):
        pool.submit(bulk_insert, es_client, index_name)
          
    
if __name__ == '__main__':
    main() 
