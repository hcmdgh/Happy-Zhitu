import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

import csv 
from tqdm import tqdm 

import core 

SCHOLAR_INFO_CSV = './input/scholar_info.csv'
CSV_FIELD = 'college_name'
SCHOLAR_BASIC_FIELD = 'department'


def main():
    with open(SCHOLAR_INFO_CSV, 'r', encoding='utf-8') as fp:
        with open('./output/scholar_id.txt', 'w', encoding='utf-8') as fp_out:
            reader = csv.DictReader(fp) 

            for entry in tqdm(list(reader)):
                scholar_id = int(entry['scholar_id'])
                field_value = entry[CSV_FIELD]
                
                scholar_entry = core.query_scholar_by_id(scholar_id=scholar_id)

                if not scholar_entry:
                    print(f"学者不存在：{scholar_id}")
                else:
                    core.update_scholar_by_id(
                        scholar_id = scholar_id, 
                        **{ SCHOLAR_BASIC_FIELD: field_value },
                    )
                    
                    print(scholar_id, file=fp_out)
            

if __name__ == '__main__':
    main()  
