import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

import core 

from tqdm import tqdm 
from typing import Optional, Any 
import json 
import traceback

DATABASE_NAME = 'GengHao'
TABLE_NAME = '20230215_provincial_award'


def convert_to_gdb_project_entry(raw_project_entry: dict[str, Any]) -> dict[str, Any]:
    gdb_project_entry = dict(raw_project_entry)
    
    del gdb_project_entry['id']
    del gdb_project_entry['field_l1']
    del gdb_project_entry['field_l2']
    del gdb_project_entry['field_l3']
    del gdb_project_entry['field_l1_id']
    del gdb_project_entry['field_l2_id']
    del gdb_project_entry['field_l3_id']
    del gdb_project_entry['finished']
    del gdb_project_entry['zhitu_id']
    
    return gdb_project_entry


def main():
    mysql_client = core.get_mysql_client()
    project_table = mysql_client.get_table(DATABASE_NAME, TABLE_NAME)
    
    for raw_entry in tqdm(project_table.scan_table(), total=project_table.count()):
        gdb_entry = convert_to_gdb_project_entry(raw_entry)
        
        result = core.create_or_update_project(gdb_entry)
        
        if result['error']:
            print(result['error'])
        else:
            project_id = result['project_id']
            assert project_id > 0

            project_table.update_by_id(
                id = raw_entry['id'], 
                zhitu_id = project_id, 
            )
            
            # 关联学者
            if True:
                scholar_orgs = set(gdb_entry['org'].split()) 
                scholar_names = set(gdb_entry['leader'].split())
                
                matched_scholar_ids = set() 
                
                for scholar_name in scholar_names:
                    for scholar_org in scholar_orgs:
                        scholar_ids = {
                            int(entry['id']) 
                            for entry in core.query_scholar_by_name_org(
                                scholar_name = scholar_name, 
                                scholar_org = scholar_org, 
                            )
                        }
                        
                        matched_scholar_ids.update(scholar_ids)

                for scholar_id in matched_scholar_ids:
                    try:
                        core.link_scholar_and_project(
                            scholar_id = scholar_id, 
                            project_id = project_id, 
                        )
                    except Exception:
                        traceback.print_exc()
                    
                scholar_ids_json = json.dumps(list(matched_scholar_ids), ensure_ascii=False)
                project_table.update_by_id(
                    id = raw_entry['id'], 
                    scholar_zhitu_ids = scholar_ids_json, 
                )


if __name__ == '__main__':
    main() 
