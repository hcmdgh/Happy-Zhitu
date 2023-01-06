import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import core 

import json 
from tqdm.auto import tqdm 
from typing import Any, Optional 


def main():
    with open('/MAG/zhitu/wzm/es_paper.json', 'w', encoding='utf-8') as writer:
        with open('/MAG/zhitu/wzm/paper_author_field.json', 'r', encoding='utf-8') as reader:
            for line in tqdm(reader):
                paper_entry = json.loads(line)
                paper_id = int(paper_entry['id'])
                scholar_list = paper_entry.get('scholar_list') 
                field_list = paper_entry.get('field_list') 

                if field_list:
                    field_id_list = [ entry['field_id'] for entry in field_list ]
                else:
                    field_id_list = []
                
                if scholar_list:
                    for scholar_entry in scholar_list:
                        scholar_id = int(scholar_entry['scholar_id']) 
                        scholar_name = scholar_entry['scholar_name'].strip() 
                        scholar_org = scholar_entry['scholar_org'].strip()
                        scholar_org = core.translate_org_name_to_zh(scholar_org)
                        
                        entry = dict(
                            _id = f"{scholar_id}-{paper_id}",
                            createTime = core.get_now_datetime_str('-'),
                            updateTime = core.get_now_datetime_str('-'),
                            scholarId = scholar_id,
                            scholarName = scholar_name, 
                            orgName = scholar_org, 
                            publishId = str(paper_id), 
                            publishType = 'Paper', 
                            fieldIds = field_id_list, 
                        )
                        
                        json_str = json.dumps(entry, ensure_ascii=False).strip() 
                        print(json_str, file=writer)
                        
    
if __name__ == '__main__':
    main() 
