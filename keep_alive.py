from flask import Flask
import threading
import time
import requests
import os

# Keep-alive functionality for Replit
app = Flask(__name__)

@app.route('/')
def keep_alive_endpoint():
    return "Keep-alive service running!"

def run_keep_alive():
    """Run the keep-alive server on a different port"""
    app.run(host='0.0.0.0', port=8000, debug=False)

def keep_alive():
    """Start the keep-alive service"""
    server_thread = threading.Thread(target=run_keep_alive)
    server_thread.daemon = True
    server_thread.start()
    
    # Ping the main app every 5 minutes to keep it alive
    while True:
        try:
            # Get the Replit URL from environment or use localhost
            repl_url = os.environ.get('REPL_URL', 'http://localhost:5000')
            if repl_url != 'http://localhost:5000':
                requests.get(repl_url, timeout=30)
                print("Keep-alive ping sent successfully")
        except Exception as e:
            print(f"Keep-alive ping failed: {e}")
        
        # Wait 5 minutes before next ping
        time.sleep(300)
