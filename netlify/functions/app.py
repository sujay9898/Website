import json
import sys
import os
from urllib.parse import unquote

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

# Import all the required modules for Flask app
import logging
from flask import Flask, render_template, abort, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Import email service from same directory
from email_service import send_order_confirmation_email

try:
    from instamojo_wrapper import Instamojo
except ImportError:
    Instamojo = None

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get("SESSION_SECRET", "dummy-secret-key-for-development-123")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database, relative to the app instance folder
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
else:
    # Fallback for development without database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

# Environment-based logging
log_level = logging.DEBUG if os.environ.get('FLASK_ENV') == 'development' else logging.INFO
logging.basicConfig(level=log_level)

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Cache static files
@app.after_request
def add_cache_headers(response):
    if request.endpoint == 'static':
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

with app.app_context():
    # Create tables if needed (only if database is available)
    try:
        db.create_all()
    except Exception as e:
        logging.warning(f"Database not available during startup: {e}")

# Initialize Instamojo
api_key = os.environ.get("INSTAMOJO_API_KEY")
auth_token = os.environ.get("INSTAMOJO_AUTH_TOKEN")

if api_key and auth_token and Instamojo:
    instamojo_api = Instamojo(
        api_key=api_key,
        auth_token=auth_token,
        endpoint='https://www.instamojo.com/api/1.1/'
    )
else:
    instamojo_api = None
    logging.warning("Instamojo credentials not configured")

# Poster data - prices from individual items not used (pricing handled by cart.js)
ALL_POSTERS = [
    {
        'id': 'poster_1',
        'name': 'Smoking Chills Red',
        'price': 299,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676740/Smoking_Chills_Red_text_s93bz4.jpg'
    },
    {
        'id': 'poster_2',
        'name': 'Smoking Chills Yellow',
        'price': 299,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676731/Smoking_Chills_Yellow_text_okjrri.jpg'
    },
    {
        'id': 'poster_3',
        'name': 'Virat 100',
        'price': 249,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676728/Virat_100_gp0dgr.jpg'
    },
    {
        'id': 'poster_4',
        'name': 'Vikram Card Blue',
        'price': 279,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676728/Vikram_Card_Blue_cjpnn9.jpg'
    },
    {
        'id': 'poster_5',
        'name': 'Vada Chennai Sayings',
        'price': 199,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676727/Vada_Chennai_-_Sayings_qnltbs.jpg'
    },
    {
        'id': 'poster_6',
        'name': 'Yuvan Cassette',
        'price': 229,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676727/Yuvan_-_Cassette_nocxfj.jpg'
    },
    {
        'id': 'poster_7',
        'name': 'You Smell Like Love',
        'price': 259,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676725/You_smell_like_love_xyhnmy.jpg'
    },
    {
        'id': 'poster_8',
        'name': 'Vikram Card Red',
        'price': 279,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676723/Vikram_Card_Red_rwezuv.jpg'
    },
    {
        'id': 'poster_9',
        'name': 'Ten Incarnations Chocolate',
        'price': 189,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676723/The_ten_Incarnations_Chocolate_bpl64o.jpg'
    },
    {
        'id': 'poster_10',
        'name': 'Ten Incarnations Red',
        'price': 189,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676723/The_ten_Incarnations_Red_bqifuf.jpg'
    },
    {
        'id': 'poster_11',
        'name': 'Vaaranam Aayiram Sayings',
        'price': 219,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676719/Vaaranam_Aayiram_-_Sayings_wy0lp8.jpg'
    },
    {
        'id': 'poster_12',
        'name': 'Ten Incarnations Blue',
        'price': 189,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676719/The_ten_Incarnations_Blue_m9nmru.jpg'
    },
    {
        'id': 'poster_13',
        'name': 'TK Alien',
        'price': 249,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676718/TK_-_Alien_vrd8yr.jpg'
    },
    {
        'id': 'poster_14',
        'name': 'Pulp Fiction ft Rai',
        'price': 299,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676715/Plup_Fiction_-_Ft_Rai_a02jvj.jpg'
    },
    {
        'id': 'poster_15',
        'name': 'Super Deluxe Mysskin Sayings',
        'price': 239,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676715/Super_Deluxe_Mysskin_-_Sayings_ztytaj.jpg'
    },
    {
        'id': 'poster_16',
        'name': 'Super Deluxe Intro Sayings',
        'price': 239,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676715/Super_Deluxe_Intro_-_Sayings_he2bja.jpg'
    },
    {
        'id': 'poster_17',
        'name': 'Soorarai Pottru Sayings',
        'price': 199,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676715/Soorarai_Pottru_-_Sayings_hhfupo.jpg'
    },
    {
        'id': 'poster_18',
        'name': 'Super Deluxe Quotes',
        'price': 239,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676713/Super_Deluxe_-_Quotes_nzuzmc.jpg'
    },
    {
        'id': 'poster_19',
        'name': 'Minnale Pink',
        'price': 209,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676712/Minnale_Pink_cacsxj.jpg'
    },
    {
        'id': 'poster_20',
        'name': 'Sarpatta Parambarai Sayings',
        'price': 219,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676711/Sarpatta_Parambarai_-_Sayings_icrquf.jpg'
    },
    {
        'id': 'poster_21',
        'name': 'Minnale Olive',
        'price': 209,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676710/Minnale_Olive_bgkkea.jpg'
    },
    {
        'id': 'poster_22',
        'name': 'Leo Blood',
        'price': 329,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676710/Leo_Blood_hozq47.jpg'
    },
    {
        'id': 'poster_23',
        'name': 'Rise of Anbu',
        'price': 259,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676709/Rise_of_Anbu_jvpvj8.jpg'
    },
    {
        'id': 'poster_24',
        'name': 'Sarpatta Parambarai Quotes',
        'price': 219,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676709/Sarpatta_Parambarai_-_Quotes_yjvjpn.jpg'
    },
    {
        'id': 'poster_25',
        'name': 'Minnale Dark Blue',
        'price': 209,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676708/Minnale_Dark_Blue_tdwzhn.jpg'
    },
    {
        'id': 'poster_26',
        'name': 'Leo Yellow',
        'price': 329,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676705/Leo_yellow_dvl4t6.jpg'
    },
    {
        'id': 'poster_27',
        'name': 'Meiyazhagan Cassette',
        'price': 189,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676704/Meiyazhagan_-_Cassette_ljj4cz.jpg'
    },
    {
        'id': 'poster_28',
        'name': 'Leo Red',
        'price': 329,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676703/Leo_Red_qchqtw.jpg'
    },
    {
        'id': 'poster_29',
        'name': 'Meiyazhagan Quotes',
        'price': 189,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676702/Meiyazhagan_-_Quotes_gufnkb.jpg'
    },
    {
        'id': 'poster_30',
        'name': 'Leo Biscuit',
        'price': 329,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676700/Leo_Biscuit_gydv8g.jpg'
    },
    {
        'id': 'poster_31',
        'name': 'Johnny Typography',
        'price': 199,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676699/Johnny_-_Typography_zaffhc.jpg'
    },
    {
        'id': 'poster_32',
        'name': 'KH Cassette Red',
        'price': 229,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676699/KH-Cassette_Red_vrnqyp.jpg'
    },
    {
        'id': 'poster_33',
        'name': 'Kendrick Lamar Blue',
        'price': 249,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676698/Kendrick_Lamar_Blue_csvkms.jpg'
    },
    {
        'id': 'poster_34',
        'name': 'KH Cassette Olive',
        'price': 229,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676698/KH-Cassette_Olive_nrzvo6.jpg'
    },
    {
        'id': 'poster_35',
        'name': 'Kendrick Lamar Red',
        'price': 249,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676698/Kendrick_Lamar_Red_tuwave.jpg'
    },
    {
        'id': 'poster_36',
        'name': 'Anbe Sivam Sayings',
        'price': 179,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676697/Anbe_Sivam_-_Sayings_pvw8d9.jpg'
    },
    {
        'id': 'poster_37',
        'name': 'Billa AK',
        'price': 259,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676695/Billa_-_AK_vgrlzd.jpg'
    },
    {
        'id': 'poster_38',
        'name': 'Tale of Kutti and Rukku',
        'price': 199,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676694/A_Tale_of_Kutti_and_Rukku_neciqt.jpg'
    },
    {
        'id': 'poster_39',
        'name': 'Hey Ram Sayings',
        'price': 179,
        'image_url': 'https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676694/Hey_Ram_-_Sayings_d9ixlb.jpg'
    }
]


@app.route('/')
def index():
    """Homepage with posters button"""
    return render_template('index.html')


@app.route('/posters')
def posters():
    """Posters page displaying all posters"""
    return render_template('posters.html', posters=ALL_POSTERS)


@app.route('/poster/<poster_id>')
def poster_detail(poster_id):
    """Individual poster details page"""
    poster = None
    for p in ALL_POSTERS:
        if p['id'] == poster_id:
            poster = p
            break
    
    if not poster:
        abort(404)
    
    return render_template('poster_detail.html', poster=poster)


@app.route('/cart')
def cart():
    """Cart page displaying items from localStorage"""
    return render_template('cart.html')


@app.route('/checkout')
def checkout():
    """Checkout page for order processing"""
    return render_template('checkout.html')


@app.route('/process-order', methods=['POST'])
def process_order():
    """Show order preview with customer details and edit options"""
    # Collect order details from form (simulating the input() calls from the Python code)
    order = {}
    order['Customer Name'] = request.form.get('customer_name')
    # Shipping Address section
    order['Address'] = request.form.get('address')
    order['Pincode'] = request.form.get('pincode')
    order['City'] = request.form.get('city')
    order['State'] = request.form.get('state')
    order['Phone Number'] = request.form.get('phone_number')
    order['Email'] = request.form.get('email')
    order['Cash on Delivery'] = request.form.get('cash_on_delivery')
    
    return render_template('order_preview.html', order=order)

@app.route('/confirm-order', methods=['POST'])
def confirm_order():
    """Final order confirmation after preview"""
    # Collect order details from form again
    order = {}
    order['Customer Name'] = request.form.get('customer_name')
    order['Address'] = request.form.get('address')
    order['Pincode'] = request.form.get('pincode')
    order['City'] = request.form.get('city')
    order['State'] = request.form.get('state')
    order['Phone Number'] = request.form.get('phone_number')
    order['Email'] = request.form.get('email')
    order['Cash on Delivery'] = request.form.get('cash_on_delivery')
    
    # Get cart items from the hidden form field
    cart_items_json = request.form.get('cart_items', '[]')
    try:
        cart_items = json.loads(cart_items_json)
    except:
        cart_items = []
    
    # Exact output as in the Python code
    print("Order captured successfully! Here are the details:")
    print()
    for key, value in order.items():
        print(f"{key}: {value}")
    
    # Also log to application logger
    logging.info("Order captured successfully! Here are the details:")
    for key, value in order.items():
        logging.info(f"{key}: {value}")
    
    # Send order confirmation email immediately
    order_id = None
    if order.get('Email'):
        try:
            order_id = send_order_confirmation_email(order, cart_items)
            if order_id:
                logging.info(f"Order confirmation email sent successfully to {order['Email']}")
                logging.info(f"Order ID: {order_id}")
        except Exception as e:
            logging.error(f"Failed to send order confirmation email: {e}")
            order_id = "EMAIL_FAILED"
    
    # Render success page with order details and cart items
    emailjs_public_key = os.environ.get('EMAILJS_PUBLIC_KEY', '')
    return render_template('order_success.html', 
                         order=order, 
                         order_id=order_id, 
                         cart_items=cart_items,
                         emailjs_public_key=emailjs_public_key)

@app.route('/email-test')
def email_test():
    # EmailJS configuration for testing
    emailjs_public_key = os.environ.get('EMAILJS_PUBLIC_KEY', '')
    return render_template('email_test.html', emailjs_public_key=emailjs_public_key)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500

# API endpoint for poster search
@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    results = [poster for poster in ALL_POSTERS 
              if query in poster['name'].lower()]
    return jsonify(results[:10])  # Limit to 10 results

@app.route('/create-payment', methods=['POST'])
def create_payment():
    """Create Instamojo payment or fallback to dummy system"""
    try:
        # Get order details from form
        customer_name = request.form.get('customer_name')
        email = request.form.get('email')
        phone = request.form.get('phone_number')
        cart_total = float(request.form.get('cart_total', 0))
        
        # Get cart items and sanitize them
        cart_items_json = request.form.get('cart_items', '[]')
        try:
            cart_items = json.loads(cart_items_json)
            # Sanitize cart items to remove any undefined values
            sanitized_cart_items = []
            for item in cart_items:
                if isinstance(item, dict):
                    sanitized_item = {}
                    for key, value in item.items():
                        # Skip undefined/null values or replace with defaults
                        if value is not None and str(value).lower() != 'undefined':
                            sanitized_item[key] = value
                        elif key == 'frameText':
                            sanitized_item[key] = 'No Frame'
                        elif key == 'quantity':
                            sanitized_item[key] = 1
                        elif key == 'price':
                            sanitized_item[key] = 159
                    # Only add items with required fields
                    if 'name' in sanitized_item and 'price' in sanitized_item:
                        sanitized_cart_items.append(sanitized_item)
            cart_items = sanitized_cart_items
        except Exception as e:
            logging.error(f"Error parsing cart items: {e}")
            cart_items = []
        
        # If Instamojo is available and configured, use it
        if instamojo_api:
            # Create payment request
            payment_request = instamojo_api.payment_request_create(
                amount=cart_total,
                purpose=f'Filmytea Poster Order - {customer_name}',
                buyer_name=customer_name,
                email=email,
                phone=phone,
                redirect_url=request.host_url + 'order-success.html',
                send_email=False,
                webhook=request.host_url + 'webhook'
            )
            
            if payment_request['success']:
                payment_url = payment_request['payment_request']['longurl']
                return redirect(payment_url)
            else:
                logging.error(f"Instamojo payment creation failed: {payment_request}")
                # Fall through to dummy payment
        
        # Dummy payment system fallback
        return render_template('dummy_payment.html',
                             customer_name=customer_name,
                             email=email,
                             phone=phone,
                             cart_total=cart_total,
                             cart_items=cart_items)
    
    except Exception as e:
        logging.error(f"Payment creation error: {e}")
        return render_template('error.html', 
                             error_code=500, 
                             error_message="Payment processing error"), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle Instamojo payment webhook"""
    if instamojo_api:
        mac_provided = request.form.get('mac')
        payment_id = request.form.get('payment_id')
        
        # Verify the payment
        payment_details = instamojo_api.payment_detail(
            payment_id=payment_id
        )
        
        if payment_details['success']:
            # Payment successful, handle order processing
            logging.info(f"Payment successful for payment_id: {payment_id}")
            return "OK", 200
        else:
            logging.error(f"Payment verification failed for payment_id: {payment_id}")
            return "Failed", 400
    
    return "Webhook not configured", 400

# Keep alive service (for Replit deployment)
def keep_alive():
    """Minimal keep-alive service to prevent hibernation"""
    import threading
    import time
    import requests
    
    def ping_self():
        try:
            repl_url = os.environ.get('REPL_URL')
            if repl_url:
                requests.get(f"{repl_url}/")
        except:
            pass  # Ignore errors in keep-alive
    
    def background_task():
        while True:
            time.sleep(300)  # 5 minutes
            ping_self()
    
    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()

# Start keep-alive service if running on Replit
if os.environ.get('REPL_URL'):
    keep_alive()

# Netlify serverless function handler
def handler(event, context):
    """Netlify function handler"""
    try:
        # Get request information
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        query_params = event.get('queryStringParameters') or {}
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        # Clean up the path - remove function prefix
        if path.startswith('/.netlify/functions/app'):
            path = path.replace('/.netlify/functions/app', '') or '/'
        
        # Handle URL decoding
        path = unquote(path)
        
        # Create Flask test environment
        environ_base = {
            'REQUEST_METHOD': http_method,
            'PATH_INFO': path,
            'QUERY_STRING': '&'.join([f"{k}={v}" for k, v in query_params.items() if v]),
            'CONTENT_TYPE': headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body)) if body else '0',
            'HTTP_HOST': headers.get('host', 'localhost'),
            'wsgi.url_scheme': 'https'
        }
        
        # Add other headers with HTTP_ prefix
        for header_name, header_value in headers.items():
            if header_name.lower() not in ['content-type', 'content-length', 'host']:
                environ_key = f"HTTP_{header_name.upper().replace('-', '_')}"
                environ_base[environ_key] = header_value
        
        # Create WSGI environment
        from werkzeug.test import EnvironBuilder
        builder = EnvironBuilder(
            path=path,
            method=http_method,
            data=body,
            query_string=environ_base['QUERY_STRING'],
            headers=headers
        )
        
        # Get response from Flask app
        with app.test_client() as client:
            if http_method == 'POST':
                if 'application/json' in headers.get('content-type', ''):
                    json_data = json.loads(body) if body else {}
                    response = client.post(path, json=json_data, query_string=query_params)
                else:
                    response = client.post(path, data=body, query_string=query_params)
            else:
                response = client.get(path, query_string=query_params)
        
        # Convert Flask response to Netlify format
        response_headers = {}
        for key, value in response.headers:
            response_headers[key] = value
            
        return {
            'statusCode': response.status_code,
            'headers': response_headers,
            'body': response.get_data(as_text=True)
        }
        
    except Exception as e:
        logging.error(f"Function handler error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/html'},
            'body': f'<h1>Internal Server Error</h1><p>Error: {str(e)}</p>'
        }