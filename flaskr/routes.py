from flask import Blueprint, render_template, request, redirect, url_for, flash

# Create a Blueprint
bp = Blueprint('main', __name__)

# Home route
@bp.route('/')
def index():
    return render_template('index.html')


# About route
@bp.route('/about')
def about():
    return render_template('about.html')


# Example of handling a form submission
@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        flash(f'Thank you, {name}!', 'success')
        return redirect(url_for('main.index'))
    return render_template('submit.html')


# Error handling
@bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404