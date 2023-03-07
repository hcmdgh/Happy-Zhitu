import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

import csv 
from tqdm import tqdm 
from typing import Any, Optional 

import core 

# CSV格式的学者详情，表的列名需要与scholar_basic表一致。
SCHOLAR_INFO_CSV_PATH = './input/scholar_info.csv'

# 输出的学者id
OUTPUT_SCHOLAR_ID_PATH = './output/scholar_id.txt'


def parse_csv_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return dict(
        name = entry['scholar_name'], 
        department = entry['college_name'], 
        org_name = entry['organization_name'], 
    ) 


def main():
    with open(SCHOLAR_INFO_CSV_PATH, 'r', encoding='utf-8') as fp:
        with open(OUTPUT_SCHOLAR_ID_PATH, 'w', encoding='utf-8') as fp_out:
            reader = csv.DictReader(fp)

            for entry in tqdm(list(reader)):
                entry = parse_csv_entry(entry)
                
                result = core.create_scholar(entry)

                if result['error']:
                    print(result['error'])
                else:
                    scholar_id = result['scholar_id']
                    scholar_name = result['scholar_name']
                    scholar_org = result['scholar_org']
                    assert scholar_id and scholar_name and scholar_org 
                    
                    match_result = core.match_scholar_with_publish(name=scholar_name, org=scholar_org)

                    print(f"【匹配成果】{scholar_id} {scholar_name} {len(match_result['paper'])} {len(match_result['patent'])} {len(match_result['project'])}")

                    for paper_id in match_result['paper']:
                        try:
                            core.link_scholar_and_paper(scholar_id=scholar_id, paper_id=paper_id)
                        except Exception:
                            pass 
                        
                    for patent_id in match_result['patent']:
                        try:
                            core.link_scholar_and_patent(scholar_id=scholar_id, patent_id=patent_id)
                        except Exception:
                            pass 

                    for project_id in match_result['project']:
                        try:
                            core.link_scholar_and_project(scholar_id=scholar_id, project_id=project_id)
                        except Exception:
                            pass 

                    print(scholar_id, file=fp_out)
                

if __name__ == '__main__':
    main() 
