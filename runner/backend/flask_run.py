import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import backend 


def main():
    print("Running from main()!")
    
    app = backend.create_app()
    
    app.run(
        host = '0.0.0.0',
        port = 10000, 
        debug = True, 
    )
    
    
if __name__ == '__main__':
    main() 
