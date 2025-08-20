// Google Apps Script - Filmytea Store
// Main backend logic

// All posters data
const ALL_POSTERS = [
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
];

// Main function to serve the web app
function doGet(e) {
  const page = e.parameter.page || 'index';
  const posterId = e.parameter.id;
  
  switch(page) {
    case 'posters':
      return HtmlService.createTemplateFromFile('posters')
        .evaluate()
        .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
    
    case 'poster':
      if (posterId) {
        const poster = ALL_POSTERS.find(p => p.id === posterId);
        if (poster) {
          const template = HtmlService.createTemplateFromFile('poster_detail');
          template.poster = poster;
          return template.evaluate()
            .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
        }
      }
      return HtmlService.createHtmlOutput('<h2>Poster not found</h2><a href="?">← Home</a>');
    
    case 'cart':
      return HtmlService.createTemplateFromFile('cart')
        .evaluate()
        .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
    
    case 'checkout':
      return HtmlService.createTemplateFromFile('checkout')
        .evaluate()
        .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
    
    default:
      return HtmlService.createTemplateFromFile('index')
        .evaluate()
        .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
  }
}

// Handle form submissions
function doPost(e) {
  const action = e.parameter.action;
  
  if (action === 'place_order') {
    return processOrder(e.parameter);
  }
  
  return ContentService.createTextOutput('Invalid action');
}

// Process order and send confirmation email
function processOrder(formData) {
  try {
    // Generate order ID
    const orderId = 'FL' + Date.now().toString().slice(-6) + Math.random().toString(36).substr(2, 2).toUpperCase();
    
    // Parse cart items
    let cartItems = [];
    try {
      cartItems = JSON.parse(formData.cart_items || '[]');
    } catch(e) {
      cartItems = [];
    }
    
    // Calculate total
    const totalAmount = cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
    
    // Order details
    const orderDetails = {
      orderId: orderId,
      customerName: formData.customer_name,
      email: formData.email,
      phone: formData.phone_number,
      address: formData.address,
      city: formData.city,
      state: formData.state,
      pincode: formData.pincode,
      cashOnDelivery: formData.cash_on_delivery,
      items: cartItems,
      totalAmount: totalAmount,
      orderDate: new Date().toLocaleDateString()
    };
    
    // Send confirmation email
    sendOrderConfirmationEmail(orderDetails);
    
    // Save to Google Sheets (optional)
    saveOrderToSheet(orderDetails);
    
    // Return success page
    const template = HtmlService.createTemplateFromFile('order_success');
    template.order = orderDetails;
    return template.evaluate()
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
      
  } catch (error) {
    console.error('Order processing error:', error);
    return HtmlService.createHtmlOutput('<h2>Order processing failed. Please try again.</h2>');
  }
}

// Send order confirmation email using Gmail API
function sendOrderConfirmationEmail(orderDetails) {
  try {
    // Create items list
    const itemsList = orderDetails.items.map(item => 
      `• ${item.name} (Size: ${item.size}, Frame: ${item.frameText}) - Qty: ${item.quantity} - ₹${item.price * item.quantity}`
    ).join('\n');
    
    // Email content
    const emailBody = `Dear ${orderDetails.customerName},

Thank you for placing your order with Filmytea! We are excited to let you know that your order has been successfully received and is currently being processed.

Order Details:
Order ID: ${orderDetails.orderId}
Item(s):
${itemsList}

Total Amount: ₹${orderDetails.totalAmount}
Delivery Address: ${orderDetails.address}, ${orderDetails.city}, ${orderDetails.state} - ${orderDetails.pincode}

Once your order is shipped, you will receive another email with tracking details. If you have any questions or need further assistance, feel free to reach out!

Thank you for your support, and we look forward to delivering your order soon!

Best Regards,
Sujay
Filmytea Team
contact: filmyteacare@gmail.com`;

    // Send email
    GmailApp.sendEmail(
      orderDetails.email,
      `Order Confirmation - ${orderDetails.orderId} - Filmytea`,
      emailBody,
      {
        name: 'Filmytea',
        replyTo: 'filmyteacare@gmail.com'
      }
    );
    
    console.log(`Order confirmation email sent to ${orderDetails.email}`);
    
  } catch (error) {
    console.error('Email sending failed:', error);
  }
}

// Save order to Google Sheets (optional)
function saveOrderToSheet(orderDetails) {
  try {
    // Get or create spreadsheet
    let spreadsheet;
    try {
      spreadsheet = SpreadsheetApp.openById('YOUR_SPREADSHEET_ID'); // Replace with your sheet ID
    } catch (e) {
      // Create new spreadsheet if not exists
      spreadsheet = SpreadsheetApp.create('Filmytea Orders');
      console.log('Created new spreadsheet:', spreadsheet.getId());
    }
    
    const sheet = spreadsheet.getActiveSheet();
    
    // Add headers if first row is empty
    if (sheet.getLastRow() === 0) {
      sheet.getRange(1, 1, 1, 11).setValues([[
        'Order ID', 'Date', 'Customer Name', 'Email', 'Phone', 
        'Address', 'City', 'State', 'Pincode', 'Total Amount', 'Items'
      ]]);
    }
    
    // Add order data
    const itemsString = orderDetails.items.map(item => 
      `${item.quantity}x ${item.name} (${item.size}, ${item.frameText})`
    ).join('; ');
    
    sheet.appendRow([
      orderDetails.orderId,
      orderDetails.orderDate,
      orderDetails.customerName,
      orderDetails.email,
      orderDetails.phone,
      orderDetails.address,
      orderDetails.city,
      orderDetails.state,
      orderDetails.pincode,
      orderDetails.totalAmount,
      itemsString
    ]);
    
  } catch (error) {
    console.error('Error saving to sheet:', error);
  }
}

// Get all posters (for AJAX requests)
function getAllPosters() {
  return ALL_POSTERS;
}

// Get single poster (for AJAX requests)
function getPoster(posterId) {
  return ALL_POSTERS.find(p => p.id === posterId);
}

// Include CSS and JS files
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}