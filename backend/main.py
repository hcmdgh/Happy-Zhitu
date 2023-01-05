import sys 
sys.path.append('..')

import blueprint
import core

from flask import Flask 


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(blueprint.google_scholar.paper.bp)
    app.register_blueprint(blueprint.google_scholar.scholar.bp)
    app.register_blueprint(blueprint.zhitu.diagnose.bp)
    app.register_blueprint(blueprint.zhitu.field.bp)
    app.register_blueprint(blueprint.zhitu.org.bp)
    app.register_blueprint(blueprint.zhitu.paper.bp)
    app.register_blueprint(blueprint.zhitu.scholar.bp)
    app.register_blueprint(blueprint.zhitu.link.bp)
    
    core.init_client(flask_app=app)

    return app 


def main():
    print("Running from main()!")
    
    app = create_app()
    
    app.run(
        host = '0.0.0.0',
        port = 10000, 
        debug = False, 
    )
    

if __name__ == '__main__':
    main() 
