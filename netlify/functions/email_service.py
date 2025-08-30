import os
import secrets
import string
import yagmail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Keep SendGrid as backup
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
except ImportError:
    SendGridAPIClient = None
    Mail = None

def generate_order_id():
    """Generate a random order ID"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def send_order_confirmation_email(order_data, cart_items):
    """Send order confirmation email to customer using available email service"""
    
    # Check for EmailJS/Client-side email service keys
    emailjs_public_key = os.environ.get('EMAILJS_PUBLIC_KEY')
    emailjs_private_key = os.environ.get('EMAILJS_PRIVATE_KEY')
    
    # Try Gmail SMTP (free option)
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    
    # Fallback to SendGrid
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    
    if emailjs_public_key and emailjs_private_key:
        return send_emailjs_email(order_data, cart_items)
    elif gmail_user and gmail_password:
        return send_gmail_email(order_data, cart_items, gmail_user, gmail_password)
    elif sendgrid_api_key:
        return send_sendgrid_email(order_data, cart_items, sendgrid_api_key)
    else:
        print("No email service configured. Please set email service credentials")
        # Generate order ID anyway for logging
        order_id = generate_order_id()
        print(f"Order ID generated: {order_id}")
        return order_id

def send_emailjs_email(order_data, cart_items):
    """EmailJS integration - order ID generation for frontend email sending"""
    # Generate order ID for tracking
    order_id = generate_order_id()
    print(f"Order confirmation will be sent via EmailJS to {order_data['Email']}")
    print(f"EmailJS configured - Order ID: {order_id}")
    print("Email will be sent via frontend EmailJS integration")
    return order_id

def send_gmail_email(order_data, cart_items, gmail_user, gmail_password):
    """Send email using Gmail SMTP (free)"""
    try:
        # Generate order ID
        order_id = generate_order_id()
        
        # Calculate total from cart items
        total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
        
        # Create item list string for HTML
        item_list = []
        for item in cart_items:
            item_list.append(f"                <strong>{item['name']}</strong><br>")
            item_list.append(f"                   Size: {item['size']} | Frame: {item['frameText']}<br>")
            item_list.append(f"                   Quantity: {item['quantity']} | Price: ₹{item['price'] * item['quantity']}<br><br>")
        
        items_text = '\n'.join(item_list)
        
        # Create HTML email content
        email_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
        .order-section {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 6px; border-left: 4px solid #3498db; }}
        .order-id {{ font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 15px; }}
        .item-list {{ background-color: #ecf0f1; padding: 15px; border-radius: 4px; margin: 10px 0; }}
        .total {{ font-size: 18px; font-weight: bold; color: #27ae60; text-align: right; margin-top: 15px; }}
        .address {{ background-color: #fff; padding: 15px; border-radius: 4px; border: 1px solid #ddd; margin: 10px 0; }}
        .no-link {{ color: #333 !important; text-decoration: none !important; }}
        .no-link a {{ color: #333 !important; text-decoration: none !important; pointer-events: none; }}
        span[data-auto-link] {{ color: #333 !important; text-decoration: none !important; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #3498db; text-align: center; }}
        .signature {{ color: #7f8c8d; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Filmytea</h1>
        <p>Your Order Confirmation</p>
    </div>
    
    <div class="content">
        <h2>Dear {order_data['Customer Name']},</h2>
        
        <p>Thank you for placing your order with <strong>Filmytea</strong>! We are excited to let you know that your order has been successfully received and is currently being processed.</p>
        
        <div class="order-section">
            <div class="order-id">Order ID: {order_id}</div>
            
            <h3>Item Details:</h3>
            <div class="item-list">
{items_text}
            </div>
            
            <div class="total">Total Amount: ₹{total_amount}</div>
        </div>
        
        <div class="order-section">
            <h3>Delivery Information:</h3>
            <div class="address">
                <strong>Delivery Address:</strong><br>
                <div class="no-link" style="color: #333 !important; text-decoration: none !important; font-family: Arial, sans-serif;">{order_data['Address']}</div>
                <div class="no-link" style="color: #333 !important; text-decoration: none !important; font-family: Arial, sans-serif;">{order_data['City']}, {order_data['State']} - {order_data['Pincode']}</div>
            </div>
        </div>
        
        <p>Once your order is shipped, you will receive another email with tracking details.</p>
        
        <p>If you have any questions or need further assistance, feel free to reach out to us!</p>
        
        <p>Thank you for your support, and we look forward to delivering your amazing posters soon!</p>
        
        <div class="footer">
            <p><strong>Best Regards,</strong><br>
            Sujay<br>
            <em>Filmytea Team</em></p>
            
            <div class="signature">
                Contact: <a href="mailto:filmyteacare@gmail.com">filmyteacare@gmail.com</a><br>
                Visit us at Filmytea for more amazing posters!
            </div>
        </div>
    </div>
</body>
</html>"""

        # Send email using Gmail SMTP
        yag = yagmail.SMTP(gmail_user, gmail_password)
        yag.send(
            to=order_data['Email'],
            subject=f"Order Confirmation - {order_id} - Filmytea",
            contents=email_content
        )
        
        print(f"Order confirmation email sent successfully via Gmail to {order_data['Email']}")
        print(f"Order ID: {order_id}")
        return order_id
        
    except Exception as e:
        print(f"Gmail SMTP error: {e}")
        order_id = generate_order_id()
        print(f"Order ID generated: {order_id}")
        return order_id

def send_sendgrid_email(order_data, cart_items, sendgrid_api_key):
    """Send email using SendGrid (backup option)"""
    if not SendGridAPIClient or not Mail:
        print("SendGrid not available")
        order_id = generate_order_id()
        return order_id
        
    try:
        sender_email = "filmyteacare@gmail.com"
        
        # Generate order ID
        order_id = generate_order_id()
        
        # Calculate total from cart items
        total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
        
        # Create item list string for HTML
        item_list = []
        for item in cart_items:
            item_list.append(f"                <strong>{item['name']}</strong><br>")
            item_list.append(f"                   Size: {item['size']} | Frame: {item['frameText']}<br>")
            item_list.append(f"                   Quantity: {item['quantity']} | Price: ₹{item['price'] * item['quantity']}<br><br>")
        
        items_text = '\n'.join(item_list)
        
        # Create HTML email content (same as Gmail version)
        email_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
        .order-section {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 6px; border-left: 4px solid #3498db; }}
        .order-id {{ font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 15px; }}
        .item-list {{ background-color: #ecf0f1; padding: 15px; border-radius: 4px; margin: 10px 0; }}
        .total {{ font-size: 18px; font-weight: bold; color: #27ae60; text-align: right; margin-top: 15px; }}
        .address {{ background-color: #fff; padding: 15px; border-radius: 4px; border: 1px solid #ddd; margin: 10px 0; }}
        .no-link {{ color: #333 !important; text-decoration: none !important; }}
        .no-link a {{ color: #333 !important; text-decoration: none !important; pointer-events: none; }}
        span[data-auto-link] {{ color: #333 !important; text-decoration: none !important; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #3498db; text-align: center; }}
        .signature {{ color: #7f8c8d; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Filmytea</h1>
        <p>Your Order Confirmation</p>
    </div>
    
    <div class="content">
        <h2>Dear {order_data['Customer Name']},</h2>
        
        <p>Thank you for placing your order with <strong>Filmytea</strong>! We are excited to let you know that your order has been successfully received and is currently being processed.</p>
        
        <div class="order-section">
            <div class="order-id">Order ID: {order_id}</div>
            
            <h3>Item Details:</h3>
            <div class="item-list">
{items_text}
            </div>
            
            <div class="total">Total Amount: ₹{total_amount}</div>
        </div>
        
        <div class="order-section">
            <h3>Delivery Information:</h3>
            <div class="address">
                <strong>Delivery Address:</strong><br>
                <div class="no-link" style="color: #333 !important; text-decoration: none !important; font-family: Arial, sans-serif;">{order_data['Address']}</div>
                <div class="no-link" style="color: #333 !important; text-decoration: none !important; font-family: Arial, sans-serif;">{order_data['City']}, {order_data['State']} - {order_data['Pincode']}</div>
            </div>
        </div>
        
        <p>Once your order is shipped, you will receive another email with tracking details.</p>
        
        <p>If you have any questions or need further assistance, feel free to reach out to us!</p>
        
        <p>Thank you for your support, and we look forward to delivering your amazing posters soon!</p>
        
        <div class="footer">
            <p><strong>Best Regards,</strong><br>
            Sujay<br>
            <em>Filmytea Team</em></p>
            
            <div class="signature">
                Contact: <a href="mailto:filmyteacare@gmail.com">filmyteacare@gmail.com</a><br>
                Visit us at Filmytea for more amazing posters!
            </div>
        </div>
    </div>
</body>
</html>"""

        # Create SendGrid message
        message = Mail(
            from_email=sender_email,
            to_emails=order_data['Email'],
            subject=f"Order Confirmation - {order_id} - Filmytea",
            html_content=email_content
        )
        
        # Send email using SendGrid
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        
        print(f"Order confirmation email sent successfully via SendGrid to {order_data['Email']}")
        print(f"Order ID: {order_id}")
        print(f"SendGrid Response: {response.status_code}")
        return order_id
        
    except Exception as e:
        print(f"SendGrid error: {e}")
        order_id = generate_order_id()
        return order_id