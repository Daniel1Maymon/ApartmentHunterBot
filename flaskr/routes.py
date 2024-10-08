import threading
from flask import Blueprint, render_template, jsonify, request
from sqlalchemy import desc
from services.fb_scraper import run_scraper, scrape_and_store_posts, send_email_with_new_posts
from pymongo.errors import PyMongoError
from flaskr.models import post
from flaskr.models.SQL.property import Property
from flaskr.database import mySQL_db
from datetime import datetime, timedelta
from pytz import timezone
import logging


# Global lock variable
lock = threading.Lock()
is_running = False

# Create a Blueprint for routes
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

def scrape_posts():
    global is_running
    
    # Lock the code to ensure the process runs only once
    with lock:
        if is_running:
            return jsonify({"status": "error", "message": "Scraper is already running. Please wait until it finishes."}), 429

        # Mark that the scraper has started running
        is_running = True
    
    logging.info("Scraping posts...")
    try:
        scrape_and_store_posts()
        
        return jsonify({"message": "Scraping and saving posts completed"}), 200
        
    except PyMongoError as e:
        logging.ERROR(f"Database error occurred")
        return jsonify({"status": "error", "message": "Database error occurred."}), 500
    except Exception as e:
        logging.ERROR(f"500: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
    finally:
        # Release the lock when scraper finishes
        with lock:
            is_running = False
        logging.info("Scraper finished running.")

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

@bp.route("/add_post", methods=['POST'])
def add_property():
    new_property = Property(
        description='A beautiful 3-bedroom house',
        price=300000.00,
        size=120.50,
        rooms=3,
        city='givataim',
        address="Shenkin",
        url='http://example.com/property/1234',
        sent=False
    )
    
    mySQL_db.session.add(new_property)
    mySQL_db.session.commit()
    
    return f'new_property = {new_property}'

@bp.route('/print_properties')
def print_properties():
    properties = Property.query.all()

    for property in properties:
        print(f'ID: {property.id}, Description: {property.description}, Price: {property.price}')

    return "Check your console for the properties."

@bp.route('/apartments')
def index():
    return render_template('apartments.html')

@bp.route('/api/apartments')
def get_apartments():
    properties = Property.query.order_by(desc(Property.created_at)).all()
    
    apartments = [
        {
            'description': p.description,
            'address': p.address,
            'price': float(p.price) if p.price is not None else None,
            'rooms': p.rooms,
            'size': p.size,
            'phone': p.phone,
            'city': p.city,
            'url': p.url,
            'created_at': p.created_at.isoformat()
        } for p in properties
    ]
    
    for apartment in apartments:
        if apartment['created_at']:
            utc_dt = datetime.strptime(apartment['created_at'], '%Y-%m-%dT%H:%M:%S')
            israel_dt = utc_to_israel_time(utc_dt)
            apartment['created_at'] = israel_dt.strftime('%d-%m-%Y %H:%M:%S')
    return jsonify(apartments)



def utc_to_israel_time(utc_dt):
    israel_tz = timezone('Asia/Jerusalem')
    return utc_dt.replace(tzinfo=timezone('UTC')).astimezone(israel_tz)

# Define multiple endpoints for the same view function
bp.add_url_rule(rule='/', view_func=index)
bp.add_url_rule(rule='/home', view_func=index)
bp.add_url_rule(rule='/notification_setting', view_func=settings)
bp.add_url_rule(rule='/scheduling', view_func=script_scheduling)
bp.add_url_rule(rule='/links', view_func=links)
bp.add_url_rule(rule='/run_scraper', view_func=run_scraper_route, methods=['POST', 'GET'])
bp.add_url_rule(rule='/get_posts', view_func=scrape_posts, methods=['POST', 'GET'])
# bp.add_url_rule(rule='/save-schedule', view_func=save_schedule, methods=['POST'])
# bp.add_url_rule(rule='/run-task/<message>')