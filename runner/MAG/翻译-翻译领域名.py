import jojo_translation 
from tqdm.auto import tqdm 
import json 


def main():
    field_id_list = []
    field_name_list = []
    
    with open('/MAG/json/field.json', 'r', encoding='utf-8') as fp:
        for line in fp:
            entry = json.loads(line)
            field_id = int(entry['id']) 
            field_name = entry['display_name'].strip() 
            field_level = int(entry['level'])
            
            if field_level > 2:
                continue 

            field_id_list.append(field_id)
            field_name_list.append(field_name)

    field_zh_name_list = jojo_translation.translate_batch_to_zh(
        source_batch = field_name_list, 
        api = 'baidu', 
        use_tqdm = True, 
    )
            
    with open('/MAG/zhitu/field_name_translation_L012.json', 'w', encoding='utf-8') as fp:
        assert len(field_id_list) == len(field_name_list) == len(field_zh_name_list)
        
        for field_id, field_name, field_zh_name in zip(field_id_list, field_name_list, field_zh_name_list):
            entry = dict(
                field_id = field_id, 
                field_name = field_name, 
                field_zh_name = field_zh_name, 
            )
            
            json_str = json.dumps(entry, ensure_ascii=False).strip() 
            print(json_str, file=fp)
            

if __name__ == '__main__':
    main() 
