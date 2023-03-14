import sys 
import os 
_dir = os.path.dirname(__file__)
os.chdir(_dir)
sys.path.append(os.path.join(_dir, '../..'))
sys.path.append(os.path.join(_dir, '../../submodule/package'))

import json 
from unidecode import unidecode 
from tqdm import tqdm 

from jojo_es import * 

import core 


def main():
    pass 


if __name__ == '__main__':
    main() 
