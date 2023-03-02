import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)

import json 
from tqdm import tqdm 
from pprint import pprint 

import jojo_es 

PAPER_TITLE = "Effect of pH on hydrogen production from glucose by a mixed culture"


def main():
    es_client = jojo_es.ESClient(
        host = '124.205.141.242', 
        port = 10000, 
        password = '6GYZTyH6D3fR4Y',
    )
    paper_index = es_client.get_index('mag_paper')
    
    paper_entry_list = paper_index.query_X_eq_x(
        X = 'original_title.text', 
        x = PAPER_TITLE, 
        limit = 10, 
    )
    
    pprint(paper_entry_list)


if __name__ == '__main__':
    main() 
