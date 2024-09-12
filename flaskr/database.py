from flask_pymongo import PyMongo

print(f"\n::: _name__ = {__name__} :::\n")

# Initialize PyMongo
mongo = PyMongo()


def init_app(app):
    # Bind the PyMongo instance to Flask app
    mongo.init_app(app=app)
