import sys
import os


# Add the path to the project directory
sys.path.append('/mnt/c/Projects/ApartmentHunterBot')

from flaskr import create_app


'''
from flask import Flask, jsonify

from services.fb_scraper import get_env_path
from .database import init_app
import os
from dotenv import load_dotenv
# from etc.fb_scraper import  get_env_path
from pymongo.errors import PyMongoError
from pymongo import MongoClient
from .extensions import socketio  # Import socketio from extensions.py
from flask_sqlalchemy import SQLAlchemy # type: ignore

# Load the .env file
load_dotenv(dotenv_path=get_env_path())

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config["MONGO_URI"] = os.getenv(key="MONGO_URL")
    
    # Initialize MongoClient once and store it in app.config
    app.config['MONGO_CLIENT'] = MongoClient(os.getenv(key="MONGO_URL"))
    
    # Set up the MySQL database URI using environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Initialize SocketIO with the app
    # socketio.init_app(app)

    # Register Blueprints or routes here
    from . import routes
    app.register_blueprint(blueprint=routes.bp)

    # Initialize the database
    init_app(app)
    
    # Middleware to handle PyMongo exceptions
    @app.errorhandler(code_or_exception=PyMongoError)
    def handle_pymongo_error(error):
        app.logger.error(f"Database error: {error}")
        return jsonify({"status": "error", "message": "A database error occurred."}), 500

    return app
'''


app = create_app()
# celery = make_celery(app)



if __name__ == "__main__":
    
    app.run(host='0.0.0.0', debug=False)
    # socketio.run(app)