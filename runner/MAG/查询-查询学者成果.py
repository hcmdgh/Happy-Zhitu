import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '../..'))
sys.path.append(os.path.join(_dir, '../../submodule/package'))

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
        host = '124.205.141.242',
        password = '6GYZTyH6D3fR4Y', 
        port = 10000,  
    )
    author_index = es_client.get_index('mag_author')
    paper_index = es_client.get_index('mag_paper')
    paper_author_index = es_client.get_index('mag_paper_author_affiliation')
            
    for scholar_id in tqdm(scholar_id_set, disable=True):
        scholar_entry = core.query_scholar_by_id(scholar_id)

        if not scholar_entry:
            print(f"学者id不存在：{scholar_id}")
        else:
            scholar_name = scholar_entry['name']
            scholar_org = scholar_entry['org_name']
            
            paper_author_list = paper_author_index.query_X_eq_x


if __name__ == '__main__':
    main() 
