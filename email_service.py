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
    
    # Create item list string
    item_list = []
    for item in cart_items:
        item_list.append(f"• {item['name']} (Size: {item['size']}, Frame: {item['frameText']}) - Qty: {item['quantity']} - ₹{item['price'] * item['quantity']}")
    
    items_text = '\n'.join(item_list)
    
    # Create email content
    email_content = f"""Dear {order_data['Customer Name']},

Thank you for placing your order with Filmytea! We are excited to let you know that your order has been successfully received and is currently being processed.

Order Details:
Order ID: {order_id}
Item(s):
{items_text}

Total Amount: ₹{total_amount}
Delivery Address: {order_data['Address']}, {order_data['City']}, {order_data['State']} - {order_data['Pincode']}

Once your order is shipped, you will receive another email with tracking details. If you have any questions or need further assistance, feel free to reach out!

Thank you for your support, and we look forward to delivering your order soon!

Best Regards,
Sujay
Filmytea Team
contact: filmyteacare@gmail.com"""

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"Filmytea <{gmail_user}>"
        msg['To'] = order_data['Email']
        msg['Subject'] = f"Order Confirmation - {order_id} - Filmytea"
        
        # Add body to email
        msg.attach(MIMEText(email_content, 'plain'))
        
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