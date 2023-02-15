import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

import core 

from tqdm import tqdm 

SCHOLAR_ID_PATH = './input/scholar_id.txt'
DELETE_TITLE = '院士'


def main():
    scholar_id_set: set[int] = set() 

    with open(SCHOLAR_ID_PATH, 'r', encoding='utf-8') as fp:
        for line in fp:
            scholar_id = int(line)
            scholar_id_set.add(scholar_id)

    for scholar_id in tqdm(scholar_id_set):
        scholar_entry = core.query_scholar_by_id(scholar_id=scholar_id)

        if not scholar_entry:
            print(f"学者id不存在：{scholar_id}")
        else:
            scholar_title = scholar_entry['title']
            title_set = set(scholar_title.split()) 

            title_set.discard('院士')
            
            title_str = ' '.join(title_set)
            
            core.update_scholar_title(
                scholar_id = scholar_id, 
                title = title_str, 
            )
            
            
if __name__ == '__main__':
    main() 
