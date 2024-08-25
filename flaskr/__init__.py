from flask import Flask, jsonify
from .database import init_app
import os
from dotenv import load_dotenv
from etc.fb_scraper import  get_env_path
from pymongo.errors import PyMongoError

# Load the .env file
load_dotenv(dotenv_path=get_env_path())

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config["MONGO_URI"] = os.getenv(key="MONGO_URL")

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

