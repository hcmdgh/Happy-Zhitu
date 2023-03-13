import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

from pprint import pprint 

import core 

SCHOLAR_ID = 44466257968
SCHOLAR_ID = 44171436224
SCHOLAR_ID = 44171514048 


def main():
    scholar_entry = core.query_scholar_by_id(scholar_id=SCHOLAR_ID)
    print("【学者】")
    pprint(scholar_entry)
    print() 

    paper_entry_list = core.query_scholar_paper(
        scholar_id = SCHOLAR_ID, 
        source = 'JanusGraph', 
    )
    print("【论文】")
    pprint(paper_entry_list)
    print(len(paper_entry_list))
    print() 
    
    patent_entry_list = core.query_scholar_patent(
        scholar_id = SCHOLAR_ID, 
        source = 'JanusGraph', 
    )
    print("【专利】")
    pprint(patent_entry_list)
    print(len(patent_entry_list))
    print() 
    
    project_entry_list = core.query_scholar_project(
        scholar_id = SCHOLAR_ID, 
        source = 'JanusGraph', 
    )
    print("【项目】")
    pprint(project_entry_list)
    print(len(project_entry_list))
    print() 


if __name__ == '__main__':
    main() 
