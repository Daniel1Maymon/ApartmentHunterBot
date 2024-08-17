from flask import Blueprint, render_template

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

# Define multiple endpoints for the same view function
bp.add_url_rule('/', view_func=index)
bp.add_url_rule('/home', view_func=index)
bp.add_url_rule(rule='/notification_setting', view_func=settings)
bp.add_url_rule(rule='/scheduling', view_func=script_scheduling)
bp.add_url_rule(rule='/links', view_func=links)
