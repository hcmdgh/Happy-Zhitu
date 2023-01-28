import json 
from tqdm import tqdm 
from collections import defaultdict


def main():
    scholar_field_score_map: dict[int, tuple[int, float]] = dict()
    
    with open('/MAG/zhitu/wzm/es/es_scholar_index.json', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp, total=6359_0576):
            entry = json.loads(line)
            scholar_id = int(entry['scholarId'])
            field_id = int(entry['fieldId'])
            field_level = int(entry['level'])
            score = float(entry['originIndex'])
            
            if field_level == 1:
                if scholar_id not in scholar_field_score_map:
                    scholar_field_score_map[scholar_id] = (field_id, score) 
                else:
                    if score > scholar_field_score_map[scholar_id][1]:
                        scholar_field_score_map[scholar_id] = (field_id, score)
                                    
    with open('/MAG/zhitu/wzm/es/es_scholar_index.json', 'r', encoding='utf-8') as reader_1:
        with open('/MAG/zhitu/wzm/es/es_scholar_performance_index.json', 'r', encoding='utf-8') as reader_2:
            with open('/MAG/zhitu/wzm/es/es_scholar_history_index.json', 'r', encoding='utf-8') as reader_3:
                with open('/MAG/zhitu/wzm/es/es_scholar_index_slim.json', 'w', encoding='utf-8') as writer_1:
                    with open('/MAG/zhitu/wzm/es/es_scholar_performance_index_slim.json', 'w', encoding='utf-8') as writer_2:
                        with open('/MAG/zhitu/wzm/es/es_scholar_history_index_slim.json', 'w', encoding='utf-8') as writer_3:
                            for line_1, line_2, line_3 in tqdm(zip(reader_1, reader_2, reader_3), total=6359_0576):
                                entry = json.loads(line_1)
                                scholar_id = int(entry['scholarId'])
                                field_id = int(entry['fieldId'])
                                field_level = int(entry['level'])

                                if field_level == 1:
                                    if scholar_field_score_map[scholar_id][0] != field_id:
                                        continue 
                                    
                                writer_1.write(line_1)
                                writer_2.write(line_2)
                                writer_3.write(line_3)


if __name__ == '__main__':
    main() 
