import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

from pprint import pprint 
from collections import defaultdict, Counter

import core 

SCHOLAR_ID = 44466257968
SCHOLAR_ID = 44171436224
SCHOLAR_ID = 37698629816
SCHOLAR_ID = 19020357696


def main():
    scholar_entry = core.query_scholar_by_id(scholar_id=SCHOLAR_ID)
    print("【学者】")
    pprint(scholar_entry)
    print() 

    paper_entry_list = core.query_scholar_paper(
        scholar_id = SCHOLAR_ID, 
        source = 'JanusGraph', 
    )
    
    year_list = [] 

    for paper_entry in paper_entry_list:
        year = int(paper_entry['year'])
        year_list.append(year)
    
    print("【论文】")
    print(sorted(Counter(year_list).items(), reverse=True))
    print() 
    
    # patent_entry_list = core.query_scholar_patent(
    #     scholar_id = SCHOLAR_ID, 
    #     source = 'JanusGraph', 
    # )
    # print("【专利】")
    # pprint(patent_entry_list)
    # print(len(patent_entry_list))
    # print() 
    
    # project_entry_list = core.query_scholar_project(
    #     scholar_id = SCHOLAR_ID, 
    #     source = 'JanusGraph', 
    # )
    # print("【项目】")
    # pprint(project_entry_list)
    # print(len(project_entry_list))
    # print() 


if __name__ == '__main__':
    main() 
