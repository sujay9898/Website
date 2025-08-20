import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from keep_alive import keep_alive
import threading

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Sample data for portfolio (in a real app, this would come from a database)
PROJECTS = [
    {
        'title': 'E-Commerce Platform',
        'description': 'A full-stack e-commerce solution built with Flask and SQLAlchemy',
        'technologies': ['Flask', 'SQLAlchemy', 'Bootstrap', 'JavaScript'],
        'status': 'Completed'
    },
    {
        'title': 'Task Management App',
        'description': 'Collaborative task management tool with real-time updates',
        'technologies': ['Python', 'WebSockets', 'HTML5', 'CSS3'],
        'status': 'In Progress'
    },
    {
        'title': 'Data Analytics Dashboard',
        'description': 'Interactive dashboard for data visualization and analytics',
        'technologies': ['Flask', 'Chart.js', 'Pandas', 'Bootstrap'],
        'status': 'Planning'
    }
]

@app.route('/')
def index():
    """Home page route"""
    return render_template('index.html', projects=PROJECTS[:2])

@app.route('/about')
def about():
    """About page route"""
    skills = [
        {'name': 'Python', 'level': 90},
        {'name': 'Flask', 'level': 85},
        {'name': 'JavaScript', 'level': 80},
        {'name': 'HTML/CSS', 'level': 88},
        {'name': 'Bootstrap', 'level': 85},
        {'name': 'SQL', 'level': 75}
    ]
    return render_template('about.html', skills=skills)

@app.route('/portfolio')
def portfolio():
    """Portfolio page route"""
    return render_template('portfolio.html', projects=PROJECTS)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page route with form handling"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Basic validation
        if not all([name, email, subject, message]):
            flash('All fields are required!', 'error')
            return render_template('contact.html')
        
        if '@' not in email:
            flash('Please enter a valid email address!', 'error')
            return render_template('contact.html')
        
        # In a real application, you would process the form data here
        # For now, we'll just show a success message
        flash(f'Thank you {name}! Your message has been received. We\'ll get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('index.html', error="Internal server error"), 500

if __name__ == '__main__':
    # Start keep_alive in a separate thread for Replit uptime
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
