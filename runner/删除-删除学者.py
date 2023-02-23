import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

import core 

SCHOLAR_ID = 28681261240  # 庄福振
SCHOLAR_ID = 14372606192  # 王德庆


def main():
    core.delete_scholar(SCHOLAR_ID)
    
    
if __name__ == '__main__':
    main() 
