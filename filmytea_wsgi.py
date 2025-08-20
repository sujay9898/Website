#!/usr/bin/python3.11

import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/filmytea'  # You'll need to change 'yourusername' to your actual PythonAnywhere username
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['GMAIL_APP_PASSWORD'] = 'your_gmail_app_password_here'  # You'll set this in the PythonAnywhere files section
os.environ['SESSION_SECRET'] = 'your_secret_key_here'  # You'll generate a secret key

from app import app as application

if __name__ == "__main__":
    application.run()