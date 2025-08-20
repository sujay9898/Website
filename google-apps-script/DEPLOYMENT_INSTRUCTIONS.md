# Filmytea Google Apps Script Deployment Instructions

## 📋 **Complete Setup Guide**

### **Step 1: Create Google Apps Script Project**

1. **Go to** [script.google.com](https://script.google.com)
2. **Click** "New Project"
3. **Rename** your project to "Filmytea Store"

### **Step 2: Upload All Files**

**Delete the default `Code.gs` file first, then create these files:**

1. **Code.gs** - Copy content from `google-apps-script/Code.gs`
2. **index.html** - Copy content from `google-apps-script/index.html`  
3. **posters.html** - Copy content from `google-apps-script/posters.html`
4. **poster_detail.html** - Copy content from `google-apps-script/poster_detail.html`
5. **cart.html** - Copy content from `google-apps-script/cart.html`
6. **checkout.html** - Copy content from `google-apps-script/checkout.html`
7. **order_success.html** - Copy content from `google-apps-script/order_success.html`
8. **style.html** - Copy content from `google-apps-script/style.html`
9. **cart_js.html** - Copy content from `google-apps-script/cart_js.html`

### **Step 3: Configure Email Permissions**

1. **In Code.gs**, find the `sendOrderConfirmationEmail` function
2. **Save** your project (Ctrl+S)
3. **Click** the "Run" button to authorize Gmail permissions
4. **Allow** Gmail access when prompted

### **Step 4: Deploy as Web App**

1. **Click** "Deploy" → "New deployment"
2. **Settings:**
   - Type: Web app
   - Description: "Filmytea Store v1"
   - Execute as: Me
   - Who has access: Anyone
3. **Click** "Deploy"
4. **Copy** the web app URL - this is your live website!

### **Step 5: Optional - Google Sheets Integration**

**To store orders in Google Sheets:**
1. **Create** a new Google Sheet
2. **Copy** the Sheet ID from the URL
3. **In Code.gs**, replace `YOUR_SPREADSHEET_ID` with your actual Sheet ID
4. **Redeploy** your web app

## 🎉 **Your Store is Live!**

**Features Working:**
✅ Browse 39 movie posters  
✅ Add to cart with size/frame selection  
✅ Complete checkout process  
✅ **Automatic Gmail email confirmations**  
✅ Order storage in Google Sheets (if configured)  
✅ Mobile responsive design  
✅ Professional order management  

## 📧 **Email Configuration**

The Gmail integration works automatically using your Google account. Order confirmation emails will be sent from your Gmail address to customers.

## 🔧 **Customization**

**To modify poster data:**
- Edit the `ALL_POSTERS` array in `Code.gs`

**To change email template:**
- Modify `sendOrderConfirmationEmail` function in `Code.gs`

**To update styling:**
- Edit `style.html` file

## 🚀 **Benefits Over Other Platforms**

✅ **Completely FREE** - No hosting costs  
✅ **Built-in Gmail** - No email service setup needed  
✅ **Google Sheets** - Free database alternative  
✅ **Auto-scaling** - Handles traffic automatically  
✅ **99.9% uptime** - Google's infrastructure  
✅ **SSL included** - Secure HTTPS automatically  

## 📱 **Access Your Store**

Your Filmytea store will be available at:
`https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec`

**Share this URL with customers - your store is ready for business!**

---

**Need help?** The deployment process is straightforward, but if you encounter issues, check the Google Apps Script logs in the execution transcript.