import os 
import sys 
_dir = os.path.dirname(__file__)
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

import pymongo 


def main():
    mongo_client = pymongo.MongoClient('192.168.1.221')
    mongo_collection = mongo_client.cloud_academic.wos_new1 
    
    for entry in mongo_collection.find():
        print(entry)


if __name__ == '__main__':
    main() 
