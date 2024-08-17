from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register Blueprints or routes here
    from . import routes
    app.register_blueprint(blueprint=routes.bp)

    return app
