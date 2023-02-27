import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)

import json 
from tqdm import tqdm 

import jojo_es 

AUTHOR_MAGID_PATH = '../output/scholar_magid.txt'


def main():
    es_client = jojo_es.ESClient(
        host = '124.205.141.242', 
        port = 10000, 
        password = '6GYZTyH6D3fR4Y',
    )
    author_index = es_client.get_index('mag_author')
    paper_index = es_client.get_index('mag_paper')
    paper_author_index = es_client.get_index('mag_paper_author_affiliation')
    
    author_magid_set = set() 
    
    with open(AUTHOR_MAGID_PATH, 'r', encoding='utf-8') as fp:
        for line in fp:
            author_magid = int(line)
            author_magid_set.add(author_magid)
            
    with open('../output/scholar_publish.json', 'w', encoding='utf-8') as fp:
        for author_magid in tqdm(author_magid_set):
            author_entry = author_index.query_by_id(author_magid)
            assert author_entry
            
            paper_author_entry_list = paper_author_index.query_X_eq_x(
                X = 'author_id', 
                x = author_magid, 
            )
            
            paper_magid_set = { paper_author_entry['paper_id'] for paper_author_entry in paper_author_entry_list }

            paper_entry_list = [] 

            for paper_magid in paper_magid_set:
                paper_entry = paper_index.query_by_id(paper_magid)
                assert paper_entry
                
                paper_entry_list.append(paper_entry)
                
            author_entry['paper_list'] = paper_entry_list 
            
            json_str = json.dumps(author_entry, ensure_ascii=False, indent=4)
            print(json_str, file=fp)


if __name__ == '__main__':
    main() 
