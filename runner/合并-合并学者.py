import sys 
import os 
os.chdir(os.path.dirname(__file__))
sys.path.append('..')

import core 
from tqdm import tqdm 

# 每行包含两个学者id，表示将后一个id合并至前一个id
SCHOLAR_ID_PATH = './input/merge_scholar_id.txt'


def main():
    with open(SCHOLAR_ID_PATH, 'r', encoding='utf-8') as fp:
        for line in tqdm(fp.readlines()):
            target_id, src_id = map(int, line.split())

            result = core.merge_scholar(
                src_id = src_id, 
                target_id = target_id, 
            )
            
            if result['error']:
                print(result['error'])


if __name__ == '__main__':
    main() 
