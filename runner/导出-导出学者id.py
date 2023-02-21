import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

import core
from tqdm import tqdm 
import json 

TABLE_NAME = 'GengHao.20230215_provincial_award'


def main():
    mysql_client = core.get_mysql_client()
    mysql_table = mysql_client.get_table(TABLE_NAME)

    scholar_id_set = set() 
    
    for entry in tqdm(mysql_table.scan_table(), total=mysql_table.count()):
        scholar_id_list = json.loads(entry['scholar_zhitu_ids']) 
        scholar_id_set.update(scholar_id_list)
    
    with open('./output/scholar_id.txt', 'w', encoding='utf-8') as fp:
        for scholar_id in scholar_id_set:
            scholar_id = int(scholar_id)
            print(scholar_id, file=fp)


if __name__ == '__main__':
    main() 
