import sys
import os


# Add the path to the project directory
sys.path.append('/mnt/c/Projects/ApartmentHunterBot')

from flaskr import create_app


app = create_app()

# from flaskr.extensions import socketio  # Import socketio from extensions.py

if __name__ == "__main__":
    app.run()
    # socketio.run(app)