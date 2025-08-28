import os
import logging
import json

from flask import Flask, render_template, abort, request, redirect, url_for, jsonify, flash
from email_service import send_order_confirmation_email
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from instamojo_wrapper import Instamojo


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dummy-secret-key-for-development-123")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

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
    # Create tables if needed
    db.create_all()

# Initialize Instamojo
api_key = os.environ.get("INSTAMOJO_API_KEY")
auth_token = os.environ.get("INSTAMOJO_AUTH_TOKEN")

if api_key and auth_token:
    # Use test endpoint - change to production endpoint when going live
    instamojo_api = Instamojo(
        api_key=api_key,
        auth_token=auth_token,
        endpoint='https://test.instamojo.com/api/1.1/'
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
    
    # Render success page with order details
    return render_template('order_success.html', order=order, order_id=order_id)

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
    """Dummy payment system for development"""
    try:
        # Get order details from form
        customer_name = request.form.get('customer_name')
        email = request.form.get('email')
        phone = request.form.get('phone_number')
        cart_total = float(request.form.get('cart_total', 0))
        
        # Get cart items
        cart_items_json = request.form.get('cart_items', '[]')
        try:
            cart_items = json.loads(cart_items_json)
        except:
            cart_items = []
        
        # Store order data in session for dummy payment
        from flask import session
        import time
        
        dummy_payment_id = f"dummy_{int(time.time())}"
        
        session['pending_order'] = {
            'customer_name': customer_name,
            'email': email,
            'phone_number': phone,
            'address': request.form.get('address'),
            'pincode': request.form.get('pincode'),
            'city': request.form.get('city'),
            'state': request.form.get('state'),
            'cart_items': cart_items,
            'cart_total': cart_total,
            'payment_id': dummy_payment_id
        }
        
        logging.info(f"Dummy payment created: {dummy_payment_id}")
        
        # Redirect directly to success page for dummy payment
        return redirect(url_for('payment_success', payment_id=dummy_payment_id, payment_request_id=dummy_payment_id))
        
    except Exception as e:
        logging.error(f"Error creating dummy payment: {e}")
        flash('Error processing payment. Please try again.', 'error')
        return redirect(url_for('checkout'))

@app.route('/payment-success')
def payment_success():
    """Handle successful dummy payment redirect"""
    from flask import session
    
    payment_id = request.args.get('payment_id')
    payment_request_id = request.args.get('payment_request_id')
    
    # Get order data from session
    pending_order = session.get('pending_order')
    
    if pending_order:
        try:
            # For dummy payment, always consider it successful
            order = {
                'Customer Name': pending_order['customer_name'],
                'Email': pending_order['email'],
                'Phone Number': pending_order['phone_number'],
                'Address': pending_order['address'],
                'Pincode': pending_order['pincode'],
                'City': pending_order['city'],
                'State': pending_order['state'],
                'Payment Status': 'Paid (Demo)',
                'Payment ID': payment_id or 'DEMO_PAYMENT',
                'Amount': pending_order['cart_total']
            }
            
            cart_items = pending_order['cart_items']
            
            # Log successful order
            logging.info("Order completed successfully with payment!")
            for key, value in order.items():
                logging.info(f"{key}: {value}")
            
            # Send order confirmation email
            order_id = None
            if order.get('Email'):
                try:
                    order_id = send_order_confirmation_email(order, cart_items)
                    if order_id:
                        logging.info(f"Order confirmation email sent successfully to {order['Email']}")
                except Exception as e:
                    logging.error(f"Failed to send order confirmation email: {e}")
            
            # Clear session data
            session.pop('pending_order', None)
            
            return render_template('order_success.html', order=order, order_id=order_id, paid=True)
        except Exception as e:
            logging.error(f"Error verifying payment: {e}")
            flash('Error verifying payment. Please contact support.', 'error')
            return redirect(url_for('checkout'))
    
    flash('Invalid payment session. Please try again.', 'error')
    return redirect(url_for('checkout'))

@app.route('/payment-webhook', methods=['POST'])
def payment_webhook():
    """Handle Instamojo payment webhook"""
    try:
        data = request.form.to_dict()
        logging.info(f"Payment webhook received: {data}")
        
        # Here you would typically verify the webhook MAC and update order status
        # For now, just log the payment notification
        if data.get('status') == 'Credit':
            logging.info(f"Payment successful webhook: {data.get('payment_id')}")
        
        return "OK"
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return "Error", 500

@app.route('/send-order-email', methods=['POST'])
def send_order_email():
    """Send order confirmation email with cart data"""
    try:
        data = request.get_json()
        order_data = data.get('order', {})
        cart_items = data.get('cart_items', [])
        
        order_id = send_order_confirmation_email(order_data, cart_items)
        
        if order_id:
            return {'success': True, 'order_id': order_id}
        else:
            return {'success': False, 'error': 'Failed to send email'}, 500
            
    except Exception as e:
        logging.error(f"Error sending order email: {e}")
        return {'success': False, 'error': str(e)}, 500