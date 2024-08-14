import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(import_name=__name__, instance_relative_config=True)
    
    # sets some default configuration that the app will use
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATA_BASE=os.path.join(app.instance_path, 'flask.sqlite')
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    
    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app


create_app(test_config=None)