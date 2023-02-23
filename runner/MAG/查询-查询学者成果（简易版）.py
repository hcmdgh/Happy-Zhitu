import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '../..'))
sys.path.append(os.path.join(_dir, '../../submodule/package'))

import json 
import lzma 
from tqdm import tqdm 

import core 
import jojo_es 


def main():
    scholar_id_set = set() 
    
    with open('../input/scholar_id.txt', 'r', encoding='utf-8') as fp:
        for line in fp: 
            scholar_id = int(line.strip().strip('"'))
            scholar_id_set.add(scholar_id)

    es_client = jojo_es.ESClient(
        host = '192.168.0.90',
    )
    paper_index = es_client.get_index('mag_zhitu_paper', 'mag_zhitu_paper')
    
    exist_cnt = total_cnt = 0 
            
    with lzma.open('../output/MAG_scholar_paper.json.xz', 'wt', encoding='utf-8') as fp:
    # with open('../output/MAG_scholar_paper.json', 'wt', encoding='utf-8') as fp:
        for scholar_id in tqdm(scholar_id_set, disable=False):
            scholar_entry = core.query_scholar_by_id(scholar_id)

            if not scholar_entry:
                print(f"学者id不存在：{scholar_id}")
            else:
                del scholar_entry['matched']
                del scholar_entry['birthday']
                del scholar_entry['create_time']
                del scholar_entry['update_time']
                
                paper_entry_list = paper_index.query_X_eq_x(
                    X = 'scholars.scholarId', 
                    x = scholar_id, 
                )
                
                if paper_entry_list:
                    exist_cnt += 1 
                total_cnt += 1 

                if paper_entry_list:
                    json_entry = dict(scholar_entry)
                    json_entry['paper_list'] = paper_entry_list 
                    json_str = json.dumps(json_entry, ensure_ascii=False).strip() 
                    print(json_str, file=fp)
                
    print(f"{exist_cnt} / {total_cnt}")


if __name__ == '__main__':
    main() 
