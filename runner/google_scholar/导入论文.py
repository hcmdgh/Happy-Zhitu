import sys 
import os 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import core 

import json 
from tqdm import tqdm 


def main():
    with open('../output/scholar_paper_map.json', 'r', encoding='utf-8') as fp:
        for line in tqdm


if __name__ == '__main__':
    main() 
