import sys 
import os 
_dir = os.path.realpath(os.path.dirname(__file__))
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '..'))

import core 

TITLE = '高效清洁能量转换材料的设计、性能及机理研究'


def main():
    core.query_paper_by_title(
        title = TITLE, 
        source = 'JanusGraph', 
    )


if __name__ == '__main__':
    main() 
