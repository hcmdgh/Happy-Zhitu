import sys 
import os 
os.chdir(os.path.dirname(__file__))
sys.path.append('..')

import core 

from tqdm.auto import tqdm 


def main():
    core.init_client()
    mysql_client = core.get_mysql_client() 
    table = mysql_client.get_table('dump', 'scholar_basic')
    mongo_client = core.get_mongo_client()
    collection = mongo_client.get_collection('zhitu', 'scholar_name_pinyin_map')

    collection.drop() 
    collection.create_index('id', 'name', 'norm_name', 'org', 'norm_org', 'pinyin_list', 'name_pinyin_list', 'update_time')

    for scholar_entry in tqdm(table.scan_table(batch_size=10000), total=4060_0954):
        try:
            scholar_id = int(scholar_entry['id']) 
            scholar_name = scholar_entry['name'].strip() 
            scholar_org = scholar_entry['org_name'].strip() 
        except Exception:
            continue 
        
        norm_name = core.normalize_str(scholar_name, keep_space=False)
        norm_org = core.normalize_str(scholar_org, keep_space=False)
        
        pinyin_set = {
            core.convert_name_to_pinyin_1(scholar_name),
            core.convert_name_to_pinyin_2(scholar_name),
        }    
        
        name_pinyin_set = {
            scholar_name, 
            norm_name, 
            *pinyin_set, 
        }
        
        collection.insert_one(
            dict(
                _id = scholar_id, 
                id = scholar_id, 
                name = scholar_name, 
                norm_name = norm_name, 
                org = scholar_org, 
                norm_org = norm_org, 
                pinyin_list = list(pinyin_set), 
                name_pinyin_list = list(name_pinyin_set),
                updated_time = core.get_now_date_str(), 
            ),
            ignore_duplicate = True, 
        )
        
    
if __name__ == '__main__':
    main() 
