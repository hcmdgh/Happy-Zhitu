import sys 
import os 
_dir = os.path.dirname(__file__)
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '../../submodule/package'))

from unidecode import unidecode 
from tqdm import tqdm 
import traceback

from jojo_es import * 


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
    
    new_author_index.delete_index()
    
    new_author_index.create_mapping(
        dict(
            id = ESType.KEYWORD,
            name = ESType.KEYWORD_TEXT,
            name_en = ESType.KEYWORD_TEXT,
            name_zh = ESType.KEYWORD_TEXT,
            normalized_name = ESType.KEYWORD,
            affiliation = ESType.KEYWORD_TEXT,
            normalized_affiliation = ESType.KEYWORD,
            country = ESType.KEYWORD_TEXT, 
            domain = ESType.KEYWORD_TEXT, 
        )
    )
    
    batch = [] 
    
    for author_entry in tqdm(old_author_index.scroll(scroll_size=5000), total=old_author_index.count()):
        try:
            author_id = author_entry['id'].strip() 
            name = author_entry.get('name') if author_entry.get('name') else None 
            name_en = author_entry.get('name_en') if author_entry.get('name_en') else None 
            name_zh = author_entry.get('name_zh') if author_entry.get('name_zh') else None 
            affiliation = author_entry.get('affiliation') if author_entry.get('affiliation') else None 
            country = author_entry.get('country') if author_entry.get('country') else None 
            domain = author_entry.get('domain') if author_entry.get('domain') else None 

            normalized_name_set = set() 
            
            if name:
                normalized_name_set.add(normalize_str(name))
            if name_en:
                normalized_name_set.add(normalize_str(name_en))
            if name_zh:
                normalized_name_set.add(normalize_str(name_zh))

            if affiliation:
                norm_affiliation = normalize_str(affiliation)
            else:
                norm_affiliation = None 
                
            new_author_entry = dict(
                _id = author_id, 
                id = author_id,
                name = name,
                name_en = name_en,
                name_zh = name_zh,
                normalized_name = list(normalized_name_set),
                affiliation = affiliation,
                normalized_affiliation = norm_affiliation,
                country = country, 
                domain = domain, 
            )
            batch.append(new_author_entry)
            
            if len(batch) >= 5000:
                new_author_index.bulk_insert(batch)
                batch.clear() 
        except Exception:
            traceback.print_exc()
            
    if batch:
        new_author_index.bulk_insert(batch)


if __name__ == '__main__':
    main() 
