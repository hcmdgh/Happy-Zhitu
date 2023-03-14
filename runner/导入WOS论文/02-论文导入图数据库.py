import json 
import lzma 
from tqdm import tqdm 
from datetime import datetime 
from typing import Optional, Any 

import jojo_janusgraph 

INPUT_PATH = '/mnt/GengHao/zhitu-data/WOS-20212022/raw.json.xz'
OUTPUT_PATH = '/mnt/GengHao/zhitu-data/WOS-20212022/graph_database.json.xz'
COUNT = 198_5198

graph_client = jojo_janusgraph.JanusGraphClient(url='ws://192.168.0.83:8182/gremlin')


def normalize_title(title: str) -> str:
    out = str() 
    
    for ch in title:
        if ch.isalnum():
            out += ch.lower() 
        else:
            out += ' '
            
    out = ' '.join(out.split())
    
    return out 


def convert_wos_paper_entry_to_zhitu(wos_paper_entry: dict[str, Any]) -> dict[str, Any]:
    zhitu_paper_entry = dict(wos_paper_entry)
    
    zhitu_paper_entry['mongo_id'] = zhitu_paper_entry.pop('_id', None) 
    
    try:
        author_entry_list = [] 
        
        for author_entry in zhitu_paper_entry['author_organ']:
            author_name = author_entry['name']
            author_org = author_entry['org']
            
            author_entry_list.append(
                dict(
                    name = author_name, 
                    org = author_org, 
                )
            )
    except Exception:
        author_entry_list = []
        
    zhitu_paper_entry['authors'] = json.dumps(author_entry_list, ensure_ascii=False).strip() 
    
    try:
        date_ = datetime.strptime(zhitu_paper_entry['collection_date'], '%Y-%m-%d')
    except Exception:
        date_ = None 
        
    zhitu_paper_entry['date'] = date_ 
    
    zhitu_paper_entry['doc_type'] = 'wos'
    
    zhitu_paper_entry['keywords'] = zhitu_paper_entry.get('keyword')
    
    zhitu_paper_entry['lang'] = 'en'
    
    try:
        seps = zhitu_paper_entry['se_pages'].split('-')
        page_start = seps[0]
        page_end = seps[1]
    except Exception:
        page_start = page_end = None 
        
    zhitu_paper_entry['page_start'] = page_start
    zhitu_paper_entry['page_end'] = page_end
    
    zhitu_paper_entry['paper_title'] = zhitu_paper_entry.get('title')
    
    try:
        norm_title = normalize_title(zhitu_paper_entry['paper_title']) 
    except Exception:
        norm_title = None     
    
    zhitu_paper_entry['paper_title_lowercase'] = norm_title 
    
    zhitu_paper_entry['venue'] = zhitu_paper_entry.get('venue')
    
    zhitu_paper_entry['volume'] = zhitu_paper_entry.get('volume')
    
    try:
        year = int(zhitu_paper_entry['year'])
    except Exception:
        year = None 
        
    zhitu_paper_entry['year'] = year 
    
    return zhitu_paper_entry


def query_paper_by_title(title: str) -> set[int]:
    paper_id_set: set[int] = set()

    paper_id_set.update(
        graph_client.query_vertex_by_prop(
            label = 'Paper', 
            prop_name = 'paper_title_lowercase', 
            prop_val = title, 
        )
    )
    
    paper_id_set.update(
        graph_client.query_vertex_by_prop(
            label = 'Paper', 
            prop_name = 'paper_title_lowercase', 
            prop_val = normalize_title(title), 
        )
    )
    
    return paper_id_set 
    

def main():
    with lzma.open(INPUT_PATH, 'rt', encoding='utf-8') as reader, \
         lzma.open(OUTPUT_PATH, 'wt', encoding='utf-8') as writer:
        for line in tqdm(reader, total=COUNT):
            wos_paper_entry = json.loads(line) 
            
            zhitu_paper_entry = convert_wos_paper_entry_to_zhitu(wos_paper_entry)
            
            paper_title = zhitu_paper_entry.get('paper_title')
            
            if not paper_title:
                print(f"论文标题不存在：{wos_paper_entry}")
                continue 
            
            exist_paper_id_set = query_paper_by_title(paper_title)
            
            if exist_paper_id_set:
                paper_id = exist_paper_id_set.pop() 
                
                graph_client.update_vertex(
                    vid = paper_id, 
                    prop_dict = zhitu_paper_entry, 
                )
            else:
                paper_id = graph_client.create_vertex(
                    v_label = 'Paper',
                    prop_dict = zhitu_paper_entry,
                )
            
            zhitu_paper_entry['zhitu_id'] = paper_id 
            
            json_str = json.dumps(zhitu_paper_entry, ensure_ascii=False).strip() 
            print(json_str, file=writer)
            

if __name__ == '__main__':
    main() 
