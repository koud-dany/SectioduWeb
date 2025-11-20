# 🚀 HOSTINGER FILE MANAGER DEPLOYMENT GUIDE
## Deploy lasectionduweb.org WITHOUT SSH

Since you don't have SSH access, we'll use **Hostinger's File Manager** for deployment.

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### ✅ **What You Need:**
1. **Your Hostinger Username** (find in hPanel dashboard - looks like `u123456789`)
2. **Domain pointed to Hostinger** (use nameservers: `ns1.dns-parking.com`, `ns2.dns-parking.com`)
3. **Python support** (check hPanel → Advanced → Select PHP Version)
4. **Your existing credentials** (AWS S3, Cloudinary, etc.)

---

## 🔧 STEP-BY-STEP DEPLOYMENT

### **STEP 1: Get Your Hostinger Username**
1. Login to **Hostinger hPanel**
2. Look for your **username** (usually `u123456789`)
3. **Write it down** - you'll need it for file paths

### **STEP 2: Upload Files via File Manager**
1. **hPanel** → **File Manager**
2. **Navigate to** `/public_html` folder
3. **Delete default files** (index.html, etc.)
4. **Upload ALL your project files** including:
   ```
   ├── app.py
   ├── config.py
   ├── passenger_wsgi.py
   ├── .htaccess
   ├── requirements.txt
   ├── tournament.db
   ├── static/
   ├── templates/
   └── all other project files
   ```

### **STEP 3: Create Production Environment File**
1. **In File Manager**, create new file: `.env`
2. **Copy content from** `.env.production` (in your project folder)
3. **Update with your actual credentials:**
   ```bash
   # Replace with your actual AWS credentials
   AWS_ACCESS_KEY_ID=your_actual_aws_key
   AWS_SECRET_ACCESS_KEY=your_actual_secret
   S3_BUCKET=your_bucket_name
   ```

### **STEP 4: Update Configuration Files**
1. **Edit `passenger_wsgi.py`**:
   - Replace `YOUR_USERNAME` with your actual Hostinger username
   - Example: `/home/u123456789/public_html`

2. **Edit `.htaccess`**:
   - Replace `YOUR_USERNAME` with your actual username
   - Example: `PassengerAppRoot /home/u123456789/public_html`

### **STEP 5: Install Python Dependencies**
**Option A: Using Terminal (if available)**
1. **hPanel** → **Advanced** → **Terminal** (if available)
2. Run: `pip3 install -r requirements.txt`

**Option B: Contact Hostinger Support**
- Ask them to install dependencies from your `requirements.txt`

### **STEP 6: Configure Domain**
1. **hPanel** → **Domains**
2. **Add Domain**: `lasectionduweb.org`
3. **Point to**: `/public_html`
4. **Wait for DNS propagation** (24-48 hours)

### **STEP 7: Enable Python Application**
1. **hPanel** → **Advanced** → **Select PHP Version**
2. **Switch to Python** (if available)
3. **Select Python 3.8+**
4. **Enable Passenger**

---

## 🔍 TESTING DEPLOYMENT

### **Test Your Site:**
1. **Visit**: `https://lasectionduweb.org`
2. **Check for errors** in browser console
3. **Test key features**:
   - User registration/login
   - Video upload
   - Voting system
   - Admin panel

### **If There Are Errors:**
1. **Check File Manager logs**
2. **Verify file permissions** (755 for folders, 644 for files)
3. **Ensure all files uploaded correctly**
4. **Double-check .env credentials**

---

## 🆘 TROUBLESHOOTING

### **Common Issues:**

**🔸 "Internal Server Error (500)"**
- Check `.htaccess` file syntax
- Verify `passenger_wsgi.py` paths
- Ensure Python dependencies installed

**🔸 "Module not found errors"**
- Install missing packages: `pip3 install package_name`
- Check `requirements.txt` uploaded correctly

**🔸 "Database errors"**
- Ensure `tournament.db` uploaded
- Check database file permissions
- Verify database path in config

**🔸 "Static files not loading"**
- Check `static/` folder uploaded
- Verify file permissions
- Clear browser cache

---

## 📞 HOSTINGER SUPPORT

If you encounter issues:
1. **Contact Hostinger Support**
2. **Tell them**: "I need help setting up a Python Flask application"
3. **Provide**: Your `requirements.txt` file
4. **Ask for**: Python dependency installation assistance

---

## 🎯 QUICK CHECKLIST

Before going live:
- [ ] All files uploaded to `/public_html`
- [ ] `.env` file created with real credentials
- [ ] `passenger_wsgi.py` updated with your username
- [ ] `.htaccess` updated with your username
- [ ] Python dependencies installed
- [ ] Domain pointing to Hostinger
- [ ] Site loads at `https://lasectionduweb.org`

---

## 📧 NEXT STEPS

Once deployed:
1. **Test thoroughly**
2. **Set up SSL certificate** (usually automatic)
3. **Monitor for errors**
4. **Create admin account**
5. **Upload test videos**

**Your site will be live at: https://lasectionduweb.org** 🌟
