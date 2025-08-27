import json
import sys
import os

# Add the parent directory to Python path so we can import the Flask app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app import app

def handler(event, context):
    """
    Netlify function handler for Flask app
    """
    try:
        # Get the request path and method
        path = event.get('path', '/')
        method = event.get('httpMethod', 'GET')
        headers = event.get('headers', {})
        query_params = event.get('queryStringParameters') or {}
        body = event.get('body', '')
        
        # Create a test client
        with app.test_client() as client:
            # Handle the request
            if method == 'POST':
                response = client.post(path, 
                                     data=body, 
                                     headers=headers,
                                     query_string=query_params)
            elif method == 'GET':
                response = client.get(path, 
                                    headers=headers,
                                    query_string=query_params)
            else:
                response = client.open(path, 
                                     method=method,
                                     data=body,
                                     headers=headers,
                                     query_string=query_params)
            
            # Return the response
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }