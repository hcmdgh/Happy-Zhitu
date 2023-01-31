import sys 
import os 
os.chdir(os.path.dirname(__file__))
sys.path.append('..')

import core 

import csv 
from tqdm import tqdm 

# CSV格式的学者详情，表的列名需要与scholar_basic表一致。
SCHOLAR_INFO_CSV_PATH = './input/scholar_info.csv'


def main():
    with open(SCHOLAR_INFO_CSV_PATH, 'r', encoding='utf-8') as fp:
        reader = csv.DictReader(fp)

        for entry in tqdm(list(reader)):
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
                    core.link_scholar_and_paper(scholar_id=scholar_id, paper_id=paper_id)
                    
                for patent_id in match_result['patent']:
                    core.link_scholar_and_patent(scholar_id=scholar_id, patent_id=patent_id)

                for project_id in match_result['project']:
                    core.link_scholar_and_project(scholar_id=scholar_id, project_id=project_id)
                

if __name__ == '__main__':
    main() 
