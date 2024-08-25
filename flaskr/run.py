import sys
import os

# Add the path to the project directory
sys.path.append('/mnt/c/Projects/ApartmentHunterBot')

from flaskr import create_app


app = create_app()

if __name__ == "__main__":
    app.run()