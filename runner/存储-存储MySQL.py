import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '../submodule/package'))

import jojo_mysql 
import csv 
from tqdm import tqdm 

CSV_PATH = './input/award2.csv'
DATABASE_NAME = 'GengHao'
TABLE_NAME = '20230215_provincial_award'
TABLE_SCHEMA = f"""
    CREATE TABLE {DATABASE_NAME}.{TABLE_NAME} (
        id BIGINT AUTO_INCREMENT PRIMARY KEY, 
        project_title TEXT, 
        project_title_E TEXT, 
        leader TEXT,
        org TEXT,
        award_type TEXT,
        year INT,
        award TEXT,
        award_number TEXT,
        nominating_org TEXT,
        region TEXT,
        title TEXT, 
        
        field_l1 TEXT,
        field_l2 TEXT,
        field_l3 TEXT,
        field_l1_id TEXT,
        field_l2_id TEXT,
        field_l3_id TEXT,
        finished INT DEFAULT 0
    );
"""


def main():
    mysql_client = jojo_mysql.MySQLClient(
        host = '192.168.0.84', 
        port = 3306, 
        user = 'root', 
        password = 'root', 
    )
    mysql_table = mysql_client.get_table(DATABASE_NAME, TABLE_NAME)
    mysql_table.drop_table()
    
    mysql_table.cursor.execute(TABLE_SCHEMA)
    
    with open(CSV_PATH, 'r', encoding='utf-8') as fp:
        reader = csv.DictReader(fp)
        
        for row in tqdm(list(reader)):
            mysql_table.insert_one(row)


if __name__ == '__main__':
    main() 
