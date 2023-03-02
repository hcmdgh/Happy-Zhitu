import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)

import csv 
import json 
from tqdm import tqdm 
from pprint import pprint 

import jojo_es 

COUNTRY_CODE = 'UA'

EXPORT_FIELD = True 


def main():
    field_map = dict() 
    
    with open('/MAG/json/field.json', 'r', encoding='utf-8') as fp:
        for line in fp:
            field_entry = json.loads(line)
            field_id = int(field_entry['id']) 
            field_map[field_id] = field_entry 
            
    with open('/MAG/json/field_name_translation_L012.json', 'r', encoding='utf-8') as fp:
        for line in fp:
            field_entry = json.loads(line)
            field_id = int(field_entry['field_id']) 
            field_zh_name = field_entry['field_zh_name']

            field_map[field_id]['zh_name'] = field_zh_name
    
    es_client = jojo_es.ESClient(
        host = '124.205.141.242', 
        port = 10000, 
        password = '6GYZTyH6D3fR4Y',
    )
    affiliation_index = es_client.get_index('mag_affiliation')
    author_index = es_client.get_index('mag_author')
    paper_author_index = es_client.get_index('mag_paper_author_affiliation')
    paper_field_index = es_client.get_index('mag_paper_field')
    
    aff_entry_list = affiliation_index.query_X_eq_x('iso_3166_code', COUNTRY_CODE)

    aff_entry_dict = dict() 
    
    for aff_entry in aff_entry_list:
        aff_id = int(aff_entry['id'])
        aff_entry_dict[aff_id] = aff_entry
    
    author_entry_dict = dict()  
    
    for aff_entry in tqdm(aff_entry_dict.values()):
        aff_id = int(aff_entry['id'])
        author_entry_list = author_index.query_X_eq_x('last_known_affiliation_id', aff_id)

        for author_entry in author_entry_list:
            author_id = int(author_entry['id']) 
            paper_count = int(author_entry['paper_count'])
            
            if author_id not in author_entry_dict:
                if paper_count >= 10:
                    author_entry_dict[author_id] = author_entry
                    
    with open('../output/乌克兰学者.csv', 'w', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=['姓名', '机构', '论文数量', '二级领域'])
        writer.writeheader()
        
        for author_entry in tqdm(author_entry_dict.values()):
            author_id = int(author_entry['id']) 
            author_name = author_entry['display_name']
            author_aff = aff_entry_dict[author_entry['last_known_affiliation_id']]['display_name'] 
            paper_count = author_entry['paper_count']
            
            if EXPORT_FIELD:
                L2_field_name_set = set() 

                paper_author_entry_list = paper_author_index.query_X_eq_x('author_id', author_id)
                
                for paper_author_entry in paper_author_entry_list:
                    paper_id = int(paper_author_entry['paper_id'])
                    paper_field_entry_list = paper_field_index.query_X_eq_x('paper_id', paper_id) 
                    
                    for paper_field_entry in paper_field_entry_list:
                        field_id = int(paper_field_entry['field_id'])
                        field_entry = field_map[field_id]
                        
                        if field_entry['level'] == 1:
                            L2_field_name_set.add(field_entry['zh_name']) 
            else:
                L2_field_name_set = set() 

            L2_field_name_set_str = ', '.join(L2_field_name_set) 
            
            writer.writerow(
                dict(
                    姓名 = author_name, 
                    机构 = author_aff, 
                    论文数量 = paper_count, 
                    二级领域 = L2_field_name_set_str, 
                )
            )


if __name__ == '__main__':
    main() 
