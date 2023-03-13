import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

import csv 
from tqdm import tqdm 
from datetime import datetime

import core 


def main():
    client = core.get_mysql_client()
    table = client.get_table('dump.scholar_award')
    
    with open('./input/scholar_award.csv', 'r', encoding='utf-8') as fp:
        reader = csv.DictReader(fp)
        
        for entry in tqdm(list(reader)):
            scholar_name = entry['name'].strip() 
            scholar_org = entry['organization'].strip() 
            award_name = entry['awrad_name'].strip() 
            year = int(entry['year'])
            
            scholar_id_set = core.query_scholar_id_by_name_org(
                scholar_name = scholar_name, 
                scholar_org = scholar_org,
            )
            
            if not scholar_id_set:
                print(f"学者不存在：{scholar_name} {scholar_org}")
            else:
                scholar_id = scholar_id_set.pop() 
                
                table.insert_one(
                    dict(
                        name = scholar_name, 
                        organization = scholar_org,
                        year = year, 
                        award_name = award_name,
                        scholar_id = scholar_id, 
                        create_time = datetime.now(), 
                    )
                )                


if __name__ == '__main__':
    main() 
