import sys 
import os 
os.chdir(os.path.dirname(__file__))
sys.path.append('..')

import core

from pprint import pprint  


def main():
    res = core.tag_by_title('Modeling Dynamic Heterogeneous Graph and Node Importance for Future Citation Prediction')
    pprint(res)


if __name__ == '__main__':
    main() 
