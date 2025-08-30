import json
import sys
import os
from urllib.parse import unquote

# Add the parent directory to Python path so we can import the Flask app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Load environment variables from .env file if it exists
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                try:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
                except ValueError:
                    pass

# Import Flask app with error handling
try:
    from app import app
except ImportError as e:
    print(f"Import error: {e}")
    # Create a simple Flask app as fallback
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return f"Import Error: {str(e)}. Check function deployment."

def handler(event, context):
    """
    Netlify function handler for Flask app
    """
    try:
        # Get the request path and method
        raw_path = event.get('path', '/')
        method = event.get('httpMethod', 'GET')
        headers = event.get('headers', {})
        query_params = event.get('queryStringParameters') or {}
        body = event.get('body', '')
        is_base64 = event.get('isBase64Encoded', False)
        
        # Clean the path - remove function prefix if present
        path = raw_path
        if path.startswith('/.netlify/functions/app'):
            path = path[len('/.netlify/functions/app'):]
        if not path:
            path = '/'
        
        # Decode URL encoding
        path = unquote(path)
        
        # Handle form data for POST requests
        if method == 'POST' and body:
            if is_base64:
                import base64
                body = base64.b64decode(body).decode('utf-8')
        
        # Set up Flask app context
        with app.test_request_context(path=path, method=method, headers=headers, query_string=query_params, data=body):
            # Create a test client
            with app.test_client() as client:
                # Handle the request
                if method == 'POST':
                    content_type = headers.get('content-type', '')
                    if 'application/x-www-form-urlencoded' in content_type:
                        response = client.post(path, data=body, headers=headers, query_string=query_params)
                    elif 'application/json' in content_type:
                        response = client.post(path, json=json.loads(body) if body else {}, headers=headers, query_string=query_params)
                    else:
                        response = client.post(path, data=body, headers=headers, query_string=query_params)
                elif method == 'GET':
                    response = client.get(path, headers=headers, query_string=query_params)
                else:
                    response = client.open(path, method=method, data=body, headers=headers, query_string=query_params)
                
                # Prepare response headers
                response_headers = dict(response.headers)
                
                # Handle CORS for API requests
                if path.startswith('/api/'):
                    response_headers['Access-Control-Allow-Origin'] = '*'
                    response_headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                    response_headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                
                # Return the response
                return {
                    'statusCode': response.status_code,
                    'headers': response_headers,
                    'body': response.get_data(as_text=True)
                }
                
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e), 'type': type(e).__name__})
        }