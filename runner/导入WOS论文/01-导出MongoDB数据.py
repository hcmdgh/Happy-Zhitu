import json 
import pymongo 
from tqdm import tqdm 
import lzma 


def main():
    mongo_client = pymongo.MongoClient('192.168.1.221')
    mongo_collection = mongo_client.cloud_academic.wos_new1 
    count = mongo_collection.count_documents({})
    
    with lzma.open('/home/gh/zhitu_data/wos_2021_2022.json.xz', 'wt', encoding='utf-8') as fp:
        for entry in tqdm(mongo_collection.find(), total=count):
            json_str = json.dumps(entry, ensure_ascii=False).strip() 
            print(json_str, file=fp)


if __name__ == '__main__':
    main() 
