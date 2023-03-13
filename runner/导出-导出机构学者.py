import sys 
import os 
_dir = os.path.dirname(__file__) 
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

import json 
from tqdm import tqdm 

import core 


def main():
    scholar_entry_dict = dict() 
    
    with open('./input/org_name.txt', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp.readlines()):
            org_name = line.strip() 
            
            scholar_entry_list = core.query_scholar_by_org(org_name)

            for scholar_entry in scholar_entry_list:
                scholar_id = int(scholar_entry['id'])
                name = scholar_entry['name'].strip() 
                org_name = scholar_entry['org_name'].strip() 
                
                scholar_entry_dict[scholar_id] = dict(
                    id = scholar_id, 
                    name = name, 
                    org_name = org_name, 
                )
    
    with open('./output/scholar_info.json', 'w', encoding='utf-8') as fp:
        for scholar_entry in scholar_entry_dict.values():
            entry_json = json.dumps(scholar_entry, ensure_ascii=False).strip() 
            print(entry_json, file=fp)


if __name__ == '__main__':
    main() 
