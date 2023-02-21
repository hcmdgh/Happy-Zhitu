import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

import core

from pprint import pprint  
from tqdm import tqdm 
import json 

TABLE_NAME = 'GengHao.20230215_provincial_award'
TYPE = 'project'


def main():
    mysql_client = core.get_mysql_client()
    mysql_table = mysql_client.get_table(TABLE_NAME)
    
    for entry in tqdm(mysql_table.scan_table(), total=mysql_table.count()):
        try:
            table_id = int(entry['id'])
            publish_id = int(entry['zhitu_id'])

            field_id_set = {
                int(entry['field_l1_id']), 
                *json.loads(entry['field_l2_id']),     
                *json.loads(entry['field_l3_id']),     
            }
        except Exception:
            print(f"错误的数据：{entry}")
        else:
            for field_id in field_id_set:
                field_id = int(field_id)
                
                if TYPE == 'paper':
                    core.link_paper_and_field(paper_id=publish_id, field_id=field_id)
                elif TYPE == 'patent':
                    core.link_patent_and_field(patent_id=publish_id, field_id=field_id)
                elif TYPE == 'project':
                    core.link_project_and_field(project_id=publish_id, field_id=field_id)
                else:
                    raise AssertionError 
                
            field_ids_json = json.dumps(list(field_id_set), ensure_ascii=False)

            mysql_table.update_by_id(
                id = table_id, 
                field_zhitu_ids = field_ids_json, 
            )


if __name__ == '__main__':
    main() 
