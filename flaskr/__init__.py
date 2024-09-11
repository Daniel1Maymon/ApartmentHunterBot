from celery import Celery # type: ignore
from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os

from flaskr.database import init_app
from flaskr.extensions import socketio # Import socketio from extensions.py

# Celery configuration
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=os.getenv("MONGO_URL"),  # Using Redis as backend
        broker=os.getenv("MONGO_URL")    # Using Redis as broker
    )

    celery.conf.update(app.config)
    return celery

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config["MONGO_URI"] = os.getenv("MONGO_URL")

    # Initialize MongoClient once and store it in app.config
    app.config['MONGO_CLIENT'] = MongoClient(os.getenv("MONGO_URL"))

    # Initialize SocketIO with the app
    # socketio.init_app(app)

    # Register Blueprints or routes here
    from flaskr import routes
    app.register_blueprint(blueprint=routes.bp)

    # Initialize the database
    init_app(app)

    # Middleware to handle PyMongo exceptions
    @app.errorhandler(code_or_exception=PyMongoError)
    def handle_pymongo_error(error):
        app.logger.error(f"Database error: {error}")
        return jsonify({"status": "error", "message": "A database error occurred."}), 500

    return app
