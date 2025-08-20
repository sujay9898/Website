import os
import logging

from flask import Flask, render_template, abort, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
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

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    # import models  # noqa: F401
    db.create_all()

# All posters data
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
    """Process the order with buy now functionality"""
    # Collect order details from form
    order = {
        'Reference Number': request.form.get('reference_number'),
        'Retail Price': request.form.get('retail_price'),
        'Customer Name': request.form.get('customer_name'),
        'Address Line 1': request.form.get('address_line1'),
        'Address Line 2': request.form.get('address_line2'),
        'Address Line 3 / Landmark': request.form.get('address_line3'),
        'Pincode': request.form.get('pincode'),
        'City': request.form.get('city'),
        'State': request.form.get('state'),
        'Phone Number': request.form.get('phone_number'),
        'Email': request.form.get('email'),
        'Cash on Delivery': request.form.get('cash_on_delivery')
    }
    
    # Log order details for processing
    logging.info("Order captured successfully!")
    for key, value in order.items():
        logging.info(f"{key}: {value}")
    
    # Render success page with order details
    return render_template('order_success.html', order=order)