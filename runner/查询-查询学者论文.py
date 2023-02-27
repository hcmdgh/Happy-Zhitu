import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

from pprint import pprint 

import core 

SCHOLAR_ID = 14372606192  # 王德庆
SCHOLAR_ID = 28681261240  # 庄福振


def main():
    paper_list = core.query_scholar_paper(
        scholar_id = SCHOLAR_ID, 
        source = 'JanusGraph', 
    )
    print(len(paper_list))

    paper_list.sort(key=lambda x: x['paper_title'])

    for paper in paper_list:
        title = paper['paper_title']
        citation_cnt = paper['n_citation']
        
        print(title)
        print(citation_cnt)
        print()


if __name__ == '__main__':
    main() 
