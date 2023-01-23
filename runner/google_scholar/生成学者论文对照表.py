import sys 
import os 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import jojo_mongo 
import jojo_es 
from tqdm import tqdm 
import json 
import traceback 


def main():
    mongo_client = jojo_mongo.MongoClient(host='192.168.0.91')
    mongo_table = mongo_client.get_collection('scholar', 'scholar_association_20230102')

    es_client = jojo_es.ESClient(host='124.205.141.242', port=9202)
    es_table = es_client.get_index('publication_copy_attributes', 'doc')
    
    with open('../output/scholar_paper_map.json', 'w', encoding='utf-8') as fp: 
        for entry in tqdm(list(mongo_table.fetch_all())):
            scholar_ggid = entry['google_id']
            scholar_ztid_list = entry['zhitu_ids']
            org_name = entry['org_name']
         
            if scholar_ztid_list:
                try:
                    paper_list = es_table.query_X_eq_x('author_id.keyword', scholar_ggid)
                except Exception:
                    traceback.print_exc()
                    
                    paper_list = [] 
                    
                if paper_list: 
                    json_str = json.dumps(
                        dict(
                            scholar_ggid = scholar_ggid, 
                            scholar_ztid_list = scholar_ztid_list, 
                            org_name = org_name, 
                            paper_list = paper_list, 
                        ),
                        ensure_ascii = False, 
                    ).strip() 
                    
                    print(json_str, file=fp)


if __name__ == '__main__':
    main() 
