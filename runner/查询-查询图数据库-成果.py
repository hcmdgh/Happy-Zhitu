import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

import core 

from pprint import pprint 

TITLE = 'A theoretical investigation on ESIPT process of a red-emitting ratiometric fluorescent probe and its fluorescent detection mechanism for cyanide anion'


def main():
    paper_list = core.query_paper_by_title(
        title = TITLE, 
        source = 'JanusGraph', 
    )
    print("【论文】")
    pprint(paper_list)
    print() 

    patent_list = core.query_patent_by_title(
        title = TITLE, 
        source = 'JanusGraph', 
    )
    print("【专利】")
    pprint(patent_list)
    print() 
    
    project_list = core.query_project_by_title(
        title = TITLE, 
        source = 'JanusGraph', 
    )
    print("【项目】")
    pprint(project_list)
    print() 


if __name__ == '__main__':
    main() 
