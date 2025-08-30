#!/usr/bin/env python3
"""
Build script for Netlify deployment
Creates static assets and prepares the app for deployment
"""

import os
import shutil
import json
from pathlib import Path

def create_dist_directory():
    """Create and populate the dist directory for deployment"""
    
    # Create dist directory
    dist_dir = Path('dist')
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    print("✓ Created dist directory")
    
    # Copy static files
    if Path('static').exists():
        shutil.copytree('static', dist_dir / 'static')
        print("✓ Copied static files")
        
        # Create a manifest for static files
        static_files = []
        for root, dirs, files in os.walk(dist_dir / 'static'):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), dist_dir)
                static_files.append(rel_path)
        
        with open(dist_dir / 'static_manifest.json', 'w') as f:
            json.dump({'static_files': static_files}, f)
        print("✓ Created static files manifest")
    
    # Copy Python files that the Flask app needs
    python_files = ['app.py', 'email_service.py', 'main.py']
    for py_file in python_files:
        if Path(py_file).exists():
            shutil.copy2(py_file, dist_dir / py_file)
            print(f"✓ Copied {py_file}")
    
    # Copy templates directory for Flask
    if Path('templates').exists():
        shutil.copytree('templates', dist_dir / 'templates')
        print("✓ Copied templates directory")
    
    # Copy JavaScript data files that the Flask app needs
    js_files = ['posters-data.js', 'posters_data.js']
    for js_file in js_files:
        if Path(js_file).exists():
            shutil.copy2(js_file, dist_dir / js_file)
            print(f"✓ Copied {js_file}")
    
    # Copy _redirects file to dist directory
    redirects_file = Path('_redirects')
    if redirects_file.exists():
        shutil.copy2(redirects_file, dist_dir / '_redirects')
        print("✓ Copied _redirects file")
    
    # Create a simple index.html fallback if it doesn't exist
    index_path = dist_dir / 'index.html'
    if not index_path.exists():
        index_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Filmytea - Movie Posters</title>
    <script>
        // Redirect to Flask app function
        window.location.href = '/.netlify/functions/app/';
    </script>
</head>
<body>
    <p>Redirecting to Filmytea...</p>
</body>
</html>'''
        with open(index_path, 'w') as f:
            f.write(index_content)
        print("✓ Created index.html fallback")
    
    print("🚀 Build completed successfully!")

if __name__ == '__main__':
    create_dist_directory()