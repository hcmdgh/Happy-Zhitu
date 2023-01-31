import sys 
import os 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import core 

import json 
from datetime import datetime 
from tqdm import tqdm 


def main():
    with open('../output/scholar_paper_map.json', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp, total=5_3882):
            entry = json.loads(line)
            
            scholar_id_set = set(entry["scholar_ztid_list"])
            
            for paper_entry in entry['paper_list']:
                paper_entry.pop('id', None)
                
                paper_entry['abst'] = paper_entry.get('abstract') 
                paper_entry['paper_title'] = paper_entry.get('title') 
                paper_entry['n_citation'] = paper_entry.get('num_citations') 
                paper_entry['doc_type'] = paper_entry.get('pub_type')
                paper_entry['keywords'] = paper_entry.get('keyword')
                
                author_name_list = [] 
                
                if paper_entry.get('author'):
                    for author_name in paper_entry['author']:
                        author_name_list.append(dict(name=author_name)) 
                
                if author_name_list:
                    paper_entry['authors'] = json.dumps(author_name_list, ensure_ascii=False).strip() 
                
                try:
                    paper_entry['date'] = datetime.strptime(paper_entry.get('pub_date'), '%Y-%m-%d')  

                    if paper_entry['date'].year <= 1900:
                        paper_entry['date'] = None 
                except Exception:
                    paper_entry['date'] = None 
                
                try:
                    paper_entry['year'] = int(paper_entry.get('pub_year'))  
                    
                    if paper_entry['year'] <= 1900: 
                        paper_entry['year'] = None 
                except Exception:
                    paper_entry['year'] = None 

                paper_result = core.create_or_update_paper(paper_entry)

                paper_id = paper_result['paper_id']
                paper_title = paper_entry.get('title')

                if paper_id and paper_title:
                    field_id_set = { field['field_zhituid'] for field in core.tag_by_title(paper_title) }

                    for field_id in field_id_set:
                        core.link_paper_and_field(
                            paper_id = paper_id, 
                            field_id = field_id, 
                        )

                    for scholar_id in scholar_id_set:
                        core.link_scholar_and_paper(
                            scholar_id = scholar_id, 
                            paper_id = paper_id, 
                        )


if __name__ == '__main__':
    main() 
