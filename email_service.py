import os
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_order_id():
    """Generate a random order ID"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def send_order_confirmation_email(order_data, cart_items):
    """Send order confirmation email to customer using Gmail SMTP"""
    gmail_user = "filmyteacare@gmail.com"
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if not gmail_password:
        print("Gmail app password not found")
        return False
    
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
                <span style="color: #333; text-decoration: none;">{order_data['Address']}</span><br>
                <span style="color: #333; text-decoration: none;">{order_data['City']}, {order_data['State']} - {order_data['Pincode']}</span>
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

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"Filmytea <{gmail_user}>"
        msg['To'] = order_data['Email']
        msg['Subject'] = f"Order Confirmation - {order_id} - Filmytea"
        
        # Add body to email
        msg.attach(MIMEText(email_content, 'html'))
        
        # Gmail SMTP configuration
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        server.login(gmail_user, gmail_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(gmail_user, order_data['Email'], text)
        server.quit()
        
        print(f"Order confirmation email sent successfully to {order_data['Email']}")
        print(f"Order ID: {order_id}")
        return order_id
        
    except Exception as e:
        print(f"Gmail SMTP error: {e}")
        return False