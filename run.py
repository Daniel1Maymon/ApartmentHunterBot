import os, sys

if os.getenv('DOCKER_CONTAINER') is None:
    from dotenv import load_dotenv
    load_dotenv()
    os.environ['PYTHONPATH'] = os.getenv('PROJECT_PATH')

if __name__ == "__main__":
    # python run.py scraper
    if len(sys.argv) > 1 and sys.argv[1] == "scraper":
        from flaskr.scraper import run
        run()

    # python run.py
    else:
        from flaskr import create_app

        flaskr = create_app()
        # celery = make_celery(flaskr)

        flaskr.run(host='0.0.0.0', debug=False)
        # socketio.run(flaskr)
