import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

from tqdm import tqdm 
from pprint import pprint 

import core 

SCHOLAR_ID = 28681261240  # 庄福振
SCHOLAR_ID = 14372606192  # 王德庆


def norm_str(s: str) -> str:
    out = ''
    
    for ch in s:
        if ch.isalnum():
            out += ch.lower() 
            
    return out 


def main():
    gdb_client = core.get_janusgraph_client()
    
    paper_list = core.query_scholar_paper(
        scholar_id = SCHOLAR_ID, 
        source = 'JanusGraph', 
    )
    print(len(paper_list))
    
    paper_dict = dict() 

    for paper in tqdm(paper_list):
        title = paper['paper_title']
        norm_title = norm_str(title)
        
        try:
            citation_cnt = int(paper['n_citation']) 
        except:
            citation_cnt = 0 
        
        exist_paper = paper_dict.get(norm_title)
        
        if exist_paper:
            if exist_paper['n_citation'] < citation_cnt:
                gdb_client.delete_vertex(exist_paper['vid'])
                paper_dict[norm_title] = paper
        else:
            paper_dict[norm_title] = paper


if __name__ == '__main__':
    main() 
