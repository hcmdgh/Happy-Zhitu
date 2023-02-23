import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

from pprint import pprint 

import core 

SCHOLAR_ID = 28681261240  # 庄福振
SCHOLAR_ID = 14372606192  # 王德庆


def main():
    paper_list = core.query_scholar_paper(
        scholar_id = SCHOLAR_ID, 
        source = 'JanusGraph', 
    )
    print(len(paper_list))

    title_list = [] 
    
    for paper in paper_list:
        title = paper['paper_title']
        title_list.append(title)

    title_list.sort() 
    
    for title in title_list:
        print(title)
    

if __name__ == '__main__':
    main() 
