from flask import Blueprint, render_template, jsonify, request
from etc.fb_scraper import run_scraper, send_email_with_new_posts
# from models import post
from pymongo.errors import PyMongoError

from flaskr.models import post
# from .tasks import print_message

# Create a Blueprint
bp = Blueprint('main', __name__)

# Home route
# @bp.route('/', '/home')
def index():
    return render_template(template_name_or_list='home.html')

# About route
# @bp.route('/notification')
def settings():
    return render_template(template_name_or_list='settings.html')

def script_scheduling():
    return render_template(template_name_or_list='script_scheduling.html')

def links():
    return render_template(template_name_or_list='saved_links.html')

def run_scraper_route():
    try:
        # Calling the scraper function
        posts = run_scraper()
        if not posts:
            return jsonify({ "message": "No new posts found"})
        
        post.insert_posts(posts=posts)
        print("\n--------- Sending email with the new posts --------- \n")
        send_email_with_new_posts()

        return jsonify({"status": "success", "message": f"Scraper ran successfully!\n{len(posts)} new posts found\nAn email has been sent\n"})
    
    except PyMongoError as e:
        return jsonify({"status": "error", "message": "Database error occurred."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# def run_task(message):
#     task = print_message.delay(message)  # Running the Celery task asynchronously
#     return f"Task started: {task.id}"

# Define multiple endpoints for the same view function
bp.add_url_rule(rule='/', view_func=index)
bp.add_url_rule(rule='/home', view_func=index)
bp.add_url_rule(rule='/notification_setting', view_func=settings)
bp.add_url_rule(rule='/scheduling', view_func=script_scheduling)
bp.add_url_rule(rule='/links', view_func=links)
bp.add_url_rule(rule='/run_scraper', view_func=run_scraper_route, methods=['POST', 'GET'])
# bp.add_url_rule(rule='/save-schedule', view_func=save_schedule, methods=['POST'])
# bp.add_url_rule(rule='/run-task/<message>')