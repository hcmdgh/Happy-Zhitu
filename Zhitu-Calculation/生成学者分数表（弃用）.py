from entity import * 

import jojo_mongo as mongo 
from util import * 
from collections import defaultdict 
from typing import Any 


def build_ScholarScore_table(scholar_id_list: list[int]) -> list[ScholarScore]:
    def generate_ScholarScore_entities(scholar_id: int, 
                                       field_list: list[dict[str, Any]], 
                                       scholar: Scholar) -> list[ScholarScore]:
        scholar_score_list = [] 
                                       
        for field in field_list: 
            field_id = field['field_id']
            
            scholar_score = ScholarScore(
                _id = f"{scholar_id}-{field_id}",
                created_time = now(), 
                scholar_id = scholar_id, 
                field_id = field['field_id'], 
                field_name = field['field_name'], 
                field_level = field['field_level'], 
                priority = field['field_level'], 
                
                award_value = scholar.award_value, 
                basic_score = scholar.basic_score, 
                scholar_name = scholar.name, 
                org_id = scholar.org_id,
                org_name = scholar.org_name,
                department = scholar.department, 
                scholar_gender = scholar.gender, 
                scholar_birth_year = scholar.birth_year, 
                scholar_title = scholar.title, 
                
                original_score = 0., 
            )
            
            scholar_score_list.append(scholar_score)
        
        return scholar_score_list

    def get_scholars_by_id(scholar_id_list: list[int]) -> dict[int, Scholar]:
        scholar_list: list[Scholar] = mongo.query_X_in_x(
            collection = Scholar, 
            X = '_id', 
            x = scholar_id_list, 
        )
        
        scholar_map: dict[int, Scholar] = dict() 
        
        for scholar in scholar_list:
            scholar_id = int(scholar._id)
            scholar_map[scholar_id] = scholar 

        return scholar_map 
        
    publish_list: list[ScholarPublish] = mongo.query_X_in_x(
        collection = ScholarPublish, 
        X = 'scholar_id', 
        x = scholar_id_list, 
    )
    
    scholar_field_map: dict[int, list[int]] = defaultdict(list)
    field_map: dict[int, dict[str, Any]] = dict() 

    for publish in publish_list:
        scholar_id = int(publish.scholar_id) 
        field_list = publish.field_list if publish.field_list else [] 
        
        for field in field_list:
            field_id = field['field_id']
            
            field_map[field_id] = field 
            scholar_field_map[scholar_id].append(field_id)
        
    scholar_map: dict[int, Scholar] = get_scholars_by_id(scholar_id_list)

    scholar_score_list: list[ScholarScore] = []
        
    for scholar_id in scholar_id_list:
        scholar = scholar_map[scholar_id]
        field_id_list = scholar_field_map[scholar_id]

        L1_field_count_map: dict[int, int] = defaultdict(int)
        L2_field_count_map: dict[int, int] = defaultdict(int)
        L3_field_count_map: dict[int, int] = defaultdict(int)

        for field_id in field_id_list: 
            field_level = field_map[field_id]['field_level']

            if field_level == 1:
                L1_field_count_map[field_id] += 1 
            elif field_level == 2: 
                L2_field_count_map[field_id] += 1 
            elif field_level == 3: 
                L3_field_count_map[field_id] += 1 
            else:
                raise AssertionError 
        
        # 按学者1级领域的数量降序排序，取出现次数最多的1个领域
        if True:
            entries = sorted(list(L1_field_count_map.items()), key=lambda x: -x[1]) 
            filtered_L1_field_ids: set[int] = { entry[0] for entry in entries[:1] }

            scholar_score_list.extend(
                generate_ScholarScore_entities(
                    scholar_id = scholar_id, 
                    field_list = [field_map[field_id] for field_id in filtered_L1_field_ids], 
                    scholar = scholar, 
                )
            )

        # 按学者2级领域的数量降序排序，取出现次数最多的3个领域
        if True:
            entries = sorted(list(L2_field_count_map.items()), key=lambda x: -x[1]) 
            filtered_L2_field_ids: set[int] = { entry[0] for entry in entries[:3] }

            scholar_score_list.extend(
                generate_ScholarScore_entities(
                    scholar_id = scholar_id, 
                    field_list = [field_map[field_id] for field_id in filtered_L2_field_ids], 
                    scholar = scholar, 
                )
            )

        # 按学者3级领域的数量降序排序，取出现次数最多的5个领域
        if True:
            entries = sorted(list(L3_field_count_map.items()), key=lambda x: -x[1]) 
            filtered_L3_field_ids: set[int] = { entry[0] for entry in entries[:5] }

            scholar_score_list.extend(
                generate_ScholarScore_entities(
                    scholar_id = scholar_id, 
                    field_list = [field_map[field_id] for field_id in filtered_L3_field_ids], 
                    scholar = scholar, 
                )
            )

    mongo.insert_many(scholar_score_list)
            
    return scholar_score_list


def main():
    pass 


if __name__ == '__main__':
    main() 
