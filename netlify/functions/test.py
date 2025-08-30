def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': '<h1>Netlify Function Working!</h1><p>If you see this, the deployment is working.</p>'
    }