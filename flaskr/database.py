from flask_pymongo import PyMongo 
from flask_sqlalchemy import SQLAlchemy

print(f"\n::: _name__ = {__name__} :::\n")

# Initialize PyMongo
mongo = PyMongo()

# Initialize SQLAlchemy
mySQL_db = SQLAlchemy()

def init_app(app):
    # Bind the PyMongo instance to Flask app
    mongo.init_app(app=app)
    
    # Bind the SQLAlchemy instance to Flask app
    mySQL_db.init_app(app)