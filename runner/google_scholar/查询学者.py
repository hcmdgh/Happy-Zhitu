import sys 
import os 
_dir = os.path.dirname(__file__)
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '../../submodule/package'))

import json 
from unidecode import unidecode 
from tqdm import tqdm 

from jojo_es import * 

SCHOLAR_COUNTRY = 'Hong Kong'


def normalize_str(s: str) -> str:
    s = unidecode(s)
    
    out = str() 
    
    for ch in s:
        if ch.isalnum():
            out += ch.lower() 
            
    out = ''.join(out.split())
    
    return out


def main():
    old_es_client = ESClient(
        host = '192.168.1.153', 
        port = 9202, 
    )
    new_es_client = ESClient(
        host = '192.168.1.219', 
        port = 9200, 
    )
    old_author_index = old_es_client.get_index('author_all_copy_attributes', 'doc')
    new_author_index = new_es_client.get_index('google_author')

    matched_cnt = 0 
    
    with open('../input/scholar_info.json', 'r', encoding='utf-8') as reader:
        with open('../output/scholar_with_google_id.json', 'w', encoding='utf-8') as writer:
            for line in tqdm(reader.readlines()):
                scholar_entry = json.loads(line)
                zhitu_id = scholar_entry['id']
                scholar_name = scholar_entry['name']
                scholar_name_2 = scholar_name[1:] + scholar_name[:1]
                scholar_org = scholar_entry['org_name']
                norm_name = normalize_str(scholar_name)
                norm_name_2 = normalize_str(scholar_name_2)
                
                author_entry_list = new_author_index.query_X_in_x_and_Y_eq_y(
                    X = 'normalized_name', 
                    x = [norm_name, norm_name_2], 
                    Y = 'country', 
                    y = SCHOLAR_COUNTRY, 
                    limit = 5, 
                )
                
                google_id_set = { author_entry['id'] for author_entry in author_entry_list }
                
                if google_id_set:
                    matched_cnt += 1
                    
                json_str = json.dumps(
                    dict(
                        zhitu_id = zhitu_id, 
                        scholar_name = scholar_name, 
                        scholar_org = scholar_org,
                        google_id_list = list(google_id_set), 
                    ),
                    ensure_ascii = False, 
                ).strip() 
                
                print(json_str, file=writer)
                    
    print(f"匹配的学者数量：{matched_cnt}")

            
if __name__ == '__main__':
    main() 
