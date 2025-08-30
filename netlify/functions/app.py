import json
import sys
import os
from urllib.parse import unquote

# Add the dist directory to Python path so we can import the Flask app
dist_path = os.path.join(os.path.dirname(__file__), '..', '..', 'dist')
sys.path.insert(0, dist_path)

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

# Also try loading environment from the current directory
current_env_path = os.path.join(os.getcwd(), '.env')
if os.path.exists(current_env_path):
    with open(current_env_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                try:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
                except ValueError:
                    pass

# Import Flask app with better error handling
try:
    # Change working directory to dist for proper file access
    os.chdir(dist_path)
    from app import app
    print("Successfully imported Flask app from dist directory")
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    print(f"Dist path: {dist_path}")
    print(f"Dist path exists: {os.path.exists(dist_path)}")
    if os.path.exists(dist_path):
        print(f"Files in dist: {os.listdir(dist_path)}")
    
    # Create a simple Flask app as fallback
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    @app.route('/<path:path>')
    def debug_info(path=''):
        import traceback
        debug_content = f"""
        <h1>Netlify Function Debug Info</h1>
        <h2>Import Error:</h2>
        <pre>{str(e)}</pre>
        <h2>Current Directory:</h2>
        <pre>{os.getcwd()}</pre>
        <h2>Dist Path:</h2>
        <pre>{dist_path}</pre>
        <h2>Dist Path Exists:</h2>
        <pre>{os.path.exists(dist_path)}</pre>
        """
        
        if os.path.exists(dist_path):
            debug_content += f"""
        <h2>Files in Dist:</h2>
        <pre>{os.listdir(dist_path)}</pre>
            """
        
        debug_content += f"""
        <h2>Files Available (current dir):</h2>
        <pre>{str(os.listdir('.'))}</pre>
        <h2>Python Path:</h2>
        <pre>{chr(10).join(sys.path)}</pre>
        <h2>Environment Variables:</h2>
        <pre>{chr(10).join([f'{k}={v}' for k, v in os.environ.items() if 'PATH' in k or 'PYTHON' in k])}</pre>
        <h2>Traceback:</h2>
        <pre>{traceback.format_exc()}</pre>
        """
        return debug_content

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