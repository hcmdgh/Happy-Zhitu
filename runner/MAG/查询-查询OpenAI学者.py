import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)

from tqdm import tqdm 

import jojo_es 

AUTHOR_NAMES_PATH = '../input/scholar_name.txt'
ORG_MAGID = 2747134083


def norm_name(name: str) -> str:
    out = str()
    
    for ch in name:
        if ch.isalnum():
            out += ch.lower() 
        else:
            out += ' '
            
    out = ' '.join(out.split()) 
    
    return out 


def main():
    es_client = jojo_es.ESClient(
        host = '124.205.141.242', 
        port = 10000, 
        password = '6GYZTyH6D3fR4Y',
    )
    author_index = es_client.get_index('mag_author')
    
    author_name_set = set() 
    
    with open(AUTHOR_NAMES_PATH, 'r', encoding='utf-8') as fp:
        for line in fp:
            name = line.strip() 
            
            if name: 
                author_name_set.add(name)
                
    with open('../output/scholar_magid.txt', 'w', encoding='utf-8') as fp:
        for author_name in tqdm(author_name_set):
            norm_author_name = norm_name(author_name)
            
            author_entry_list = author_index.query_X_eq_x_and_Y_eq_y(
                X = 'normalized_name', 
                x = norm_author_name,
                Y = 'last_known_affiliation_id', 
                y = ORG_MAGID, 
            )
            
            if author_entry_list:
                author_magid = int(author_entry_list[0]['id']) 
                print(author_magid, file=fp)


if __name__ == '__main__':
    main() 
